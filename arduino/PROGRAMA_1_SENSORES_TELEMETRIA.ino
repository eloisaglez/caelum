/*
 * ========================================================================
 * PROGRAMA 1: SENSORES INTEGRADOS + TELEMETRÍA APC220
 * ========================================================================
 * 
 * Autor: CanSat Misión 2
 * Fecha: Enero 2026
 * Proyecto: CanSat Misión 2
 * 
 * SENSORES:
 *   ✅ HS3003: Temperatura + Humedad
 *   ✅ LPS22HB: Presión + Altitud
 *   ✅ BMI270: Acelerómetro + Giroscopio
 *   ✅ BMM150: Magnetómetro (Brújula)
 * 
 * TELEMETRÍA:
 *   ✅ APC220 por Serial1 (pines 0 y 1)
 * 
 * CONEXIÓN APC220:
 *   Pin 0 (RX) → RXD del APC220
 *   Pin 1 (TX) → TXD del APC220
 *   3.3V       → VCC del APC220
 *   GND        → GND del APC220
 * 
 * ========================================================================
 */

#include <Arduino_BMI270_BMM150.h>
#include <Arduino_HS300x.h>
#include <ReefwingLPS22HB.h>

ReefwingLPS22HB pressureSensor;

// Variables
float accelX, accelY, accelZ;
float gyroX, gyroY, gyroZ;
float magnetX, magnetY, magnetZ;
float temperatura_hs, humedad;
float temperatura_lps, presion, altitud;
int contador = 0;

void setup() {
  Serial.begin(9600);   // USB (debug)
  Serial1.begin(9600);  // APC220 (telemetría)
  delay(2000);
  
  Serial.println();
  Serial.println("╔════════════════════════════════════════╗");
  Serial.println("║  Programa 1: Sensores + Telemetría     ║");
  Serial.println("║  Arduino Nano 33 BLE Sense            ║");
  Serial.println("╚════════════════════════════════════════╝");
  Serial.println();
  
  // Inicializar IMU
  Serial.print("IMU (BMI270+BMM150)... ");
  if (!IMU.begin()) {
    Serial.println("❌ ERROR");
    while(1) delay(1000);
  }
  Serial.println("✓ OK");
  
  // Inicializar HS3003
  Serial.print("HS3003 (Temp+Humedad)... ");
  if (!HS300x.begin()) {
    Serial.println("❌ ERROR");
    while(1) delay(1000);
  }
  Serial.println("✓ OK");
  
  // Inicializar LPS22HB
  Serial.print("LPS22HB (Presión)... ");
  pressureSensor.begin();
  if (!pressureSensor.connected()) {
    Serial.println("❌ ERROR");
    while(1) delay(1000);
  }
  Serial.println("✓ OK");
  
  Serial.println();
  Serial.println("APC220 inicializado en Serial1");
  Serial.println();
  Serial.println("═══════════════════════════════════════════════════");
  Serial.println("Sistema listo. Enviando telemetría...");
  Serial.println("═══════════════════════════════════════════════════");
  Serial.println();
  
  // Enviar cabecera por radio
  Serial1.println("CANSAT_MISION2_INICIO");
  
  delay(2000);
}

void loop() {
  // LEER IMU
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(accelX, accelY, accelZ);
  }
  
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gyroX, gyroY, gyroZ);
  }
  
  if (IMU.magneticFieldAvailable()) {
    IMU.readMagneticField(magnetX, magnetY, magnetZ);
  }
  
  // LEER HS3003 (Temperatura + Humedad)
  temperatura_hs = HS300x.readTemperature();
  humedad = HS300x.readHumidity();
  
  // LEER LPS22HB (Presión + Temperatura)
  temperatura_lps = pressureSensor.readTemperature();
  presion = pressureSensor.readPressure();
  
  // Calcular altitud (nivel del mar = 1013.25 hPa)
  float referencePressure = 1013.25;
  float ratio = presion / referencePressure;
  altitud = 44330.0 * (1.0 - pow(ratio, 1.0 / 5.255));
  
  // MOSTRAR POR USB (debug)
  if (contador % 10 == 0) {
    Serial.println();
    Serial.println("N° | Temp(HS) | Humedad | Presion | Altitud | AccelZ | GyroX");
    Serial.println("───┼──────────┼─────────┼─────────┼─────────┼────────┼────────");
  }
  
  Serial.print(contador);
  Serial.print(" | ");
  Serial.print(temperatura_hs, 1);
  Serial.print("°C    | ");
  Serial.print(humedad, 1);
  Serial.print("%    | ");
  Serial.print(presion / 100.0, 1);
  Serial.print(" hPa | ");
  Serial.print(altitud, 1);
  Serial.print("m   | ");
  Serial.print(accelZ, 2);
  Serial.print("   | ");
  Serial.print(gyroX, 1);
  Serial.println();
  
  // ENVIAR POR APC220 (telemetría)
  // Formato CSV: N,Temp,Hum,Pres,Alt,AccX,AccY,AccZ,GyrX,GyrY,GyrZ,MagX,MagY,MagZ
  Serial1.print(contador);
  Serial1.print(",");
  Serial1.print(temperatura_hs, 1);
  Serial1.print(",");
  Serial1.print(humedad, 1);
  Serial1.print(",");
  Serial1.print(presion / 100.0, 2);
  Serial1.print(",");
  Serial1.print(altitud, 1);
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
  delay(2000);
}

/* 
 * ========================================================================
 * FORMATO TELEMETRÍA (CSV):
 * 
 * N,Temp,Hum,Pres,Alt,AccX,AccY,AccZ,GyrX,GyrY,GyrZ,MagX,MagY,MagZ
 * 
 * Ejemplo:
 * 1,23.5,45.2,1013.25,0.5,0.01,-0.02,1.00,0.5,-0.3,0.1,25.3,-12.1,40.5
 * 
 * ========================================================================
 */
