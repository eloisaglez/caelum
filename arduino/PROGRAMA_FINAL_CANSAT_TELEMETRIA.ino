/*
 * ========================================================================
 * PROGRAMA FINAL CANSAT - TODOS LOS SENSORES + TELEMETRÍA APC220
 * ========================================================================
 * 
 * Autor: CanSat Misión 2
 * Fecha: Febrero 2026
 * Proyecto: CanSat IES Diego Velázquez
 * 
 * SENSORES INTEGRADOS:
 *   ✅ HS3003: Temperatura + Humedad
 *   ✅ LPS22HB: Presión + Altitud
 *   ✅ BMI270: Acelerómetro + Giroscopio
 *   ✅ BMM150: Magnetómetro (Brújula)
 * 
 * SENSORES EXTERNOS:
 *   ✅ SCD40: CO2 + Temperatura + Humedad
 *   ✅ GPS ATGM336H: Posición + Altitud
 * 
 * TELEMETRÍA:
 *   ✅ APC220 por Serial1 (pines 0 y 1)
 * 
 * ========================================================================
 * CONEXIONES
 * ========================================================================
 * 
 * APC220 (telemetría):
 *   Pin 0 (RX) → RXD del APC220
 *   Pin 1 (TX) → TXD del APC220
 *   3.3V       → VCC del APC220
 *   GND        → GND del APC220
 * 
 * SCD40 (CO2) - I2C:
 *   SDA        → SDA del Arduino
 *   SCL        → SCL del Arduino
 *   3.3V       → VCC
 *   GND        → GND
 * 
 * GPS ATGM336H - Serial2 o SoftwareSerial:
 *   Ver configuración según conexión
 * 
 * ========================================================================
 */

#include <Arduino_BMI270_BMM150.h>
#include <Arduino_HS300x.h>
#include <ReefwingLPS22HB.h>
#include <Wire.h>
#include <SensirionI2CScd4x.h>

// ========== INSTANCIAS ==========
ReefwingLPS22HB pressureSensor;
SensirionI2CScd4x scd4x;

// ========== VARIABLES IMU ==========
float accelX, accelY, accelZ;
float gyroX, gyroY, gyroZ;
float magnetX, magnetY, magnetZ;

// ========== VARIABLES SENSORES INTEGRADOS ==========
float temperatura_hs, humedad_hs;
float temperatura_lps, presion, altitud;

// ========== VARIABLES SCD40 ==========
uint16_t co2;
float temperatura_scd, humedad_scd;

// ========== VARIABLES GPS ==========
// TODO: Añadir GPS cuando esté conectado
float latitud = 0.0;
float longitud = 0.0;
float altitud_gps = 0.0;
int satelites = 0;

// ========== CONTROL ==========
unsigned long contador = 0;
unsigned long tiempoAnterior = 0;
const unsigned long INTERVALO = 1000;  // 1 segundo

// ========== PRESIÓN REFERENCIA ==========
float presionReferencia = 1013.25;  // hPa a nivel del mar

void setup() {
  Serial.begin(9600);   // USB (debug)
  Serial1.begin(9600);  // APC220 (telemetría)
  Wire.begin();
  
  delay(2000);
  
  Serial.println();
  Serial.println("========================================");
  Serial.println("  CANSAT MISION 2 - PROGRAMA FINAL");
  Serial.println("  IES Diego Velazquez");
  Serial.println("========================================");
  Serial.println();
  
  // ===== INICIALIZAR IMU =====
  Serial.print("IMU (BMI270+BMM150)... ");
  if (!IMU.begin()) {
    Serial.println("ERROR");
  } else {
    Serial.println("OK");
  }
  
  // ===== INICIALIZAR HS3003 =====
  Serial.print("HS3003 (Temp+Humedad)... ");
  if (!HS300x.begin()) {
    Serial.println("ERROR");
  } else {
    Serial.println("OK");
  }
  
  // ===== INICIALIZAR LPS22HB =====
  Serial.print("LPS22HB (Presion)... ");
  pressureSensor.begin();
  if (!pressureSensor.connected()) {
    Serial.println("ERROR");
  } else {
    Serial.println("OK");
  }
  
  // ===== INICIALIZAR SCD40 =====
  Serial.print("SCD40 (CO2)... ");
  scd4x.begin(Wire);
  scd4x.stopPeriodicMeasurement();
  delay(500);
  if (scd4x.startPeriodicMeasurement() != 0) {
    Serial.println("ERROR");
  } else {
    Serial.println("OK");
  }
  
  Serial.println();
  Serial.println("Sistema iniciado. Transmitiendo...");
  Serial.println();
  
  // Enviar cabecera por radio
  Serial1.println("CANSAT,INICIO,MISION2");
  
  delay(2000);
}

