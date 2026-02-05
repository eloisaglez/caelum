/*
 * ============================================
 * CANSAT MISIÓN 2 - VERSIÓN FINAL "DEBUG"
 * Arduino Nano 33 BLE Sense Rev2
 * ============================================
 * * GUÍA RÁPIDA DE COMANDOS (Escribir en Monitor Serie y pulsar Enter):
 * -------------------------------------------------------------------
 * "GRABAR" -> Fuerza el inicio de grabación (ideal para pruebas en mesa).
 * "PARAR"  -> Detiene la grabación manualmente.
 * "CSV"    -> Descarga todos los datos guardados (para Excel).
 * "BORRAR" -> Borra la memoria RAM para empezar de cero.
 * "ESTADO" -> Te dice cuántos datos llevas y si el GPS tiene señal.
 * -------------------------------------------------------------------
 * * CONEXIONES FÍSICAS:
 * 1. GPS (BN-220): 
 * - TX del GPS -> Pin 0 (RX) del Arduino
 * - RX del GPS -> Pin 1 (TX) del Arduino
 * * 2. RADIO (APC220): 
 * - TXD de la Radio -> Pin 2 del Arduino
 * - RXD de la Radio -> Pin 3 del Arduino
 * * 3. Sensor Gases (SGP30): Pines A4 (SDA) y A5 (SCL)
 */

#include <Wire.h>
// LIBRERÍAS (Instalar desde Gestor de Librerías):
#include <Arduino_LPS22HB.h>        // Presión (Oficial Arduino)
#include <Arduino_HS300x.h>         // Temp/Humedad (Oficial Arduino)
#include <Arduino_BMI270_BMM150.h>  // Acelerómetro (Oficial Arduino)
#include <Adafruit_SGP30.h>         // Gases
#include <TinyGPS++.h>              // GPS

// ============================================
// 1. CONFIGURACIÓN DE PUERTOS
// ============================================
// Radio APC220 en pines 2 (RX) y 3 (TX)
UART ApcSerial(3, 2); 

// El GPS usa Serial1 (Pines 0 y 1) automáticamente

// ============================================
// 2. PARÁMETROS DE VUELO
// ============================================
#define NOMBRE_EQUIPO "CAELUM"
#define UMBRAL_ALTITUD 30.0   // Metros para activar grabación automática
#define MAX_REGISTROS 500     // Capacidad de memoria
#define INTERVALO_GRABACION 1000   // 1 segundo
#define INTERVALO_TELEMETRIA 1000  // 1 segundo

// ============================================
// 3. VARIABLES Y OBJETOS
// ============================================
TinyGPSPlus gps;
Adafruit_SGP30 sgp;

struct DatosSensor {
  uint32_t timestamp;
  int16_t temperatura; int16_t humedad; int16_t presion; int16_t altitud;
  uint16_t tvoc; uint16_t eco2; uint16_t h2; uint16_t ethanol;
  int32_t latitud; int32_t longitud; int16_t altitudGPS; uint8_t satelites;
  int16_t accX, accY, accZ; int16_t gyrX, gyrY, gyrZ;
};

DatosSensor registros[MAX_REGISTROS];
int numRegistros = 0;
bool grabando = false;
unsigned long tiempoInicioGrabacion = 0;
unsigned long ultimaGrabacion = 0;
unsigned long ultimaTelemetria = 0;
uint32_t numeroPaquete = 0;

float altitudInicial = 0, altitudActual = 0;
float temp = 0, hum = 0, pres = 0;
uint16_t tvoc = 0, eco2 = 0, h2 = 0, ethanol = 0;
float lat = 0, lon = 0, altGPS = 0;
int sats = 0;
float accX = 0, accY = 0, accZ = 0;
float gyrX = 0, gyrY = 0, gyrZ = 0;

