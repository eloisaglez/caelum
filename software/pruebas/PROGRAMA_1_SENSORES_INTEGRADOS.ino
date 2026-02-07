/*
 * ========================================================================
 * PROGRAMA 1: SENSORES INTEGRADOS ARDUINO NANO 33 BLE SENSE
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
 * OBJETIVO: Verificar que todos los sensores integrados funcionan
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
  Serial.begin(9600);
  delay(2000);
  
  Serial.println();
  Serial.println("╔════════════════════════════════════════╗");
  Serial.println("║  Programa 1: Sensores Integrados       ║");
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
  Serial.println("═══════════════════════════════════════════════════");
  Serial.println("Sistema listo. Leyendo sensores...");
  Serial.println("═══════════════════════════════════════════════════");
  Serial.println();
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
  
  // MOSTRAR TABLA
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
  
  contador++;
  delay(2000);
}

/* 
 * ========================================================================
 * NOTAS IMPORTANTES:
 * 
 * ⚠️ TEMPERATURA HS3003:
 *    - MÁS real que LPS22HB
 *    - Pero tiene error ±2-3°C por calor del chip
 *    - Para precisión, usar DHT22 externo
 * 
 * ✅ PRESIÓN LPS22HB:
 *    - Precisa para altitud
 *    - A nivel del mar: ~1013 hPa
 *    - En Madrid (600m): ~930 hPa
 * 
 * ✅ IMU:
 *    - Acelerómetro: ±4g de rango
 *    - En reposo Z = 1.0 m/s² (gravedad)
 *    - Útil para detectar impactos
 * 
 * ========================================================================
 */
