// =============================================================
//  CANSAT — PROGRAMA DE VUELO INTEGRADO
//  Hardware : Arduino Nano 33 BLE Sense Rev2
//  Módulo SD: Adafruit MicroSD SPI or SDIO Card Breakout Board
//  Archivo  : CANSAT_VUELO_INTEGRADO.ino
//  Proyecto : CanSat — Equipo Caelum
//  Fecha    : 2026
// =============================================================
//
//  MISIÓN: Detección de firmas de combustión y análisis de capas
//          atmosféricas mediante perfiles verticales de PM2.5
//
//  OBJETIVOS CIENTÍFICOS:
//    1. Perfil vertical de PM1.0, PM2.5, PM10 (identificar capas de
//       acumulación e inversiones térmicas: alt↑ + temp↑ + PM2.5↑)
//    2. CO2 como indicador de ESTABILIDAD ATMOSFÉRICA:
//       CO2 constante con altitud → atmósfera bien mezclada (normal)
//       CO2 variable con altitud  → capas diferenciadas o fuentes locales
//    3. Validación cruzada T+HR: comparación entre HS300x y SCD40
//       (ambos miden T y HR de forma independiente → detectar errores)
//
//  SENSORES INTEGRADOS:
//    BMI270  — Acelerómetro + Giroscopio
//    BMM150  — Magnetómetro
//    LPS22HB — Presión + Temperatura + Altitud  (librería Reefwing)
//    HS300x  — Temperatura + Humedad (sensor principal T+HR)
//
//  SENSORES EXTERNOS:
//    SCD40   — CO2 + Temperatura + Humedad (I2C) — validación cruzada T+HR
//    HM3301  — PM1.0, PM2.5, PM10 (I2C, directo Wire) — perfil vertical
//    GPS     — Latitud, Longitud, Altitud GPS, Satélites (Serial1, pins 0/1)
//
//  ALMACENAMIENTO:
//    MicroSD — CSV continuo (SdFat, SPI pins 10-13)
//
//  ESTRUCTURA CSV GENERADA (25 columnas):
//    timestamp, datetime, lat, lon, alt, alt_mar, sats,
//    temp_hs, hum_hs, temp_scd, hum_scd, temp_lps, presion,
//    co2, pm1_0, pm2_5, pm10,
//    accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, fase
//
//    temp_hs  / hum_hs  → HS300x   (integrado, sensor principal T+HR)
//    temp_scd / hum_scd → SCD40    (externo, validación cruzada T+HR)
//    temp_lps           → LPS22HB  (integrado, tercera lectura de T)
//    co2                → SCD40    (estabilidad atmosférica, NO calidad de aire)
//
//  FASES DE VUELO (detección automática):
//    espera      → En tierra, antes del lanzamiento
//    caida_libre → Descenso rápido (accel_z alejada de ~1g tras lanzamiento)
//    apertura    → Transición paracaídas (pico accel_z)
//    descenso    → Bajada suave con paracaídas
//    tierra      → Aterrizaje detectado
//
//  LIBRERÍAS NECESARIAS (Library Manager):
//    SdFat                  — Bill Greiman (Adafruit Fork)
//    Arduino_BMI270_BMM150  — oficial Arduino
//    ReefwingLPS22HB        — Reefwing Software
//    Arduino_HS300x         — oficial Arduino
//    SensirionI2cScd4x      — Sensirion
// =============================================================

#include "SdFat.h"
#include <Arduino_BMI270_BMM150.h>
#include <ReefwingLPS22HB.h>
#include <Arduino_HS300x.h>
#include <SensirionI2cScd4x.h>
#include <Wire.h>

// ---------------------------------------------------------------
//  PINES
// ---------------------------------------------------------------
#define SD_CS_PIN   10           // MicroSD Chip Select
#define SPI_SPEED   SD_SCK_MHZ(4)
#define GPS_PORT    Serial1      // GPS en pins 0 (RX) y 1 (TX)
#define HM3301_ADDR 0x40         // Dirección I2C del HM3301

