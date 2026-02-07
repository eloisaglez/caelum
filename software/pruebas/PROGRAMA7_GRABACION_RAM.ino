/*
 * =========================================================================
 * CANSAT RAM - GRABACIÓN
 * =========================================================================
 * * FORMAS DE INICIAR LA GRABACIÓN:
 * * 1. MODO AUTOMÁTICO (POR DESCENSO):
 * - En el AULA (< 5m de altura): Se activa al bajar solo 35 cm.
 * - En VUELO REAL (> 5m de altura): Se activa al bajar 2 metros para 
 * evitar fallos por ráfagas de viento.
 * * 2. MODO MANUAL (COMANDO):
 * - Escribir "GRABAR" en el monitor serie y pulsar Enter.
 * - Útil si quieres forzar la grabación antes del lanzamiento.
 * * COMANDOS DISPONIBLES EN MONITOR SERIE:
 * - "CSV"    : Muestra todos los datos guardados en formato Excel.
 * - "BORRAR" : Limpia la memoria (hazlo justo antes de lanzar).
 * - "GRABAR" : Inicia la grabación manualmente.
 * =========================================================================
 */

#include <Arduino_BMI270_BMM150.h>
#include <Arduino_HS300x.h>
#include <Arduino_LPS22HB.h>

// ================= CONFIGURACIÓN FIJA =================
#define INTERVALO_GRABACION 1000 // 1 segundo fijo
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
  Serial.begin(9600);
  
  while (!Serial); // Espera a abrir el monitor serie
  delay(1000);

  if (!IMU.begin() || !HS300x.begin() || !BARO.begin()) {
    Serial.println(">>> ERROR: Sensores no encontrados <<<");
    while (1);
  }

  Serial.println("--- CANSAT MODO INTELIGENTE INICIADO ---");
  
  // Calibración inicial
  float suma = 0;
  for(int i=0; i<20; i++) { suma += calcularAltitud(); delay(50); }
  altitudBase = suma / 20.0;
  
  Serial.print("Altitud Suelo: "); Serial.println(altitudBase);
}

void loop() {
  float altActual = calcularAltitud();
  float altRelativa = altActual - altitudBase;

  // 1. MONITOR EN TIEMPO REAL (Para ver qué pasa antes de grabar)
  static unsigned long lastMonitor = 0;
  if (millis() - lastMonitor > 500) {
    if (!grabando) {
      Serial.print("ESPERANDO | Alt:"); Serial.print(altRelativa);
      Serial.print("m | Max:"); Serial.print(altitudMax);
      Serial.print(" | Bajando:"); Serial.println(altitudMax - altRelativa);
    } else {
      Serial.print(">>> GRABANDO | Registro: "); Serial.print(numRegistros);
      Serial.print("/"); Serial.println(MAX_REGISTROS);
    }
    lastMonitor = millis();
  }

  // 2. DETECTAR DESCENSO (LÓGICA AUTOMÁTICA ADAPTATIVA)
  if (!grabando && !aterrizado) {
    if (altRelativa > altitudMax) altitudMax = altRelativa;
    
    float bajada = altitudMax - altRelativa;
    float umbralDinamico;
    int ciclosNecesarios;

    // Si estamos en el aula subirá poco (< 5m). En vuelo subirá mucho.
    if (altitudMax < 5.0) {
      umbralDinamico = 0.35;   // Sensibilidad para aula
      ciclosNecesarios = 2;    
    } else {
      umbralDinamico = 2.0;    // Seguridad para vuelo real
      ciclosNecesarios = 5;    
    }

    if (bajada > umbralDinamico) {
      contadorDescenso++;
    } else {
      contadorDescenso = 0;
    }

    if (contadorDescenso >= ciclosNecesarios) {
      iniciarGrabacion();
    }
  }

  // 3. PROCESO DE GRABACIÓN
  if (grabando) {
    if (millis() - ultimaGrabacion >= INTERVALO_GRABACION) {
      ultimaGrabacion = millis();
      grabarRegistro(altRelativa);
    }
    detectarAterrizaje(altRelativa);
    digitalWrite(LED_BUILTIN, (millis() / 250) % 2); 
  }

  // 4. GESTIÓN DE COMANDOS
  if (Serial.available()) {
    String c = Serial.readStringUntil('\n');
    c.trim(); c.toUpperCase();
    
    if (c == "CSV") exportarCSV();
    
    if (c == "BORRAR") { 
      numRegistros = 0; 
      aterrizado = false; 
      altitudMax = -1000; 
      Serial.println(">>> MEMORIA RESETEADA <<<"); 
    }
    
    if (c == "GRABAR") {
      Serial.println(">>> INICIO MANUAL RECIBIDO <<<");
      iniciarGrabacion();
    }
  }
}

// --- FUNCIONES INTERNAS ---

float calcularAltitud() {
  float p = BARO.readPressure();
  return 44330.0 * (1.0 - pow(p / 1013.25, 0.1903));
}

void iniciarGrabacion() {
  if (!grabando) {
    Serial.println("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
    Serial.println(">>> ¡GRABACIÓN INICIADA! <<<");
    Serial.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
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
      Serial.println("\n>>> ATERRIZAJE DETECTADO. PARANDO REGISTRO. <<<");
    }
  } else {
    // Si hay movimiento significativo o altura, no es aterrizaje
  }
}

void grabarRegistro(float altRel) {
  if (numRegistros >= MAX_REGISTROS) {
    grabando = false;
    Serial.println("\n--- MEMORIA LLENA ---");
    return;
  }
  DatosSensor d;
  d.timestamp = millis() - tiempoInicio;
  d.altitud = altRel * 100; // cm
  d.temperatura = HS300x.readTemperature() * 100;
  d.humedad = HS300x.readHumidity() * 100;
  d.presion = BARO.readPressure();
  
  float x, y, z;
  IMU.readAcceleration(x, y, z);
  d.accX = x * 100; d.accY = y * 100; d.accZ = z * 100;

  registros[numRegistros++] = d;
}

void exportarCSV() {
  Serial.println("\nt_ms,temp,hum,pres,alt_cm,ax,ay,az");
  for (int i = 0; i < numRegistros; i++) {
    auto d = registros[i];
    Serial.print(d.timestamp); Serial.print(",");
    Serial.print(d.temperatura/100.0); Serial.print(",");
    Serial.print(d.humedad/100.0); Serial.print(",");
    Serial.print(d.presion); Serial.print(",");
    Serial.print(d.altitud); Serial.print(",");
    Serial.print(d.accX/100.0); Serial.print(",");
    Serial.print(d.accY/100.0); Serial.print(",");
    Serial.println(d.accZ/100.0);
  }
}
