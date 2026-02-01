/*
 * ========================================
 * CANSAT - MISIÓN 2: FIRMAS DE COMBUSTIÓN
 * ========================================
 * 
 * Detección georreferenciada de compuestos volátiles (TVOC/eCO2)
 * con SGP30 + GPS + tarjeta SD
 * 
 * Hardware requerido:
 * - Arduino Nano/Uno
 * - Sensor SGP30 (I2C: SDA=A4, SCL=A5)
 * - Módulo GPS (Serial: TX=D3, RX=D4)
 * - Módulo microSD (SPI: CS=D10, MOSI=D11, MISO=D12, SCK=D13)
 * - LED indicador (D8)
 * 
 * Autor: IES Diego Velázquez - Dpto. Tecnología
 * Fecha: Enero 2026
 */

#include <Wire.h>
#include <Adafruit_SGP30.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <SD.h>
#include <SPI.h>

// ============ CONFIGURACIÓN DE PINES ============
#define GPS_RX_PIN 4
#define GPS_TX_PIN 3
#define SD_CS_PIN 10
#define LED_PIN 8

// ============ OBJETOS ============
Adafruit_SGP30 sgp;
TinyGPSPlus gps;
SoftwareSerial gpsSerial(GPS_RX_PIN, GPS_TX_PIN);

// ============ VARIABLES GLOBALES ============
File dataFile;
unsigned long lastSampleTime = 0;
const unsigned long SAMPLE_INTERVAL = 5000;  // Muestreo cada 5 segundos
unsigned int sampleCount = 0;
bool sdAvailable = false;

// Baseline del sensor (se calibra automáticamente)
uint16_t TVOC_base, eCO2_base;

// ============ CONFIGURACIÓN INICIAL ============
void setup() {
  Serial.begin(115200);
  gpsSerial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  
  Serial.println(F("================================="));
  Serial.println(F("  CANSAT MISIÓN 2 - INICIANDO"));
  Serial.println(F("  Firmas de Combustión"));
  Serial.println(F("=================================\n"));
  
  // Inicializar SGP30
  if (!sgp.begin()) {
    Serial.println(F("❌ Error: SGP30 no detectado"));
    blinkError();
    while (1);
  }
  
  Serial.print(F("✓ SGP30 detectado - Serial: 0x"));
  Serial.println(sgp.serialnumber[0], HEX);
  
  // Inicializar tarjeta SD
  if (!SD.begin(SD_CS_PIN)) {
    Serial.println(F("⚠️  SD no disponible - datos solo por Serial"));
    sdAvailable = false;
  } else {
    Serial.println(F("✓ Tarjeta SD inicializada"));
    sdAvailable = true;
    
    // Crear archivo con encabezado
    dataFile = SD.open("mission2.csv", FILE_WRITE);
    if (dataFile) {
      dataFile.println(F("timestamp,lat,lon,alt,sats,tvoc,eco2,h2,ethanol"));
      dataFile.close();
      Serial.println(F("✓ Archivo mission2.csv creado"));
    }
  }
  
  Serial.println(F("\n🔧 Calibrando sensor SGP30..."));
  Serial.println(F("   (15 segundos de estabilización)\n"));
  
  // Calibración inicial (15 segundos)
  for (int i = 0; i < 15; i++) {
    sgp.IAQmeasure();
    delay(1000);
    Serial.print(F("."));
  }
  Serial.println(F("\n✓ Calibración completada\n"));
  
  // Obtener baseline
  sgp.getIAQBaseline(&eCO2_base, &TVOC_base);
  Serial.print(F("📊 Baseline - TVOC: "));
  Serial.print(TVOC_base, HEX);
  Serial.print(F(" | eCO2: "));
  Serial.println(eCO2_base, HEX);
  
  Serial.println(F("\n🚀 SISTEMA LISTO - Iniciando monitoreo\n"));
  digitalWrite(LED_PIN, HIGH);
  delay(500);
  digitalWrite(LED_PIN, LOW);
}

// ============ BUCLE PRINCIPAL ============
void loop() {
  // Leer datos GPS continuamente
  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
  }
  
  // Tomar muestra cada SAMPLE_INTERVAL
  if (millis() - lastSampleTime >= SAMPLE_INTERVAL) {
    lastSampleTime = millis();
    takeSample();
  }
  
  // Actualizar baseline cada 30 minutos (recomendado)
  static unsigned long lastBaselineUpdate = 0;
  if (millis() - lastBaselineUpdate >= 1800000) {  // 30 min
    sgp.getIAQBaseline(&eCO2_base, &TVOC_base);
    lastBaselineUpdate = millis();
  }
}