// ---------------------------------------------------------------
//  CONFIGURACIÓN DE VUELO
//  !! Actualizar SEA_LEVEL_PRESSURE con dato real de AEMET !!
// ---------------------------------------------------------------
#define INTERVALO_MS        1000   // Muestra cada 1 segundo
#define UMBRAL_LANZAMIENTO  2.5    // m de ascenso para detectar despegue
#define UMBRAL_TIERRA       1.0    // m/s de cambio de altitud para detectar tierra
#define ACCEL_CAIDA_LIBRE   50.0   // accel_z por debajo de este valor = caída libre (mG)
#define ACCEL_APERTURA      150.0  // accel_z por encima = apertura paracaídas (mG)

float SEA_LEVEL_PRESSURE = 1013.25;  // hPa — presión nivel del mar del día (AEMET)

// ---------------------------------------------------------------
//  OBJETOS
// ---------------------------------------------------------------
SdFat              sd;
SdFile             dataFile;
ReefwingLPS22HB    LPS22HB;
SensirionI2cScd4x  scd4x;

// ---------------------------------------------------------------
//  VARIABLES DE ESTADO
// ---------------------------------------------------------------
const char FILENAME[] = "datos_SD.csv";

// Estado sensores
bool imuOK  = false;
bool lpsOK  = false;
bool hs3OK  = false;
bool scdOK  = false;
bool hm3OK  = false;
bool gpsOK  = false;
bool sdOK   = false;

// Altitud
float presionReferencia = 0.0;   // hPa al arrancar (calibración automática)
float altitudBase       = 0.0;   // m calculados al arrancar
float altitudAnterior   = 0.0;
float altitudMax        = -9999.0;

// GPS
String  gpsBuffer    = "";
float   gps_lat      = 0.0;
float   gps_lon      = 0.0;
float   gps_alt      = 0.0;
int     gps_sats     = 0;
bool    gps_fix      = false;
String  gps_datetime = "";   // Hora UTC del satélite (formato ISO)

// Fase de vuelo
enum Fase { ESPERA, CAIDA_LIBRE, APERTURA, DESCENSO, TIERRA };
Fase faseActual = ESPERA;

// ---------------------------------------------------------------
//  GRABACIÓN INTELIGENTE EN RAM (caja negra, solo durante vuelo)
//  Se activa al detectar lanzamiento, cada 2 segundos
// ---------------------------------------------------------------
#define MAX_REGISTROS_RAM  350    // ~11 min a 2s/muestra
#define INTERVALO_RAM_MS   2000   // Backup RAM cada 2 segundos

struct DatosRAM {
  uint32_t  t_ms;
  int16_t   alt;        // altitud relativa x10  (dm)
  int16_t   co2;        // ppm  — estabilidad atmosférica
  int16_t   pm25;       // ug/m3 — perfil vertical partículas
  int16_t   temp_hs;    // x100 (°C) — HS300x
  int16_t   hum_hs;     // x100 (%)  — HS300x
  int16_t   temp_scd;   // x100 (°C) — SCD40 (validación cruzada)
  int16_t   hum_scd;    // x100 (%)  — SCD40 (validación cruzada)
  int16_t   temp_lps;   // x100 (°C) — LPS22HB integrado (validación cruzada)
  int16_t   acX;        // x100 (g)
  int16_t   acY;
  int16_t   acZ;
  uint8_t   fase;
};

DatosRAM   ramBuffer[MAX_REGISTROS_RAM];
int        ramCount          = 0;
bool       grabandoRAM       = false;
unsigned long tUltimaRAM     = 0;

// Contador y tiempo
unsigned long timestamp      = 0;
unsigned long tUltimaMuestra = 0;

// =============================================================
//  SETUP
// =============================================================
void setup() {
  Serial.begin(115200);
  GPS_PORT.begin(9600);

  unsigned long ventana = millis();
  while (!Serial && millis() - ventana < 5000);

  Serial.println(F("============================================="));
  Serial.println(F("  CANSAT — VUELO INTEGRADO"));
  Serial.println(F("  Arduino Nano 33 BLE Sense Rev2"));
  Serial.println(F("============================================="));

  pinMode(LED_BUILTIN, OUTPUT);
  Wire.begin();
  inicializarSensores();
  inicializarSD();
  calibrarAltitud();

  if (sdOK) escribirCabecera();

  Serial.println(F("\n[LISTO] Esperando lanzamiento..."));
  Serial.println(F("Comandos: CSV_RAM (recuperar RAM) | BORRAR_RAM (limpiar RAM)"));
  Serial.println(F("-----------------------------------------------"));
}

