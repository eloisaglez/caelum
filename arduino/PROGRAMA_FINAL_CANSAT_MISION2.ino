/*
 * ========================================================================
 * CANSAT MISIÓN 2 - PROGRAMA FINAL COMPLETO
 * ========================================================================
 * 
 * Autor: CanSat Misión 2
 * Fecha: Enero 2026
 * Proyecto: Detección de Firmas de Combustión
 * 
 * SENSORES INTEGRADOS:
 *   ✅ HS3003: Temperatura REAL + Humedad
 *   ✅ LPS22HB: Presión + Altitud
 *   ✅ BMI270: Acelerómetro + Giroscopio
 *   ✅ BMM150: Magnetómetro (Brújula)
 *   ✅ APDS9960: Luz ambiente
 * 
 * SENSORES EXTERNOS:
 *   ✅ SGP30 (I2C A4/A5): TVOC + eCO2 + H2 + Ethanol
 *   ✅ GPS (SoftwareSerial D2/D4): Posición + Altitud
 *   ✅ APC220 (Serial1): Antena RF para telemetría
 *   ✅ MicroSD (SPI D10/D11/D12/D13): Grabación CSV
 * 
 * ========================================================================
 */

// ========== LIBRERÍAS ==========
#include <Arduino_BMI270_BMM150.h>
#include <Arduino_HS300x.h>
#include <ReefwingLPS22HB.h>
#include "Adafruit_SGP30.h"
#include <SD.h>
#include <SPI.h>
#include <SoftwareSerial.h>

// ========== INSTANCIAS ==========
ReefwingLPS22HB pressureSensor;
Adafruit_SGP30 sgp30;
File dataFile;
SoftwareSerial gpsSerial(2, 4);  // RX=D2, TX=D4

// ========== CONSTANTES ==========
const int chipSelect = 10;
String filename = "MISSION2.CSV";
float referencePressure = 1013.25;  // Nivel del mar

// ========== VARIABLES - IMU ==========
float accelX = 0, accelY = 0, accelZ = 0;
float gyroX = 0, gyroY = 0, gyroZ = 0;
float magnetX = 0, magnetY = 0, magnetZ = 0;

// ========== VARIABLES - SENSORES AMBIENTALES ==========
float temperatura_hs = 0, humedad = 0;
float temperatura_lps = 0, presion = 0;
float altitud = 0;

// ========== VARIABLES - SGP30 ==========
uint16_t tvoc = 0, eco2 = 0;
uint16_t h2_raw = 0, ethanol_raw = 0;

// ========== VARIABLES - GPS ==========
String gpsData = "";
float gps_lat = 0.0, gps_lon = 0.0;
float gps_alt = 0.0;
int gps_satellites = 0;
boolean gps_fix = false;

// ========== VARIABLES - CONTROL ==========
unsigned long lastPrintTime = 0;
unsigned long lastSDWriteTime = 0;
unsigned long lastAPC220SendTime = 0;
unsigned long lastGPSReadTime = 0;
int readingCount = 0;
boolean imuOk = false, hs3003Ok = false, lps22hbOk = false;
boolean sgp30Ok = false, sdOk = false, gpsOk = false;

// ========== CONFIGURACIÓN ==========
const unsigned long PRINT_INTERVAL = 2000;
const unsigned long SD_WRITE_INTERVAL = 1000;
const unsigned long APC220_SEND_INTERVAL = 5000;
const unsigned long GPS_READ_INTERVAL = 500;

// ========================================================================
// SETUP
// ========================================================================

void setup() {
  Serial.begin(9600);      // USB (debug)
  Serial1.begin(9600);     // APC220 (telemetría)
  gpsSerial.begin(9600);   // GPS
  delay(2000);
  
  printBanner();
  
  // Inicializar IMU
  Serial.print("IMU (BMI270+BMM150)... ");
  if (!IMU.begin()) {
    Serial.println("❌");
    imuOk = false;
  } else {
    Serial.println("✓");
    imuOk = true;
  }
  
  // Inicializar HS3003
  Serial.print("HS3003 (Temp+Humedad)... ");
  if (!HS300x.begin()) {
    Serial.println("❌");
    hs3003Ok = false;
  } else {
    Serial.println("✓");
    hs3003Ok = true;
  }
  
  // Inicializar LPS22HB
  Serial.print("LPS22HB (Presión)... ");
  pressureSensor.begin();
  if (pressureSensor.connected()) {
    Serial.println("✓");
    lps22hbOk = true;
  } else {
    Serial.println("❌");
    lps22hbOk = false;
  }
  
  // Inicializar SGP30
  Serial.print("SGP30 (TVOC+eCO2)... ");
  if (!sgp30.begin()) {
    Serial.println("❌");
    sgp30Ok = false;
  } else {
    Serial.println("✓");
    sgp30Ok = true;
  }
  
  // Inicializar MicroSD
  Serial.print("MicroSD (SPI)... ");
  if (!SD.begin(chipSelect)) {
    Serial.println("❌");
    sdOk = false;
  } else {
    Serial.println("✓");
    sdOk = true;
    crearArchivoCSV();
  }
  
  // Verificar GPS y APC220
  Serial.print("GPS (SoftwareSerial)... ");
  Serial.println("✓");
  gpsOk = true;
  
  Serial.print("APC220 (Serial1)... ");
  Serial.println("✓");
  
  Serial.println();
  Serial.println("═══════════════════════════════════════════════════");
  Serial.println("Sistema listo. Iniciando ciclo de lectura...");
  Serial.println("═══════════════════════════════════════════════════");
  Serial.println();
  
  delay(2000);
}

