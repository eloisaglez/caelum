#include <Arduino.h>

// ============================================
// PROGRAMA_APC220_EMISOR.ino
// Arduino Nano 33 BLE Sense Rev2
// ============================================
//
// CONEXIÓN NANO 33 BLE - APC220 (Pines 2 y 3)
// ============================================
//
// Nano 33 BLE      APC220
// ─────────────────────────
// Pin 2 (RX)  →    TXD (o el pin que envía datos del APC)
// Pin 3 (TX)  →    RXD (o el pin que recibe datos en el APC)
// 3.3V        →    VCC
// GND         →    GND
// ============================================

// En el Nano 33 BLE definimos un nuevo puerto Hardware UART.
// Sintaxis: UART(Pin_TX, Pin_RX);
// Configuración: TX en D3, RX en D2
//NOTA: El pin EN del APC220 puede dejarse sin conectar,
// funciona igualmente. Si usas Grove, no hay problema.

UART ApcSerial(3, 2); 

void setup() {
  Serial.begin(9600);   // USB (debug)
  
  // Iniciamos nuestro nuevo puerto en pines 2 y 3
  ApcSerial.begin(9600); 
  
  delay(1000);
  Serial.println("Emisor APC220 listo en pines 2 y 3...");
}

void loop() {
  // Enviamos por el puerto nuevo (pines 2 y 3)
  ApcSerial.println("HOLA");
  
  // Mensaje de control por USB
  Serial.println("Enviado: HOLA");  
  
  delay(2000);
}