// =============================================================
//  LOOP
// =============================================================
void loop() {
  // Leer GPS continuamente (no bloqueante)
  leerGPS();

  // Gestión de comandos por Serial
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim(); cmd.toUpperCase();
    if (cmd == "CSV_RAM")   exportarRAM();
    if (cmd == "BORRAR_RAM") {
      ramCount = 0; grabandoRAM = false;
      Serial.println(F("[RAM] Memoria limpiada"));
    }
  }

  // Muestra cada INTERVALO_MS
  if (millis() - tUltimaMuestra < INTERVALO_MS) return;
  tUltimaMuestra = millis();

  // -------- Leer todos los sensores --------
  float acX = 0, acY = 0, acZ = 0;
  float gyX = 0, gyY = 0, gyZ = 0;
  float presion = 0, tempLPS = 0;     // LPS22HB — presión + temperatura integrada
  float altRel = 0, altMar = 0;
  float temp_hs = 0, hum_hs = 0;      // HS300x — sensor principal T+HR
  uint16_t co2 = 0;
  float temp_scd = 0, hum_scd = 0;   // SCD40  — validación cruzada T+HR
  uint16_t pm1_0 = 0, pm2_5 = 0, pm10 = 0;

  // IMU
  if (imuOK) {
    if (IMU.accelerationAvailable()) IMU.readAcceleration(acX, acY, acZ);
    if (IMU.gyroscopeAvailable())    IMU.readGyroscope(gyX, gyY, gyZ);
  }

  // LPS22HB — presión y altitud
  if (lpsOK) {
    presion  = LPS22HB.readPressure();
    tempLPS  = LPS22HB.readTemperature();
    altRel   = 44330.0 * (1.0 - pow(presion / presionReferencia, 0.1903));
    altMar   = 44330.0 * (1.0 - pow(presion / SEA_LEVEL_PRESSURE, 0.1903));
  }

  // HS300x — temperatura y humedad (sensor principal de referencia)
  if (hs3OK) {
    temp_hs = HS300x.readTemperature();
    hum_hs  = HS300x.readHumidity();
  }

  // SCD40 — CO2 (estabilidad atmosférica) + T+HR (validación cruzada con HS300x)
  // ⚠️ Compensación de presión OBLIGATORIA: sin ella el CO2 baja artificialmente
  //    con la altitud (menos moléculas por el descenso de presión), lo que haría
  //    inútil la interpretación de CO2 vs altitud.
  if (scdOK && lpsOK && presion > 0) {
    // setAmbientPressure espera hPa como uint16_t (ej. 929 hPa)
    scd4x.setAmbientPressure((uint16_t)presion);
  }
  if (scdOK) {
    bool listo = false;
    scd4x.getDataReadyStatus(listo);
    if (listo) {
      uint16_t err = scd4x.readMeasurement(co2, temp_scd, hum_scd);
      if (err || co2 == 0) { co2 = 0; temp_scd = 0; hum_scd = 0; }
    }
  }

  // HM3301 — partículas
  leerHM3301(pm1_0, pm2_5, pm10);

  // -------- Actualizar fase de vuelo --------
  if (lpsOK) {
    actualizarFase(altRel, acZ);
    if (altRel > altitudMax) altitudMax = altRel;
    altitudAnterior = altRel;
  }

  // -------- Construir línea CSV --------
  // 24 columnas:
  //   timestamp, datetime, lat, lon, alt, alt_mar, sats,
  //   temp_hs, hum_hs, temp_scd, hum_scd, presion,
  //   co2, pm1_0, pm2_5, pm10,
  //   accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, fase

  String linea = "";
  linea += timestamp;                         linea += ",";
  linea += gps_datetime.length() > 0 ? gps_datetime : String("sin_fix"); linea += ",";
  linea += String(gps_lat, 6);               linea += ",";
  linea += String(gps_lon, 6);               linea += ",";
  linea += String(altRel, 1);                linea += ",";
  linea += String(altMar, 1);                linea += ",";
  linea += gps_sats;                         linea += ",";
  linea += String(temp_hs,  1);              linea += ",";   // HS300x
  linea += String(hum_hs,   1);              linea += ",";   // HS300x
  linea += String(temp_scd, 1);              linea += ",";   // SCD40 validación cruzada
  linea += String(hum_scd,  1);              linea += ",";   // SCD40 validación cruzada
  linea += String(tempLPS,  1);              linea += ",";   // LPS22HB integrado (validación cruzada)
  linea += String(presion,  1);              linea += ",";
  linea += co2;                              linea += ",";   // SCD40 estabilidad atm.
  linea += pm1_0;                            linea += ",";
  linea += pm2_5;                            linea += ",";
  linea += pm10;                             linea += ",";
  linea += String(acX * 1000.0, 2);         linea += ",";   // g → mG
  linea += String(acY * 1000.0, 2);         linea += ",";
  linea += String(acZ * 1000.0, 2);         linea += ",";
  linea += String(gyX, 1);                  linea += ",";
  linea += String(gyY, 1);                  linea += ",";
  linea += String(gyZ, 1);                  linea += ",";
  linea += nombreFase(faseActual);

  // -------- Guardar en SD --------
  if (sdOK) {
    if (dataFile.open(FILENAME, O_RDWR | O_CREAT | O_APPEND)) {
      dataFile.println(linea);
      dataFile.close();
    }
  }

  // -------- Grabación inteligente en RAM (solo durante vuelo activo) --------
  if (grabandoRAM && ramCount < MAX_REGISTROS_RAM) {
    if (millis() - tUltimaRAM >= INTERVALO_RAM_MS) {
      tUltimaRAM = millis();
      ramBuffer[ramCount].t_ms      = millis();
      ramBuffer[ramCount].alt        = (int16_t)(altRel   * 10.0);
      ramBuffer[ramCount].co2        = (int16_t)co2;
      ramBuffer[ramCount].pm25       = (int16_t)pm2_5;
      ramBuffer[ramCount].temp_hs    = (int16_t)(temp_hs  * 100.0);
      ramBuffer[ramCount].hum_hs     = (int16_t)(hum_hs   * 100.0);
      ramBuffer[ramCount].temp_scd   = (int16_t)(temp_scd * 100.0);
      ramBuffer[ramCount].hum_scd    = (int16_t)(hum_scd  * 100.0);
      ramBuffer[ramCount].temp_lps   = (int16_t)(tempLPS  * 100.0);
      ramBuffer[ramCount].acX        = (int16_t)(acX      * 100.0);
      ramBuffer[ramCount].acY        = (int16_t)(acY      * 100.0);
      ramBuffer[ramCount].acZ        = (int16_t)(acZ      * 100.0);
      ramBuffer[ramCount].fase       = (uint8_t)faseActual;
      ramCount++;
      digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    }
  }

  // Activar RAM al detectar lanzamiento
  if (!grabandoRAM && faseActual == CAIDA_LIBRE) {
    grabandoRAM  = true;
    tUltimaRAM   = millis();
    Serial.println(F("[RAM] Grabacion RAM iniciada"));
  }

  // -------- Serial Monitor (resumen cada 5 muestras) --------
  if (timestamp % 5 == 0) {
    Serial.println();
    Serial.print(F("t=")); Serial.print(timestamp);
    Serial.print(F("  FASE: ")); Serial.println(nombreFase(faseActual));
    Serial.print(F("  Alt rel=")); Serial.print(altRel, 1);
    Serial.print(F("m  alt_mar=")); Serial.print(altMar, 1);
    Serial.print(F("m  P=")); Serial.print(presion, 1); Serial.println(F("hPa"));
    // CO2 — indicador de estabilidad atmosférica
    Serial.print(F("  CO2=")); Serial.print(co2);
    Serial.print(F("ppm [estab.atm.]  PM2.5=")); Serial.print(pm2_5);
    Serial.print(F("ug/m3  PM10=")); Serial.println(pm10);
    // Temperatura y Humedad — validación cruzada triple (T) y doble (HR)
    Serial.print(F("  Temp HS300x=")); Serial.print(temp_hs,  1);
    Serial.print(F("C  Hum HS300x=")); Serial.print(hum_hs,   1); Serial.println(F("%"));
    Serial.print(F("  Temp SCD40 =")); Serial.print(temp_scd, 1);
    Serial.print(F("C  Hum SCD40 =")); Serial.print(hum_scd,  1); Serial.println(F("%"));
    Serial.print(F("  Temp LPS22HB=")); Serial.print(tempLPS, 1); Serial.println(F("C"));
    // Deltas entre sensores (referencia: < 2°C diferencia es aceptable)
    Serial.print(F("  DeltaT HS-SCD=")); Serial.print(abs(temp_hs - temp_scd), 1);
    Serial.print(F("C  HS-LPS=")); Serial.print(abs(temp_hs - tempLPS), 1);
    Serial.print(F("C  DeltaHR=")); Serial.print(abs(hum_hs - hum_scd), 1); Serial.println(F("%"));
    Serial.print(F("  GPS: "));
    if (gps_fix) {
      Serial.print(gps_lat, 5); Serial.print(F(",")); Serial.print(gps_lon, 5);
      Serial.print(F("  sats=")); Serial.println(gps_sats);
    } else {
      Serial.println(F("sin fix"));
    }
    if (sdOK) Serial.println(F("  SD: [OK]"));
    else      Serial.println(F("  SD: [--]"));
  }

  timestamp++;
}