void loop() {
  unsigned long tiempoActual = millis();
  
  if (tiempoActual - tiempoAnterior >= INTERVALO) {
    tiempoAnterior = tiempoActual;
    
    // ===== LEER IMU =====
    if (IMU.accelerationAvailable()) {
      IMU.readAcceleration(accelX, accelY, accelZ);
    }
    if (IMU.gyroscopeAvailable()) {
      IMU.readGyroscope(gyroX, gyroY, gyroZ);
    }
    if (IMU.magneticFieldAvailable()) {
      IMU.readMagneticField(magnetX, magnetY, magnetZ);
    }
    
    // ===== LEER HS3003 =====
    temperatura_hs = HS300x.readTemperature();
    humedad_hs = HS300x.readHumidity();
    
    // ===== LEER LPS22HB =====
    temperatura_lps = pressureSensor.readTemperature();
    presion = pressureSensor.readPressure();
    
    // Calcular altitud
    float ratio = presion / presionReferencia;
    altitud = 44330.0 * (1.0 - pow(ratio, 1.0 / 5.255));
    
    // ===== LEER SCD40 =====
    bool datosCO2 = false;
    if (scd4x.getDataReadyFlag(datosCO2) == 0 && datosCO2) {
      scd4x.readMeasurement(co2, temperatura_scd, humedad_scd);
    }
    
    // ===== MOSTRAR POR USB (debug) =====
    Serial.print("Paq:");
    Serial.print(contador);
    Serial.print(" T:");
    Serial.print(temperatura_hs, 1);
    Serial.print("C H:");
    Serial.print(humedad_hs, 1);
    Serial.print("% P:");
    Serial.print(presion / 100.0, 1);
    Serial.print("hPa Alt:");
    Serial.print(altitud, 1);
    Serial.print("m CO2:");
    Serial.print(co2);
    Serial.println("ppm");
    
    // ===== ENVIAR POR APC220 (telemetría) =====
    // Formato CSV:
    // Paq,Temp,Hum,Pres,Alt,CO2,Lat,Lon,AltGPS,Sat,AccX,AccY,AccZ,GyrX,GyrY,GyrZ,MagX,MagY,MagZ
    
    Serial1.print(contador);
    Serial1.print(",");
    Serial1.print(temperatura_hs, 1);
    Serial1.print(",");
    Serial1.print(humedad_hs, 1);
    Serial1.print(",");
    Serial1.print(presion / 100.0, 2);
    Serial1.print(",");
    Serial1.print(altitud, 1);
    Serial1.print(",");
    Serial1.print(co2);
    Serial1.print(",");
    Serial1.print(latitud, 6);
    Serial1.print(",");
    Serial1.print(longitud, 6);
    Serial1.print(",");
    Serial1.print(altitud_gps, 1);
    Serial1.print(",");
    Serial1.print(satelites);
    Serial1.print(",");
    Serial1.print(accelX, 2);
    Serial1.print(",");
    Serial1.print(accelY, 2);
    Serial1.print(",");
    Serial1.print(accelZ, 2);
    Serial1.print(",");
    Serial1.print(gyroX, 1);
    Serial1.print(",");
    Serial1.print(gyroY, 1);
    Serial1.print(",");
    Serial1.print(gyroZ, 1);
    Serial1.print(",");
    Serial1.print(magnetX, 1);
    Serial1.print(",");
    Serial1.print(magnetY, 1);
    Serial1.print(",");
    Serial1.println(magnetZ, 1);
    
    contador++;
  }
}

/* 
 * ========================================================================
 * FORMATO TELEMETRÍA CSV:
 * 
 * Paq,Temp,Hum,Pres,Alt,CO2,Lat,Lon,AltGPS,Sat,AccX,AccY,AccZ,GyrX,GyrY,GyrZ,MagX,MagY,MagZ
 * 
 * Campos:
 *   Paq     = Número de paquete (contador)
 *   Temp    = Temperatura HS3003 (°C)
 *   Hum     = Humedad HS3003 (%)
 *   Pres    = Presión LPS22HB (hPa)
 *   Alt     = Altitud barométrica (m)
 *   CO2     = Concentración CO2 (ppm)
 *   Lat     = Latitud GPS
 *   Lon     = Longitud GPS
 *   AltGPS  = Altitud GPS (m)
 *   Sat     = Número de satélites
 *   AccX/Y/Z = Acelerómetro (m/s²)
 *   GyrX/Y/Z = Giroscopio (°/s)
 *   MagX/Y/Z = Magnetómetro (µT)
 * 
 * ========================================================================
 * NOTAS:
 * 
 * - GPS pendiente de integrar (variables en 0)
 * - Calibrar presionReferencia según altitud del lugar de lanzamiento
 * - CO2 tarda ~30 segundos en dar primera lectura válida
 * 
 * ========================================================================
 */