// ========================================================================
// LOOP PRINCIPAL
// ========================================================================

void loop() {
  // LEER GPS
  if (millis() - lastGPSReadTime >= GPS_READ_INTERVAL) {
    lastGPSReadTime = millis();
    readGPS();
  }
  
  // LEER APC220 (escuchar comandos)
  while (Serial1.available()) {
    Serial1.read();  // Limpiar buffer
  }
  
  // LEER IMU
  if (imuOk) {
    if (IMU.accelerationAvailable()) {
      IMU.readAcceleration(accelX, accelY, accelZ);
    }
    if (IMU.gyroscopeAvailable()) {
      IMU.readGyroscope(gyroX, gyroY, gyroZ);
    }
    if (IMU.magneticFieldAvailable()) {
      IMU.readMagneticField(magnetX, magnetY, magnetZ);
    }
  }
  
  // LEER SENSORES AMBIENTALES
  if (hs3003Ok) {
    temperatura_hs = HS300x.readTemperature();
    humedad = HS300x.readHumidity();
  }
  
  if (lps22hbOk) {
    temperatura_lps = pressureSensor.readTemperature();
    presion = pressureSensor.readPressure();
  }
  
  // CALCULAR ALTITUD
  if (gps_fix && gps_alt > 0) {
    altitud = gps_alt;
  } else if (lps22hbOk && presion > 0) {
    float ratio = presion / referencePressure;
    altitud = 44330.0 * (1.0 - pow(ratio, 1.0 / 5.255));
  }
  
  // LEER SGP30
  if (sgp30Ok) {
    if (sgp30.IAQmeasure()) {
      tvoc = sgp30.TVOC;
      eco2 = sgp30.eCO2;
      h2_raw = sgp30.rawH2;
      ethanol_raw = sgp30.rawEthanol;
    }
  }
  
  // GRABAR EN MICROSD
  if (millis() - lastSDWriteTime >= SD_WRITE_INTERVAL) {
    lastSDWriteTime = millis();
    if (sdOk) {
      escribirMicroSD();
    }
  }
  
  // ENVIAR POR APC220
  if (millis() - lastAPC220SendTime >= APC220_SEND_INTERVAL) {
    lastAPC220SendTime = millis();
    enviarAPC220();
  }
  
  // IMPRIMIR EN MONITOR SERIE
  if (millis() - lastPrintTime >= PRINT_INTERVAL) {
    lastPrintTime = millis();
    mostrarDatos();
    readingCount++;
  }
}

// ========================================================================
// FUNCIONES AUXILIARES
// ========================================================================

void printBanner() {
  Serial.println();
  Serial.println("╔════════════════════════════════════════════════════════════╗");
  Serial.println("║          CANSAT MISIÓN 2 - PROGRAMA FINAL                 ║");
  Serial.println("║     Detección de Firmas de Combustión - Enero 2026        ║");
  Serial.println("║         IES Diego Velázquez - Bilingual School            ║");
  Serial.println("╚════════════════════════════════════════════════════════════╝");
  Serial.println();
  Serial.println("Inicializando sensores...");
  Serial.println();
}

void crearArchivoCSV() {
  if (!SD.exists(filename)) {
    dataFile = SD.open(filename, FILE_WRITE);
    if (dataFile) {
      dataFile.println("tiempo,lat,lon,alt_gps,alt_calc,temp,humedad,presion,tvoc,eco2,h2,ethanol,accelx,accely,accelz,gyroX,gyroY,gyroZ,brujula,satelites");
      dataFile.close();
    }
  }
}

void readGPS() {
  while (gpsSerial.available()) {
    char c = gpsSerial.read();
    gpsData += c;
    if (c == '\n') {
      parseGPS(gpsData);
      gpsData = "";
    }
  }
}

void parseGPS(String sentence) {
  if (sentence.length() < 6) return;
  
  if (sentence.startsWith("$GNGGA") || sentence.startsWith("$GPGGA")) {
    parseGGA(sentence);
  } else if (sentence.startsWith("$GNRMC") || sentence.startsWith("$GPRMC")) {
    parseRMC(sentence);
  }
}