// =============================================================
//  DETECCIÓN AUTOMÁTICA DE FASE DE VUELO
// =============================================================
void actualizarFase(float altRel, float acZ) {
  float acZmG = acZ * 1000.0;  // g → mG para comparar con umbrales

  switch (faseActual) {
    case ESPERA:
      // Detectar lanzamiento: altitud sube más de UMBRAL_LANZAMIENTO
      if (altRel > UMBRAL_LANZAMIENTO) {
        faseActual = CAIDA_LIBRE;
        Serial.println(F("\n>>> LANZAMIENTO DETECTADO: CAIDA LIBRE <<<"));
      }
      break;

    case CAIDA_LIBRE:
      // Detectar apertura paracaídas: pico de aceleración
      if (acZmG > ACCEL_APERTURA) {
        faseActual = APERTURA;
        Serial.println(F("\n>>> APERTURA PARACAIDAS <<<"));
      }
      break;

    case APERTURA:
      // Transición rápida a descenso cuando accel se estabiliza
      if (acZmG > 80.0 && acZmG < ACCEL_APERTURA) {
        faseActual = DESCENSO;
        Serial.println(F("\n>>> DESCENSO CON PARACAIDAS <<<"));
      }
      break;

    case DESCENSO:
      // Detectar tierra: altitud relativa cerca de 0 y accel estable
      if (altRel <= 2.0 && abs(acZmG - 1000.0) < 50.0) {
        faseActual = TIERRA;
        Serial.println(F("\n>>> ATERRIZAJE DETECTADO <<<"));
      }
      break;

    case TIERRA:
      // Fase final, no cambia
      break;
  }
}

