// ============================================
// PROGRAMA_APC220_EMISOR.ino
// Arduino Nano 33 BLE Sense Rev2
// 
// Emisor de telemetría por APC220
// ============================================
//
// DESCRIPCIÓN:
// Envía datos a través del módulo APC220 usando Serial1.
// Este programa es para probar la comunicación antes de
// integrar los sensores del CanSat.
//
// ============================================
// CONEXIÓN NANO 33 BLE - APC220
// ============================================
//
// IMPORTANTE: Las conexiones van DIRECTAS, no cruzadas.
// La etiqueta TXD/RXD del APC220 indica dónde conectar
// el pin del micro, no la función del módulo.
//
// Nano 33 BLE     APC220
// ─────────────────────────
// Pin 0 (RX)  →   RXD
// Pin 1 (TX)  →   TXD
// 3.3V        →   VCC
// GND         →   GND
//
// NOTA: El pin EN del APC220 puede dejarse sin conectar,
// funciona igualmente. Si usas Grove, no hay problema.
//
// ============================================

void setup() {
  Serial.begin(9600);   // USB (debug)
  Serial1.begin(9600);  // APC220 en pines 0 y 1
  delay(1000);
  Serial.println("Emisor APC220 listo...");
}

void loop() {
  Serial1.println("HOLA");
  Serial.println("Enviado: HOLA");  // Debug por USB
  delay(2000);
}