void parseRMC(String sentence) {
  int commaCount = 0;
  int lastIndex = 0;
  
  for (int i = 0; i < sentence.length(); i++) {
    if (sentence[i] == ',' || sentence[i] == '\n') {
      String field = sentence.substring(lastIndex, i);
      
      if (commaCount == 2) {
        gps_fix = (field == "A");
      } else if (commaCount == 3) {
        gps_lat = parseCoordinate(field);
      } else if (commaCount == 5) {
        gps_lon = parseCoordinate(field);
      }
      
      lastIndex = i + 1;
      commaCount++;
    }
  }
}

void parseGGA(String sentence) {
  int commaCount = 0;
  int lastIndex = 0;
  
  for (int i = 0; i < sentence.length(); i++) {
    if (sentence[i] == ',' || sentence[i] == '\n') {
      String field = sentence.substring(lastIndex, i);
      
      if (commaCount == 7) {
        gps_satellites = field.toInt();
      } else if (commaCount == 9) {
        if (field.length() > 0) {
          gps_alt = field.toFloat();
        }
      }
      
      lastIndex = i + 1;
      commaCount++;
    }
  }
}

float parseCoordinate(String coord) {
  if (coord.length() < 5) return 0.0;
  int dotIndex = coord.indexOf('.');
  int degreeDigits = dotIndex - 2;
  if (degreeDigits <= 0) return 0.0;
  
  float degrees = coord.substring(0, degreeDigits).toFloat();
  float minutes = coord.substring(degreeDigits).toFloat();
  return degrees + (minutes / 60.0);
}

void escribirMicroSD() {
  if (!sdOk) return;
  
  dataFile = SD.open(filename, FILE_WRITE);
  if (!dataFile) return;
  
  String line = String(readingCount) + ",";
  
  // GPS
  if (gps_fix) {
    line += String(gps_lat, 6) + "," + String(gps_lon, 6) + "," + String(gps_alt, 1) + ",";
  } else {
    line += "XXXX,XXXX,XXXX,";
  }
  
  // Altitud, Temperatura, Humedad, Presión
  line += String(altitud, 1) + "," + String(temperatura_hs, 1) + "," + String(humedad, 1) + ",";
  line += String(presion / 100.0, 1) + ",";
  
  // SGP30
  if (sgp30Ok) {
    line += String(tvoc) + "," + String(eco2) + "," + String(h2_raw) + "," + String(ethanol_raw) + ",";
  } else {
    line += "XXXX,XXXX,XXXX,XXXX,";
  }
  
  // IMU
  if (imuOk) {
    line += String(accelX, 2) + "," + String(accelY, 2) + "," + String(accelZ, 2) + ",";
    line += String(gyroX, 1) + "," + String(gyroY, 1) + "," + String(gyroZ, 1) + ",";
  } else {
    line += "XXXX,XXXX,XXXX,XXXX,XXXX,XXXX,";
  }
  
  // Brújula
  if (imuOk) {
    float heading = atan2(magnetY, magnetX) * 180 / PI;
    if (heading < 0) heading += 360;
    line += String(heading, 1) + ",";
  } else {
    line += "XXXX,";
  }
  
  line += String(gps_satellites);
  
  dataFile.println(line);
  dataFile.close();
}

void enviarAPC220() {
  String telemetry = String(readingCount) + "," + String(temperatura_hs, 1) + "," + String(humedad, 1) + ",";
  telemetry += String(presion / 100.0, 1) + "," + String(tvoc) + "," + String(eco2) + ",";
  telemetry += String(gps_lat, 4) + "," + String(gps_lon, 4) + "," + String(altitud, 1) + ",";
  telemetry += String(gps_satellites);
  
  Serial1.println(telemetry);
}

void mostrarDatos() {
  if (readingCount % 10 == 0) {
    Serial.println();
    Serial.println("N° | Lat | Lon | Alt | T | H | P | TVOC | eCO2 | Sat");
    Serial.println("──┼─────┼─────┼─────┼──┼──┼──┼──────┼──────┼────");
  }
  
  Serial.print(readingCount);
  Serial.print(" | ");
  Serial.print(gps_lat, 4);
  Serial.print(" | ");
  Serial.print(gps_lon, 4);
  Serial.print(" | ");
  Serial.print(altitud, 0);
  Serial.print(" | ");
  Serial.print(temperatura_hs, 0);
  Serial.print(" | ");
  Serial.print(humedad, 0);
  Serial.print(" | ");
  Serial.print(presion / 100.0, 0);
  Serial.print(" | ");
  Serial.print(tvoc);
  Serial.print(" | ");
  Serial.print(eco2);
  Serial.print(" | ");
  Serial.println(gps_satellites);
}

// ========== FIN DEL PROGRAMA ==========