// =============================================================
//  LECTURA HM3301 (directo Wire, sin librería)
// =============================================================
void leerHM3301(uint16_t &pm1, uint16_t &pm25, uint16_t &pm10_val) {
  if (!hm3OK) return;

  byte buf[29];
  Wire.requestFrom(HM3301_ADDR, 29);
  int i = 0;
  while (Wire.available() && i < 29) buf[i++] = Wire.read();

  if (i < 29) return;

  // Verificar checksum
  uint8_t suma = 0;
  for (int j = 0; j < 28; j++) suma += buf[j];
  if (suma != buf[28]) return;

  pm1     = (uint16_t)buf[10] << 8 | buf[11];
  pm25    = (uint16_t)buf[12] << 8 | buf[13];
  pm10_val = (uint16_t)buf[14] << 8 | buf[15];
}

// =============================================================
//  EXPORTAR RAM POR SERIAL (comando CSV_RAM)
// =============================================================
void exportarRAM() {
  Serial.println(F("\n--- CSV RAM: inicio ---"));
  Serial.println(F("t_ms,alt_m,co2_ppm,pm25,temp_hs,hum_hs,temp_scd,hum_scd,temp_lps,acX,acY,acZ,fase"));
  for (int i = 0; i < ramCount; i++) {
    Serial.print(ramBuffer[i].t_ms);                   Serial.print(",");
    Serial.print(ramBuffer[i].alt      / 10.0, 1);     Serial.print(",");
    Serial.print(ramBuffer[i].co2);                    Serial.print(",");
    Serial.print(ramBuffer[i].pm25);                   Serial.print(",");
    Serial.print(ramBuffer[i].temp_hs  / 100.0, 2);    Serial.print(",");
    Serial.print(ramBuffer[i].hum_hs   / 100.0, 2);    Serial.print(",");
    Serial.print(ramBuffer[i].temp_scd / 100.0, 2);    Serial.print(",");
    Serial.print(ramBuffer[i].hum_scd  / 100.0, 2);    Serial.print(",");
    Serial.print(ramBuffer[i].temp_lps / 100.0, 2);    Serial.print(",");
    Serial.print(ramBuffer[i].acX      / 100.0, 2);    Serial.print(",");
    Serial.print(ramBuffer[i].acY      / 100.0, 2);    Serial.print(",");
    Serial.print(ramBuffer[i].acZ      / 100.0, 2);    Serial.print(",");
    Serial.println(ramBuffer[i].fase);
  }
  Serial.print(F("--- FIN: "));
  Serial.print(ramCount);
  Serial.println(F(" registros ---"));
}

