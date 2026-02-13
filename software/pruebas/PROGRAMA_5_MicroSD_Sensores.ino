// =============================================================
//  TEST: Módulo MicroSD Adafruit + Sensores Integrados
//  Hardware : Arduino Nano 33 BLE Sense Rev2
//  Módulo SD: Adafruit MicroSD SPI or SDIO Card Breakout Board
//  Proyecto : CanSat — Misión 2 Detección de Firmas de Combustión
// =============================================================

// ---------------------------------------------------------------
//  LIBRERÍAS  (instalar desde Library Manager si no están)
//    - SdFat             buscar "SdFat" de Bill Greiman (Adafruit Fork)
//    - Arduino_BMI270_BMM150   (oficial Arduino)
//    - ReefwingLPS22HB         (Reefwing Software)
//    - Arduino_HS300x          (oficial Arduino)
//    - Arduino_APDS9960        (oficial Arduino)
// ---------------------------------------------------------------
#include "SdFat.h"                  // SD — Adafruit Fork, compatible MBED
#include <Arduino_BMI270_BMM150.h>  // Acelerómetro + Giroscopio + Magnetómetro
#include <ReefwingLPS22HB.h>        // Presión + Temperatura + Altitud
#include <Arduino_HS300x.h>         // Humedad + Temperatura (sensor HS300x)
#include <Arduino_APDS9960.h>       // Luz + Proximidad + Color

// ---------------------------------------------------------------
//  PINES SPI — Nano 33 BLE Sense Rev2
//  MOSI = D11  |  MISO = D12  |  SCK = D13  |  CS = D10
// ---------------------------------------------------------------
#define SD_CS_PIN  10
#define SPI_SPEED  SD_SCK_MHZ(4)   // 4 MHz conservador para mayor estabilidad

SdFat           sd;
SdFile          dataFile;
ReefwingLPS22HB LPS22HB;            // Objeto propio de la librería Reefwing

// ---------------------------------------------------------------
//  ALTITUD REAL (absoluta sobre nivel del mar)
//  Consultar presión al nivel del mar en AEMET o Windy ANTES de encender.
//  Ejemplos orientativos (varían cada día con el tiempo meteorológico):
//    Nivel del mar:      1013.25 hPa
//    Las Rozas (630 m):   ~929.5 hPa
//    Torrelodones (700m): ~928.8 hPa
//  !! ACTUALIZAR ESTE VALOR con el dato real de AEMET del día !!
// ---------------------------------------------------------------
float SEA_LEVEL_PRESSURE = 1013.25;  // hPa — presión real al nivel del mar (AEMET)
float presionReferencia  = 0.0;      // Se calibra automáticamente al arrancar

// ---------------------------------------------------------------
//  VARIABLES GLOBALES
// ---------------------------------------------------------------
const char FILENAME[] = "TEST_SD.CSV";

unsigned long muestraNum = 0;
unsigned long tInicio    = 0;

bool imuOK  = false;
bool lpsOK  = false;
bool hs3OK  = false;
bool apdsOK = false;
bool sdOK   = false;

// =============================================================
//  SETUP
// =============================================================
void setup() {
  Serial.begin(115200);
  delay(2000);   // Tiempo para que el PC abra el puerto serie

  Serial.println(F("============================================="));
  Serial.println(F("  TEST MicroSD + Sensores Integrados"));
  Serial.println(F("  Arduino Nano 33 BLE Sense Rev2"));
  Serial.println(F("============================================="));

  inicializarSensores();
  inicializarSD();

  // --- Calibración automática de altitud relativa al arranque ---
  if (lpsOK) {
    delay(500);  // Esperar lectura estable
    presionReferencia = LPS22HB.readPressure();
    Serial.print(F("\n[CALIB] Presion en tierra: "));
    Serial.print(presionReferencia, 2);
    Serial.println(F(" hPa"));
    float altAbsoluta = 44330.0 * (1.0 - pow(presionReferencia / SEA_LEVEL_PRESSURE, 0.1903));
    Serial.print(F("[CALIB] Altitud absoluta estimada: "));
    Serial.print(altAbsoluta, 1);
    Serial.println(F(" m (depende de SEA_LEVEL_PRESSURE)"));
    Serial.println(F("[CALIB] Altitud relativa = 0.0 m (punto de lanzamiento)"));
  }

  if (sdOK) {
    escribirCabecera();
  }

  tInicio = millis();
  Serial.println(F("\n[INFO] Grabacion iniciada — muestra cada 500 ms"));
  Serial.println(F("----------------------------------------------"));
}

