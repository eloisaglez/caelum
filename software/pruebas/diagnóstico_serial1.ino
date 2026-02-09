/*
 * PROGRAMA DE DIAGNÓSTICO PARA SERIAL1 (PINES 0 y 1)
 */
#include <Arduino.h>

void setup() {
  // Comunicación con el PC
  Serial.begin(115200);
  while (!Serial);

  // Comunicación con el GPS en pines 0 (RX) y 1 (TX)
  // PRUEBA 1: Empezamos con 9600
  Serial1.begin(9600); 

  Serial.println("--- INICIANDO DIAGNÓSTICO SERIAL1 ---");
  Serial.println("Escuchando pines RX(0) y TX(1)...");
}

void loop() {
  if (Serial1.available()) {
    char c = Serial1.read();
    Serial.write(c); // Manda al PC exactamente lo que llega del GPS
  }
}
