/*
 * ================================================================================
 * PROGRAMA 1: SENSORES INTEGRADOS ARDUINO NANO 33 BLE SENSE (VERSIÓN VUELO SEGURO)
 * ================================================================================
 * ✅ Adaptado con Espera Inteligente para Batería
 * ✅ Compatible con Arduino Nano 33 BLE Sense
 * 
 * SENSORES:
 *   ✅ HS3003: Temperatura + Humedad
 *   ✅ LPS22HB: Presión + Altitud
 *   ✅ BMI270: Acelerómetro + Giroscopio
 *   ✅ BMM150: Magnetómetro (Brújula)
 * 
 * OBJETIVO: Verificar que todos los sensores integrados funcionan
 * 
 * ================================================================================
 
#include <Arduino_BMI270_BMM150.h>
#include <Arduino_HS300x.h>
#include <ReefwingLPS22HB.h>

ReefwingLPS22HB pressureSensor;

// Variables [cite: 2]
float accelX, accelY, accelZ;
float gyroX, gyroY, gyroZ;
float magnetX, magnetY, magnetZ;
float temperatura_hs, humedad;
float temperatura_lps, presion, altitud;
int contador = 0; [cite: 3]

void setup() {
  Serial.begin(9600);

  // --- CONTROL DE ARRANQUE AUTÓNOMO (ESPERA INTELIGENTE) ---
  // Sustituimos "while (!Serial);" por este bloque de seguridad:
  unsigned long ventanaInicio = millis();
  while (!Serial && millis() - ventanaInicio < 5000) {
    // Espera 5s al USB. Si no hay, arranca solo para la misión.
  }
  
  Serial.println();
  Serial.println("╔════════════════════════════════════════╗");
  Serial.println("║  Programa 1: Sensores (Vuelo Seguro)   ║"); [cite: 4]
  Serial.println("║  Arduino Nano 33 BLE Sense            ║"); [cite: 5]
  Serial.println("╚════════════════════════════════════════╝");
  
  // Inicializar IMU [cite: 6]
  Serial.print("IMU... ");
  if (!IMU.begin()) {
    Serial.println("❌ ERROR");
    // No bloqueamos con while(1) en vuelo real, pero para test sí [cite: 7]
  } else {
    Serial.println("✓ OK");
  }
  
  // Inicializar HS3003 (Temp+Hum) [cite: 8]
  Serial.print("HS3003... ");
  if (!HS300x.begin()) {
    Serial.println("❌ ERROR");
  } else {
    Serial.println("✓ OK");
  }
  
  // Inicializar LPS22HB (Presión) [cite: 9]
  Serial.print("LPS22HB... ");
  pressureSensor.begin();
  if (!pressureSensor.connected()) {
    Serial.println("❌ ERROR");
  } else {
    Serial.println("✓ OK");
  }
  
  Serial.println("\nSistema listo. Iniciando lectura..."); [cite: 10]
  delay(1000);
}

void loop() {
  // LEER IMU [cite: 11, 12, 13]
  if (IMU.accelerationAvailable()) IMU.readAcceleration(accelX, accelY, accelZ);
  if (IMU.gyroscopeAvailable()) IMU.readGyroscope(gyroX, gyroY, gyroZ);
  if (IMU.magneticFieldAvailable()) IMU.readMagneticField(magnetX, magnetY, magnetZ);
  
  // LEER HS3003 [cite: 14]
  temperatura_hs = HS300x.readTemperature();
  humedad = HS300x.readHumidity();

  // LEER LPS22HB [cite: 15]
  presion = pressureSensor.readPressure();
  
  // Calcular altitud (Referencia estándar 1013.25 hPa) 
  // Nota: hPa = Pa / 100.0 si tu librería lee en Pascales
  float ratio = (presion / 100.0) / 1013.25; 
  altitud = 44330.0 * (1.0 - pow(ratio, 1.0 / 5.255)); [cite: 17]

  // MOSTRAR TABLA CADA 10 CICLOS [cite: 18, 19]
  if (contador % 10 == 0) {
    Serial.println("\nN° | Temp(HS) | Humedad | Presion | Altitud | AccelZ");
    Serial.println("───┼──────────┼─────────┼─────────┼─────────┼────────");
  }
  
  Serial.print(contador);
  Serial.print(" | "); [cite: 20]
  Serial.print(temperatura_hs, 1); Serial.print("°C    | ");
  Serial.print(humedad, 1); Serial.print("%    | ");
  Serial.print(presion / 100.0, 1); Serial.print(" hPa | "); [cite: 21]
  Serial.print(altitud, 1); Serial.print("m   | ");
  Serial.println(accelZ, 2); [cite: 23]
  
  contador++;
  delay(1000); // Reducido a 1s para ver cambios más rápido [cite: 22]
}

/* 
 * ========================================================================
 * NOTAS IMPORTANTES:
 * 
 *✅ TEMPERATURA HS3003:
 *    - Tiene error ±2-3°C por calor del chip
 *    - Para precisión, usar DHT22 externo o el SCD40
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