// =============================================================
//  LECTURA GPS (no bloqueante, parseo NMEA manual)
// =============================================================
void leerGPS() {
  while (GPS_PORT.available()) {
    char c = GPS_PORT.read();
    gpsBuffer += c;
    if (c == '\n') {
      parsearGPS(gpsBuffer);
      gpsBuffer = "";
    }
    if (gpsBuffer.length() > 120) gpsBuffer = "";  // Evitar overflow
  }
}

void parsearGPS(String s) {
  if (s.startsWith("$GNGGA") || s.startsWith("$GPGGA")) parsearGGA(s);
  else if (s.startsWith("$GNRMC") || s.startsWith("$GPRMC")) parsearRMC(s);
}

void parsearGGA(String s) {
  int last = 0, campo = 0;
  for (int i = 0; i < (int)s.length(); i++) {
    if (s[i] == ',' || s[i] == '\n') {
      String f = s.substring(last, i);
      // Campo 1: Hora UTC del satélite (HHMMSS.ss) → convertir a HH:MM:SS
      if (campo == 1 && f.length() >= 6) {
        String hh = f.substring(0, 2);
        String mm = f.substring(2, 4);
        String ss = f.substring(4, 6);
        gps_datetime = "UTC_" + hh + ":" + mm + ":" + ss;
      }
      if (campo == 7 && f.length() > 0) gps_sats = f.toInt();
      if (campo == 9 && f.length() > 0) gps_alt  = f.toFloat();
      last = i + 1; campo++;
    }
  }
}

void parsearRMC(String s) {
  int last = 0, campo = 0;
  for (int i = 0; i < (int)s.length(); i++) {
    if (s[i] == ',' || s[i] == '\n') {
      String f = s.substring(last, i);
      if (campo == 2) { gps_fix = (f == "A"); }
      if (campo == 3) { gps_lat =  parsearCoordenada(f); }
      if (campo == 4 && f == "S") { gps_lat = -gps_lat; }
      if (campo == 5) { gps_lon =  parsearCoordenada(f); }
      if (campo == 6 && f == "W") { gps_lon = -gps_lon; }
      last = i + 1; campo++;
    }
  }
}

float parsearCoordenada(String c) {
  if (c.length() < 5) return 0.0;
  int dot = c.indexOf('.');
  int deg = dot - 2;
  if (deg <= 0) return 0.0;
  return c.substring(0, deg).toFloat() + c.substring(deg).toFloat() / 60.0;
}

// =============================================================
//  GENERAR DATETIME DESDE MILLIS (fallback si no hay fix GPS)
// =============================================================
String generarDatetime() {
  // Se usa solo si el GPS no tiene fix todavía
  unsigned long seg = millis() / 1000;
  unsigned long mn  = seg / 60;
  unsigned long hr  = mn  / 60;
  char buf[20];
  snprintf(buf, sizeof(buf), "T+%02lu:%02lu:%02lu", hr % 24, mn % 60, seg % 60);
  return String(buf);
}

// =============================================================
//  NOMBRE DE FASE
// =============================================================
String nombreFase(Fase f) {
  switch (f) {
    case ESPERA:      return "espera";
    case CAIDA_LIBRE: return "caida_libre";
    case APERTURA:    return "apertura";
    case DESCENSO:    return "descenso";
    case TIERRA:      return "tierra";
    default:          return "desconocida";
  }
}

