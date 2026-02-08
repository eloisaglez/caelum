/*
 * =========================================================================
 * PROYECTO CANSAT RAM - PRUEBA DE SENSORES AMBIENTAL SCD40
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
#include <Wire.h>

void setup() {
  Wire.begin();
  Serial.begin(9600);
  while (!Serial);
  Serial.println("\nI2C Scanner");
}

void loop() {
  byte error, address;
  int nDevices = 0;
  for(address = 1; address < 127; address++ ) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    if (error == 0) {
      Serial.print("Dispositivo encontrado en direccion 0x");
      if (address<16) Serial.print("0");
      Serial.println(address,HEX);
      nDevices++;
    }
  }
  if (nDevices == 0) Serial.println("No se encontraron dispositivos I2C\n");
  delay(5000);
}