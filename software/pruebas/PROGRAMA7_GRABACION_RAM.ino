/*
 * =========================================================================
 * CANSAT RAM - GRABACIÓN E INTELIGENCIA DE VUELO (ADAPTADO PARA RADIO)
 * =========================================================================
 * * NOTA: Se ha añadido la "Espera Inteligente" para permitir arranque con batería.
 * * Los datos se envían por Serial1 (Radio) y se guardan en RAM.
 * =========================================================================
 */

#include <Arduino_BMI270_BMM150.h>
#include <Arduino_HS300x.h>
#include <Arduino_LPS22HB.h>

// Usamos Serial1 para la radio APC220
#define radioSerial Serial1

// ================= CONFIGURACIÓN FIJA =================
#define INTERVALO_GRABACION 1000 
#define MAX_REGISTROS 500
#define ALT_ATERRIZAJE 0.3
#define TIEMPO_ATERRIZAJE 5000
// =====================================================

struct DatosSensor {
  uint32_t timestamp;
  int16_t temperatura, humedad, presion, altitud, accX, accY, accZ;
};

DatosSensor registros[MAX_REGISTROS];
int numRegistros = 0;
bool grabando = false;
bool aterrizado = false;
float altitudBase = 0, altitudMax = -1000;
int contadorDescenso = 0;
unsigned long tiempoInicio = 0, ultimaGrabacion = 0;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);      // USB
  radioSerial.begin(9600); // Radio APC220

  // --- CONTROL DE ARRANQUE AUTÓNOMO (BATERÍA) ---
  unsigned long ventanaEspera = millis();
  while (!Serial && millis() - ventanaEspera < 5000) {
    // Espera 5s al USB; si no hay, arranca solo para la misión.
  }

  if (!IMU.begin() || !HS300x.begin() || !BARO.begin()) {
    radioSerial.println(">>> ERROR: SENSORES NO DETECTADOS <<<");
    while (1);
  }

  // Calibración inicial
  float suma = 0;
  for(int i=0; i<20; i++) { suma += calcularAltitud(); delay(50); }
  altitudBase = suma / 20.0;
  
  radioSerial.println("--- CANSAT LISTO PARA LANZAMIENTO ---");
  radioSerial.print("Altitud Base: "); radioSerial.println(altitudBase);
}

void loop() {
  float altActual = calcularAltitud();
  float altRelativa = altActual - altitudBase;

  // 1. TRANSMISIÓN DE TELEMETRÍA POR RADIO (Tiempo real)
  static unsigned long lastMonitor = 0;
  if (millis() - lastMonitor > 1000) { // Enviamos cada 1 seg por radio
    String msg = "ALT:" + String(altRelativa) + " MAX:" + String(altitudMax);
    if (grabando) msg = ">>> REC [" + String(numRegistros) + "] " + msg;
    
    radioSerial.println(msg); 
    Serial.println(msg); // También al USB para pruebas
    lastMonitor = millis();
  }

  // 2. DETECTAR DESCENSO
  if (!grabando && !aterrizado) {
    if (altRelativa > altitudMax) altitudMax = altRelativa;
    
    float bajada = altitudMax - altRelativa;
    float umbralDinamico = (altitudMax < 5.0) ? 0.35 : 2.0;
    int ciclosNecesarios = (altitudMax < 5.0) ? 2 : 5;

    if (bajada > umbralDinamico) {
      contadorDescenso++;
    } else {
      contadorDescenso = 0;
    }

    if (contadorDescenso >= ciclosNecesarios) {
      iniciarGrabacion();
    }
  }

  // 3. PROCESO DE GRABACIÓN EN RAM
  if (grabando) {
    if (millis() - ultimaGrabacion >= INTERVALO_GRABACION) {
      ultimaGrabacion = millis();
      grabarRegistro(altRelativa);
    }
    detectarAterrizaje(altRelativa);
    digitalWrite(LED_BUILTIN, (millis() / 250) % 2); 
  }

  // 4. GESTIÓN DE COMANDOS (Desde Radio o USB)
  gestionarComandos();
}

// --- FUNCIONES ---

void gestionarComandos() {
  Stream* entrada = NULL;
  if (Serial.available()) entrada = &Serial;
  else if (radioSerial.available()) entrada = &radioSerial;

  if (entrada) {
    String c = entrada->readStringUntil('\n');
    c.trim(); c.toUpperCase();
    
    if (c == "CSV") exportarCSV();
    if (c == "BORRAR") { numRegistros = 0; aterrizado = false; altitudMax = -1000; radioSerial.println("MEMORIA LIMPIA"); }
    if (c == "GRABAR") iniciarGrabacion();
  }
}

float calcularAltitud() {
  float p = BARO.readPressure();
  return 44330.0 * (1.0 - pow(p / 1013.25, 0.1903));
}

void iniciarGrabacion() {
  if (!grabando) {
    radioSerial.println("\n!!! GRABACION INICIADA !!!");
    grabando = true;
    tiempoInicio = millis();
    ultimaGrabacion = millis();
  }
}

void detectarAterrizaje(float altRel) {
  if (abs(altRel) < ALT_ATERRIZAJE) {
    static unsigned long tiempoSuelo = 0;
    if (tiempoSuelo == 0) tiempoSuelo = millis();
    if (millis() - tiempoSuelo > TIEMPO_ATERRIZAJE) {
      grabando = false;
      aterrizado = true;
      radioSerial.println(">>> ATERRIZAJE DETECTADO <<<");
    }
  }
}

void grabarRegistro(float altRel) {
  if (numRegistros >= MAX_REGISTROS) {
    grabando = false;
    return;
  }
  DatosSensor d;
  d.timestamp = millis() - tiempoInicio;
  d.altitud = altRel * 100;
  d.temperatura = HS300x.readTemperature() * 100;
  d.humedad = HS300x.readHumidity() * 100;
  d.presion = BARO.readPressure();
  float x, y, z;
  IMU.readAcceleration(x, y, z);
  d.accX = x * 100; d.accY = y * 100; d.accZ = z * 100;
  registros[numRegistros++] = d;
}

void exportarCSV() {
  // Envía el volcado de memoria por la radio
  radioSerial.println("t_ms,temp,hum,pres,alt_cm,ax,ay,az");
  for (int i = 0; i < numRegistros; i++) {
    auto d = registros[i];
    radioSerial.print(d.timestamp); radioSerial.print(",");
    radioSerial.print(d.temperatura/100.0); radioSerial.print(",");
    radioSerial.print(d.humedad/100.0); radioSerial.print(",");
    radioSerial.print(d.presion); radioSerial.print(",");
    radioSerial.print(d.altitud); radioSerial.print(",");
    radioSerial.print(d.accX/100.0); radioSerial.print(",");
    radioSerial.print(d.accY/100.0); radioSerial.print(",");
    radioSerial.println(d.accZ/100.0);
  }
}
