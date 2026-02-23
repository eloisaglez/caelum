/*
 * TEST GPS EN Serial1 (pines D0/D1)
 * Arduino Nano 33 BLE Sense Rev2
 * 
 * Conexiones GPS:
 *   TX GPS → Pin 0 (RX)
 *   RX GPS → Pin 1 (TX)
 *   VCC    → 3.3V
 *   GND    → GND
 *   EN     → 3.3V
 */

#include <Arduino.h>

void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial1.begin(9600);
  Serial.println("Escuchando GPS en Serial1 (pines 0/1)...");
}

void loop() {
  while (Serial1.available()) {
    Serial.write(Serial1.read());
  }
}