// =============================================================
//  CALIBRACIÓN AUTOMÁTICA DE ALTITUD (promedio 20 muestras)
// =============================================================
void calibrarAltitud() {
  if (!lpsOK) return;

  Serial.print(F("\n[CALIB] Calibrando altitud"));
  float suma = 0;
  for (int i = 0; i < 20; i++) {
    suma += LPS22HB.readPressure();
    delay(100);
    Serial.print(F("."));
  }
  presionReferencia = suma / 20.0;
  altitudBase = 44330.0 * (1.0 - pow(presionReferencia / SEA_LEVEL_PRESSURE, 0.1903));

  Serial.println();
  Serial.print(F("[CALIB] P referencia = ")); Serial.print(presionReferencia, 2); Serial.println(F(" hPa"));
  Serial.print(F("[CALIB] Alt absoluta = ")); Serial.print(altitudBase, 1);       Serial.println(F(" m"));
  Serial.println(F("[CALIB] Alt relativa = 0.0 m (punto de lanzamiento)"));
}

// =============================================================
//  INICIALIZAR SENSORES
// =============================================================
void inicializarSensores() {
  Serial.println(F("\n[INIT] Sensores..."));

  // IMU
  if (IMU.begin()) { imuOK = true; Serial.println(F("  [OK] IMU BMI270+BMM150")); }
  else              { Serial.println(F("  [!!] IMU — FALLO")); }

  // LPS22HB
  LPS22HB.begin();
  if (LPS22HB.connected()) { lpsOK = true; Serial.println(F("  [OK] LPS22HB")); }
  else                      { Serial.println(F("  [!!] LPS22HB — no detectado")); }

  // HS300x
  if (HS300x.begin()) { hs3OK = true; Serial.println(F("  [OK] HS300x")); }
  else                 { Serial.println(F("  [!!] HS300x — FALLO")); }

  // SCD40 (CO2)
  scd4x.begin(Wire, SCD41_I2C_ADDR_62);
  scd4x.stopPeriodicMeasurement();
  delay(500);
  uint16_t err = scd4x.startPeriodicMeasurement();
  if (!err) { scdOK = true; Serial.println(F("  [OK] SCD40 CO2")); }
  else      { Serial.println(F("  [!!] SCD40 — FALLO")); }

  // HM3301 (partículas — inicialización directa Wire)
  Wire.beginTransmission(HM3301_ADDR);
  Wire.write(0x88);
  if (Wire.endTransmission() == 0) {
    hm3OK = true;
    Serial.println(F("  [OK] HM3301 PM"));
  } else {
    Serial.println(F("  [!!] HM3301 — no detectado"));
  }

  // GPS
  Serial.println(F("  [..] GPS Serial1 iniciado (espera fix exterior)"));
  gpsOK = true;  // El puerto siempre está disponible, fix depende de exterior
}

// =============================================================
//  INICIALIZAR SD
// =============================================================
void inicializarSD() {
  Serial.println(F("\n[INIT] MicroSD..."));
  Serial.println(F("  Pines: CS=D10 MOSI=D11 MISO=D12 SCK=D13"));

  if (!sd.begin(SD_CS_PIN, SPI_SPEED)) {
    Serial.println(F("  [!!] SD — FALLO. Revisar cableado y formato FAT32."));
    return;
  }

  sdOK = true;
  uint32_t cardSize = sd.card()->sectorCount();
  Serial.print(F("  [OK] SD — ")); Serial.print(cardSize / 2048.0, 0); Serial.println(F(" MB"));
}

// =============================================================
//  ESCRIBIR CABECERA CSV
// =============================================================
void escribirCabecera() {
  if (sd.exists(FILENAME)) {
    Serial.println(F("  [SD] Archivo existente — añadiendo datos"));
    return;
  }

  if (dataFile.open(FILENAME, O_RDWR | O_CREAT | O_APPEND)) {
    dataFile.println(F("timestamp,datetime,lat,lon,alt,alt_mar,sats,"
                       "temp_hs,hum_hs,temp_scd,hum_scd,temp_lps,presion,"
                       "co2,pm1_0,pm2_5,pm10,"
                       "accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,fase"));
    dataFile.close();
    Serial.println(F("  [SD] Cabecera CSV escrita (25 columnas)"));
  }
}