// ============================================
// SETUP (SE EJECUTA UNA VEZ)
// ============================================
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH); // LED encendido mientras inicia
  
  Serial.begin(115200);  // USB Rápido
  ApcSerial.begin(9600); // Radio
  Serial1.begin(9600);   // GPS
  
  delay(2000); // Tiempo para abrir monitor

  Serial.println("\n=== INICIANDO SISTEMA CANSAT ===");
  
  // Iniciar Sensores
  if (!BARO.begin()) Serial.println("[FALLO] Sensor Presion"); else Serial.println("[OK] Presion");
  if (!HS300x.begin()) Serial.println("[FALLO] Temp/Hum"); else Serial.println("[OK] Temp/Hum");
  if (!IMU.begin()) Serial.println("[FALLO] IMU"); else Serial.println("[OK] Acelerometro");
  if (!sgp.begin()) Serial.println("[FALLO] SGP30 Gases"); else Serial.println("[OK] SGP30 Gases");

  // Calibrar Altura Base
  Serial.print("Calibrando altura (NO MOVER)... ");
  float suma = 0;
  for (int i = 0; i < 20; i++) {
    suma += calcularAltitud(BARO.readPressure() * 10); 
    delay(50);
  }
  altitudInicial = suma / 20.0;
  Serial.println("HECHO.");

  Serial.println("\n------------------------------------------------");
  Serial.println(" COMANDOS DISPONIBLES (Escribelos arriba y pulsa Enter):");
  Serial.println("  -> GRABAR  (Empieza a guardar ya)");
  Serial.println("  -> PARAR   (Deja de guardar)");
  Serial.println("  -> CSV     (Ver datos guardados)");
  Serial.println("  -> BORRAR  (Limpiar memoria)");
  Serial.println("------------------------------------------------\n");
  
  digitalWrite(LED_BUILTIN, LOW); // LED apagado = Listo
}

// ============================================
// LOOP (SE REPITE CONSTANTEMENTE)
// ============================================
void loop() {
  unsigned long ahora = millis();

  // 1. LEER COMANDOS USB (Si tú escribes algo)
  if (Serial.available()) {
    String comando = Serial.readStringUntil('\n');
    comando.trim(); comando.toUpperCase();
    procesarComando(comando);
  }
  
  // 2. LEER GPS (Siempre activo)
  while (Serial1.available() > 0) gps.encode(Serial1.read());
  
  // 3. LEER SENSORES
  leerSensores();
  altitudActual = calcularAltitud(pres);

  // 4. LÓGICA DE GRABACIÓN
  if (!grabando) {
    // MODO ESPERA (LED parpadea lento)
    digitalWrite(LED_BUILTIN, (ahora / 1000) % 2);
    
    // Auto-activación si sube 30m
    if (altitudActual > altitudInicial + UMBRAL_ALTITUD) iniciarGrabacion();
    
  } else {
    // MODO GRABANDO (LED parpadea muy rápido)
    digitalWrite(LED_BUILTIN, (ahora / 100) % 2);
    
    if (ahora - ultimaGrabacion >= INTERVALO_GRABACION) {
      ultimaGrabacion = ahora;
      grabarRegistro();
    }
    
    // Parada automática si memoria llena
    if (numRegistros >= MAX_REGISTROS) {
      grabando = false; 
      Serial.println(">>> MEMORIA LLENA <<<");
    }
  }
  
  // 5. ENVIAR TELEMETRÍA (Radio + Pantalla)
  if (ahora - ultimaTelemetria >= INTERVALO_TELEMETRIA) {
    ultimaTelemetria = ahora;
    enviarTelemetria();
  }
}

// ============================================
// FUNCIONES DE CONTROL
// ============================================

void leerSensores() {
  temp = HS300x.readTemperature();
  hum = HS300x.readHumidity();
  pres = BARO.readPressure() * 10; // Convertir kPa a hPa
  
  if (IMU.accelerationAvailable()) IMU.readAcceleration(accX, accY, accZ);
  if (IMU.gyroscopeAvailable()) IMU.readGyroscope(gyrX, gyrY, gyrZ);
  
  if (sgp.IAQmeasure()) { tvoc = sgp.TVOC; eco2 = sgp.eCO2; }
  
  if (gps.location.isValid()) { lat = gps.location.lat(); lon = gps.location.lng(); }
  if (gps.altitude.isValid()) altGPS = gps.altitude.meters();
  if (gps.satellites.isValid()) sats = gps.satellites.value();
}