// ============ FUNCIÓN DE MUESTREO ============
void takeSample() {
  sampleCount++;
  digitalWrite(LED_PIN, HIGH);
  
  // Leer SGP30
  if (!sgp.IAQmeasure()) {
    Serial.println(F("❌ Error leyendo SGP30"));
    digitalWrite(LED_PIN, LOW);
    return;
  }
  
  // Obtener datos del sensor
  uint16_t tvoc = sgp.TVOC;
  uint16_t eco2 = sgp.eCO2;
  
  // Leer señales raw (para análisis avanzado)
  if (!sgp.IAQmeasureRaw()) {
    Serial.println(F("❌ Error leyendo señales raw"));
  }
  uint16_t raw_h2 = sgp.rawH2;
  uint16_t raw_ethanol = sgp.rawEthanol;
  
  // Datos GPS
  float latitude = 0.0;
  float longitude = 0.0;
  float altitude = 0.0;
  int satellites = 0;
  
  if (gps.location.isValid()) {
    latitude = gps.location.lat();
    longitude = gps.location.lng();
    altitude = gps.altitude.meters();
    satellites = gps.satellites.value();
  }
  
  // ============ MOSTRAR EN SERIAL ============
  Serial.print(F("📍 Muestra #"));
  Serial.print(sampleCount);
  Serial.print(F(" | "));
  Serial.print(millis() / 1000);
  Serial.println(F("s"));
  
  Serial.print(F("  GPS: "));
  if (gps.location.isValid()) {
    Serial.print(latitude, 6);
    Serial.print(F(", "));
    Serial.print(longitude, 6);
    Serial.print(F(" | Alt: "));
    Serial.print(altitude, 1);
    Serial.print(F("m | Sats: "));
    Serial.println(satellites);
  } else {
    Serial.println(F("❌ Sin señal GPS"));
  }
  
  Serial.print(F("  🌫️  TVOC: "));
  Serial.print(tvoc);
  Serial.print(F(" ppb | eCO2: "));
  Serial.print(eco2);
  Serial.println(F(" ppm"));
  
  // Clasificación de calidad del aire
  Serial.print(F("  "));
  if (tvoc < 220) {
    Serial.println(F("🟢 Calidad: EXCELENTE"));
  } else if (tvoc < 660) {
    Serial.println(F("🟡 Calidad: BUENA"));
  } else if (tvoc < 2200) {
    Serial.println(F("🟠 Calidad: MODERADA"));
  } else if (tvoc < 5500) {
    Serial.println(F("🔴 Calidad: MALA"));
  } else {
    Serial.println(F("🔴 Calidad: MUY MALA - PELIGROSA"));
  }
  
  Serial.print(F("  Raw - H2: "));
  Serial.print(raw_h2);
  Serial.print(F(" | Ethanol: "));
  Serial.println(raw_ethanol);
  Serial.println();
  
  // ============ GUARDAR EN SD ============
  if (sdAvailable) {
    dataFile = SD.open("mission2.csv", FILE_WRITE);
    if (dataFile) {
      // timestamp,lat,lon,alt,sats,tvoc,eco2,h2,ethanol
      dataFile.print(millis() / 1000);
      dataFile.print(F(","));
      dataFile.print(latitude, 6);
      dataFile.print(F(","));
      dataFile.print(longitude, 6);
      dataFile.print(F(","));
      dataFile.print(altitude, 1);
      dataFile.print(F(","));
      dataFile.print(satellites);
      dataFile.print(F(","));
      dataFile.print(tvoc);
      dataFile.print(F(","));
      dataFile.print(eco2);
      dataFile.print(F(","));
      dataFile.print(raw_h2);
      dataFile.print(F(","));
      dataFile.println(raw_ethanol);
      dataFile.close();
    }
  }
  
  digitalWrite(LED_PIN, LOW);
}

// ============ FUNCIÓN DE ERROR ============
void blinkError() {
  while (1) {
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_PIN, LOW);
    delay(200);
  }
}

/*
 * ============================================
 * NOTAS DE OPERACIÓN:
 * ============================================
 * 
 * 1. CALIBRACIÓN:
 *    - El SGP30 necesita 15 segundos de calentamiento
 *    - El baseline se actualiza automáticamente cada 30 min
 * 
 * 2. CLASIFICACIÓN TVOC (según EPA):
 *    - 0-220 ppb: Excelente (aire limpio)
 *    - 220-660 ppb: Buena (aceptable)
 *    - 660-2200 ppb: Moderada (ventilación recomendada)
 *    - 2200-5500 ppb: Mala (fuente de contaminación cercana)
 *    - >5500 ppb: Muy mala (peligroso, evacuación necesaria)
 * 
 * 3. FIRMAS DE COMBUSTIÓN DETECTABLES:
 *    - Tráfico vehicular: TVOC 300-800 ppb, eCO2 elevado
 *    - Generadores diésel: TVOC >1000 ppb, H2 alto
 *    - Cocinas/barbacoas: TVOC >500 ppb, Ethanol alto
 * 
 * 4. FORMATO DE SALIDA SD:
 *    mission2.csv: timestamp,lat,lon,alt,sats,tvoc,eco2,h2,ethanol
 * 
 * 5. ANÁLISIS POST-VUELO:
 *    - Usar script Python para generar mapas de calor
 *    - Correlacionar picos de TVOC con ubicaciones GPS
 *    - Identificar fuentes de contaminación
 */
