// ============================================
// PROGRAMA_APC220_RECEPTOR.ino
// Arduino UNO
// 
// Receptor de telemetría por APC220
// ============================================
//
// DESCRIPCIÓN:
// Recibe datos del módulo APC220 y los muestra por
// el monitor serie. Usar como estación de tierra
// para recibir telemetría del CanSat.
//
// ============================================
// CONEXIÓN ARDUINO UNO - APC220
// ============================================
//
// Arduino UNO     APC220
// ─────────────────────────
// GND         →   GND
// D13         →   VCC
// D12         →   EN
// D11         →   RXD
// D10         →   TXD
// D8          →   SET
//
// NOTA: Esta es la misma conexión usada para
// configurar el APC220. El Arduino alimenta
// y controla el módulo.
//
// ============================================

#include <SoftwareSerial.h>

#define PIN_VCC 13
#define PIN_EN 12
#define PIN_RXD 11
#define PIN_TXD 10
#define PIN_SET 8

SoftwareSerial apcSerial(PIN_TXD, PIN_RXD);

void setup() {
  pinMode(PIN_VCC, OUTPUT);
  pinMode(PIN_EN, OUTPUT);
  pinMode(PIN_SET, OUTPUT);
  
  digitalWrite(PIN_VCC, HIGH);
  digitalWrite(PIN_EN, HIGH);
  digitalWrite(PIN_SET, HIGH);  // Modo normal (no configuración)
  
  Serial.begin(9600);
  apcSerial.begin(9600);
  
  Serial.println("Receptor APC220 listo...");
  Serial.println("Esperando datos...");
  Serial.println("");
}

void loop() {
  if (apcSerial.available()) {
    char c = apcSerial.read();
    Serial.print(c);
  }
}