void enviarTelemetria() {
  numeroPaquete++;
  unsigned long t = grabando ? (millis() - tiempoInicioGrabacion) : millis();
  
  // --- A. ENVIAR A RADIO APC220 (Datos CSV crudos para Tierra) ---
  ApcSerial.print(NOMBRE_EQUIPO); ApcSerial.print(",");
  ApcSerial.print(numeroPaquete); ApcSerial.print(",");
  ApcSerial.print(t); ApcSerial.print(",");
  ApcSerial.print(lat, 6); ApcSerial.print(",");
  ApcSerial.print(lon, 6); ApcSerial.print(",");
  ApcSerial.print(altGPS, 1); ApcSerial.print(",");
  ApcSerial.print(sats); ApcSerial.print(",");
  ApcSerial.print(temp, 2); ApcSerial.print(",");
  ApcSerial.print(hum, 2); ApcSerial.print(",");
  ApcSerial.print(pres, 2); ApcSerial.print(",");
  ApcSerial.print(altitudActual, 1); ApcSerial.print(",");
  ApcSerial.print(tvoc); ApcSerial.print(",");
  ApcSerial.println(eco2);

  // --- B. ENVIAR A PANTALLA USB (Datos legibles para ti) ---
  Serial.print("DATOS > ");
  Serial.print("Alt: "); Serial.print(altitudActual, 1); Serial.print("m | ");
  Serial.print("Temp: "); Serial.print(temp, 1); Serial.print("C | ");
  Serial.print("Pres: "); Serial.print(pres, 0); Serial.print("hPa | ");
  Serial.print("Gases: "); Serial.print(tvoc); Serial.print("ppb | ");
  
  Serial.print("GPS: "); 
  if (sats > 0) {
      Serial.print("OK ("); Serial.print(sats); Serial.print(" sats)");
  } else {
      Serial.print("BUSCANDO...");
  }
  
  if (grabando) Serial.print(" [GRABANDO RAM]");
  Serial.println(); // Salto de línea
}

void iniciarGrabacion() {
  grabando = true;
  tiempoInicioGrabacion = millis();
  ultimaGrabacion = tiempoInicioGrabacion;
  Serial.println("\n>>> GRABACION INICIADA (LED RAPIDO) <<<\n");
}

void grabarRegistro() {
  if (numRegistros >= MAX_REGISTROS) return;
  DatosSensor d;
  d.timestamp = millis() - tiempoInicioGrabacion;
  d.temperatura = (int16_t)(temp * 100);
  d.humedad = (int16_t)(hum * 100);
  d.presion = (int16_t)(pres * 10 - 9000); 
  d.altitud = (int16_t)altitudActual;
  d.tvoc = tvoc; d.eco2 = eco2;
  d.latitud = (int32_t)(lat * 1000000); d.longitud = (int32_t)(lon * 1000000);
  d.altitudGPS = (int16_t)altGPS; d.satelites = sats;
  d.accX = (int16_t)(accX * 100); d.accY = (int16_t)(accY * 100); d.accZ = (int16_t)(accZ * 100);
  registros[numRegistros] = d;
  numRegistros++;
}

float calcularAltitud(float presion) {
  return 44330.0 * (1.0 - pow(presion / 1013.25, 0.1903));
}

// ============================================
// GESTIÓN DE COMANDOS
// ============================================
void procesarComando(String comando) {
  if (comando == "CSV") {
    exportarCSV();
  } else if (comando == "GRABAR") {
    iniciarGrabacion();
  } else if (comando == "PARAR") {
    grabando = false;
    Serial.println("\n>>> GRABACION DETENIDA MANUALMENTE <<<");
  } else if (comando == "BORRAR") {
    numRegistros = 0;
    Serial.println("\n>>> MEMORIA RAM BORRADA <<<");
  } else if (comando == "ESTADO") {
    Serial.print("Registros usados: "); Serial.print(numRegistros);
    Serial.print(" de "); Serial.println(MAX_REGISTROS);
  }
}

void exportarCSV() {
  if (numRegistros == 0) { Serial.println("MEMORIA VACIA. Usa 'GRABAR' primero."); return; }
  Serial.println("\n=== COPIAR DESDE AQUI ===");
  Serial.println("equipo,paquete,timestamp,lat,lon,altGPS,sats,temp,hum,pres,altBaro,tvoc,eco2,accX,accY,accZ");
  for (int i = 0; i < numRegistros; i++) {
    DatosSensor d = registros[i];
    Serial.print(NOMBRE_EQUIPO); Serial.print(",");
    Serial.print(i + 1); Serial.print(",");
    Serial.print(d.timestamp); Serial.print(",");
    Serial.print(d.latitud/1000000.0,6); Serial.print(",");
    Serial.print(d.longitud/1000000.0,6); Serial.print(",");
    Serial.print(d.altitudGPS); Serial.print(",");
    Serial.print(d.satelites); Serial.print(",");
    Serial.print(d.temperatura/100.0,2); Serial.print(",");
    Serial.print(d.humedad/100.0,2); Serial.print(",");
    Serial.print((d.presion+9000)/10.0,2); Serial.print(",");
    Serial.print(d.altitud); Serial.print(",");
    Serial.print(d.tvoc); Serial.print(",");
    Serial.print(d.eco2); Serial.print(",");
    Serial.print(d.accX/100.0,2); Serial.print(",");
    Serial.print(d.accY/100.0,2); Serial.println(d.accZ/100.0,2);
    delay(20);
  }
  Serial.println("=== FIN DE DATOS ===\n");
}
