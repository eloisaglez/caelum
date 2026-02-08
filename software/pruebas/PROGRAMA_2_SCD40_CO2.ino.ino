/*
 * =========================================================================
 * PROYECTO CANSAT RAM - PRUEBA DE SENSORES AMBIENTALES
 * =========================================================================
 * DESCRIPCIÓN:
 * Este programa realiza la lectura del sensor de CO2 (SCD40) y del 
 * barómetro interno del Arduino Nano 33 BLE Sense. 
 * Muestra en tiempo real: Altitud, CO2, Temperatura y Humedad.
 * * CONEXIONES SCD40 (I2C):
 * - VCC  --> Pin 3.3V o 5V del Arduino
 * - GND  --> Pin GND del Arduino
 * - SDA  --> Pin A4 del Arduino (SDA)
 * - SCL  --> Pin A5 del Arduino (SCL)
 * * SEGURIDAD DE ARRANQUE:
 * Incluye una "ventana de espera" de 5 segundos. Si el Arduino detecta
 * conexión USB, inicia tras abrir el monitor. Si detecta batería (vuelo),
 * inicia automáticamente tras 5 segundos para evitar bloqueos.
 * =========================================================================
 */

#include <SensirionI2cScd4x.h>
#include <Arduino_LPS22HB.h>
#include <Wire.h>

SensirionI2cScd4x scd4x;
float altitudBase = 0;

void setup() {
  Serial.begin(9600);

  // --- CONTROL DE ARRANQUE AUTÓNOMO (BATERÍA) ---
  // Esperamos un máximo de 5 segundos a que se abra el Monitor Serie.
  // Si no hay conexión (uso de batería en el cohete), el programa 
  // rompe el bucle y arranca solo para no quedarse bloqueado.
  unsigned long ventanaInicio = millis();
  while (!Serial && millis() - ventanaInicio < 5000) {
    // Espera activa de cortesía para el USB
  }

  // Inicializar bus I2C y sensor SCD40
  Wire.begin();
  scd4x.begin(Wire, SCD41_I2C_ADDR_62);

  // Reinicio preventivo del sensor de CO2
  scd4x.stopPeriodicMeasurement();
  delay(500);
  scd4x.startPeriodicMeasurement();

  // Inicializar barómetro del Arduino (para la altitud)
  if (!BARO.begin()) {
    Serial.println(">>> ERROR: Barometro interno no detectado <<<");
  }

  // Calibración: Tomamos 20 muestras para fijar el "nivel del suelo" (0 metros)
  float sumaPress = 0;
  for(int i=0; i<20; i++) { 
    float p = BARO.readPressure();
    sumaPress += 44330.0 * (1.0 - pow(p / 1013.25, 0.1903));
    delay(50); 
  }
  altitudBase = sumaPress / 20.0;
  
  Serial.println("\n--- INICIO DE MEDICION EN TIEMPO REAL ---");
  Serial.println("Tiempo(s)\tAlt(m)\tCO2(ppm)\tTemp(C)\tHum(%)");
  Serial.println("------------------------------------------------------------");
}

void loop() {
  uint16_t co2 = 0;
  float t_scd = 0, h_scd = 0;
  bool datosListos = false;

  // Verificamos si el SCD40 tiene una nueva medición lista
  scd4x.getDataReadyStatus(datosListos);
  
  if (datosListos) {
    // Leemos las tres variables del SCD40 de una sola vez
    uint16_t error = scd4x.readMeasurement(co2, t_scd, h_scd);
    
    if (!error && co2 != 0) {
      // Calculamos la altitud actual comparándola con la base
      float p = BARO.readPressure();
      float altActual = (44330.0 * (1.0 - pow(p / 1013.25, 0.1903))) - altitudBase;

      // Imprimimos los datos en formato tabla
      Serial.print(millis() / 1000); Serial.print("s\t\t");
      Serial.print(altActual, 1);    Serial.print("\t");
      Serial.print(co2);             Serial.print("\t\t");
      Serial.print(t_scd, 1);        Serial.print("\t");
      Serial.println(h_scd, 1);
    }
  }
  
  // Pequeña pausa para no sobrecargar el procesador
  delay(100); 
}