// =============================================================
//  LOOP
// =============================================================
void loop() {
  muestraNum++;
  unsigned long tRelativo = millis() - tInicio;

  // ---------- IMU: BMI270 (acelerómetro + giroscopio) + BMM150 (magnetómetro) ----------
  float acX = 0, acY = 0, acZ = 0;
  float gyX = 0, gyY = 0, gyZ = 0;
  float mgX = 0, mgY = 0, mgZ = 0;

  if (imuOK) {
    if (IMU.accelerationAvailable())  IMU.readAcceleration(acX, acY, acZ);
    if (IMU.gyroscopeAvailable())     IMU.readGyroscope(gyX, gyY, gyZ);
    if (IMU.magneticFieldAvailable()) IMU.readMagneticField(mgX, mgY, mgZ);
  }

  // ---------- LPS22HB: presión, temperatura, altitud (librería Reefwing) ----------
  float presion = 0, tempLPS = 0, altitud = 0;

  float altitudRelativa = 0;  // m respecto al punto de arranque (siempre precisa)

  if (lpsOK) {
    presion  = LPS22HB.readPressure();     // hPa
    tempLPS  = LPS22HB.readTemperature();  // °C
    // Altitud absoluta: precisa solo si SEA_LEVEL_PRESSURE = presion real AEMET del dia
    altitud  = 44330.0 * (1.0 - pow(presion / SEA_LEVEL_PRESSURE, 0.1903));  // m
    // Altitud relativa: siempre precisa, empieza en 0 m al arrancar
    if (presionReferencia > 0)
      altitudRelativa = 44330.0 * (1.0 - pow(presion / presionReferencia, 0.1903));  // m
  }

  // ---------- HS300x: humedad + temperatura ----------
  float humedad = 0, tempHS = 0;

  if (hs3OK) {
    tempHS  = HS300x.readTemperature();  // °C
    humedad = HS300x.readHumidity();     // %
  }

  // ---------- APDS9960: luz + proximidad + color ----------
  int lux = 0, proximidad = 0;
  int r = 0, g = 0, b = 0, a = 0;

  if (apdsOK) {
    if (APDS.colorAvailable())     { APDS.readColor(r, g, b, a); lux = a; }
    if (APDS.proximityAvailable()) { proximidad = APDS.readProximity(); }
  }

  // ---------- Construir línea CSV ----------
  String linea = "";
  linea += muestraNum;             linea += ",";
  linea += tRelativo;              linea += ",";
  linea += String(acX, 4);        linea += ",";
  linea += String(acY, 4);        linea += ",";
  linea += String(acZ, 4);        linea += ",";
  linea += String(gyX, 2);        linea += ",";
  linea += String(gyY, 2);        linea += ",";
  linea += String(gyZ, 2);        linea += ",";
  linea += String(mgX, 2);        linea += ",";
  linea += String(mgY, 2);        linea += ",";
  linea += String(mgZ, 2);        linea += ",";
  linea += String(presion, 2);    linea += ",";
  linea += String(tempLPS, 2);    linea += ",";
  linea += String(altitud, 2);    linea += ",";
  linea += String(humedad, 1);    linea += ",";
  linea += String(tempHS, 2);     linea += ",";
  linea += lux;                   linea += ",";
  linea += proximidad;            linea += ",";
  linea += r;                     linea += ",";
  linea += g;                     linea += ",";
  linea += b;

  // ---------- Guardar en SD ----------
  bool guardado = false;
  if (sdOK) {
    if (dataFile.open(FILENAME, O_RDWR | O_CREAT | O_APPEND)) {
      dataFile.println(linea);
      dataFile.close();   // close() hace flush garantizado
      guardado = true;
    } else {
      Serial.println(F("[ERROR SD] No se pudo abrir el archivo!"));
    }
  }

  // ---------- Serial Monitor: resumen cada 10 muestras ----------
  if (muestraNum % 10 == 1) {
    Serial.println();
    Serial.print(F("--- Muestra #")); Serial.print(muestraNum);
    Serial.print(F(" | t="));         Serial.print(tRelativo);
    Serial.println(F(" ms ---"));

    Serial.print(F("  IMU  Ac [g]     X=")); Serial.print(acX, 3);
    Serial.print(F("  Y="));                  Serial.print(acY, 3);
    Serial.print(F("  Z="));                  Serial.println(acZ, 3);

    Serial.print(F("       Gy [deg/s] X=")); Serial.print(gyX, 1);
    Serial.print(F("  Y="));                  Serial.print(gyY, 1);
    Serial.print(F("  Z="));                  Serial.println(gyZ, 1);

    Serial.print(F("       Mg [uT]    X=")); Serial.print(mgX, 1);
    Serial.print(F("  Y="));                  Serial.print(mgY, 1);
    Serial.print(F("  Z="));                  Serial.println(mgZ, 1);

    Serial.print(F("  LPS  P="));        Serial.print(presion, 2);
    Serial.print(F(" hPa  T="));         Serial.print(tempLPS, 2);
    Serial.println(F(" C"));
    Serial.print(F("       Alt abs="));  Serial.print(altitud, 1);
    Serial.print(F(" m  Alt rel="));     Serial.print(altitudRelativa, 1);
    Serial.println(F(" m"));

    Serial.print(F("  HS3  Hum="));  Serial.print(humedad, 1);
    Serial.print(F(" %  T="));       Serial.print(tempHS, 2);
    Serial.println(F(" C"));

    Serial.print(F("  APDS Lux~="));  Serial.print(lux);
    Serial.print(F("  Prox="));       Serial.print(proximidad);
    Serial.print(F("  RGB=("));       Serial.print(r);
    Serial.print(F(","));              Serial.print(g);
    Serial.print(F(","));              Serial.print(b);
    Serial.println(F(")"));

    if (guardado) {
      Serial.print(F("  SD   [OK] Guardado en "));
      Serial.println(FILENAME);
    } else if (sdOK) {
      Serial.println(F("  SD   [!!] Error al guardar esta muestra"));
    } else {
      Serial.println(F("  SD   [--] No disponible — datos solo en Serial"));
    }
  }

  delay(500);   // 2 Hz — modifica si necesitas otra frecuencia
}

// =============================================================
//  FUNCIÓN: Inicializar sensores integrados
// =============================================================
void inicializarSensores() {
  Serial.println(F("\n[INIT] Sensores integrados..."));

  // IMU — BMI270 + BMM150
  if (IMU.begin()) {
    imuOK = true;
    Serial.println(F("  [OK] IMU BMI270 + BMM150"));
  } else {
    Serial.println(F("  [!!] IMU — FALLO"));
  }

  // Barométrico — LPS22HB  (API Reefwing: begin() + connected())
  LPS22HB.begin();
  if (LPS22HB.connected()) {
    lpsOK = true;
    Serial.println(F("  [OK] LPS22HB presion/temp/altitud"));
  } else {
    Serial.println(F("  [!!] LPS22HB — no detectado"));
  }

  // Humedad — HS300x
  if (HS300x.begin()) {
    hs3OK = true;
    Serial.println(F("  [OK] HS300x humedad/temperatura"));
  } else {
    Serial.println(F("  [!!] HS300x — FALLO"));
  }

  // Luz/Proximidad/Color — APDS9960
  if (APDS.begin()) {
    apdsOK = true;
    Serial.println(F("  [OK] APDS9960 luz/proximidad"));
  } else {
    Serial.println(F("  [!!] APDS9960 — FALLO"));
  }
}

// =============================================================
//  FUNCIÓN: Inicializar módulo MicroSD
// =============================================================
void inicializarSD() {
  Serial.println(F("\n[INIT] Modulo MicroSD..."));
  Serial.println(F("  Pines: CS=D10 | MOSI=D11 | MISO=D12 | SCK=D13"));

  if (!sd.begin(SD_CS_PIN, SPI_SPEED)) {
    Serial.println(F("  [!!] SD — FALLO. Revisar:"));
    Serial.println(F("       - Cables: CS->D10, MOSI->D11, MISO->D12, SCK->D13"));
    Serial.println(F("       - MicroSD insertada"));
    Serial.println(F("       - Formato FAT32 (NO exFAT, NO NTFS)"));
    Serial.println(F("       - Alimentacion 3.3V (NO 5V)"));
    // sd.initErrorHalt();  // Descomentar para ver error detallado + parar
    return;
  }

  sdOK = true;
  uint32_t cardSize = sd.card()->sectorCount();
  Serial.println(F("  [OK] MicroSD"));
  Serial.print(F("       Tamano: "));
  Serial.print(cardSize / 2048.0, 0);
  Serial.println(F(" MB"));

  if (sd.exists(FILENAME)) {
    Serial.print(F("       Archivo '"));
    Serial.print(FILENAME);
    Serial.println(F("' existente — anadiendo al final"));
  } else {
    Serial.print(F("       Creando: "));
    Serial.println(FILENAME);
  }
}

// =============================================================
//  FUNCIÓN: Escribir cabecera CSV (solo si el archivo es nuevo)
// =============================================================
void escribirCabecera() {
  if (sd.exists(FILENAME)) return;  // Si ya existe, no repetir cabecera

  if (dataFile.open(FILENAME, O_RDWR | O_CREAT | O_APPEND)) {
    dataFile.println(F("# CanSat - TEST MicroSD + Sensores Integrados"));
    dataFile.println(F("# Arduino Nano 33 BLE Sense Rev2"));
    dataFile.println(F("# Unidades: g | deg/s | uT | hPa | C | m | % | lux | 0-255"));
    dataFile.println(F("muestra,tiempo_ms,"
                       "acX_g,acY_g,acZ_g,"
                       "gyX_ds,gyY_ds,gyZ_ds,"
                       "mgX_uT,mgY_uT,mgZ_uT,"
                       "presion_hPa,tempLPS_C,altitud_m,"
                       "humedad_pct,tempHS_C,"
                       "lux,proximidad,r,g,b"));
    dataFile.close();
    Serial.println(F("  [OK] Cabecera CSV escrita"));
  } else {
    Serial.println(F("  [!!] Error al escribir cabecera"));
  }
}
