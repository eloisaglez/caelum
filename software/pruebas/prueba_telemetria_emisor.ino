// ============================================
// PROYECTO: CanSat - Prueba de Telemetría
// PLACA: Arduino Nano 33 BLE Sense
// CONEXIÓN APC220: TXD -> D2, RXD -> D3 [Modificado para evitar conflictos con carga]
// ============================================

/* * ⚠️ NOTA IMPORTANTE PARA EL LABORATORIO:
 * Estamos usando la conexión CRUZADA por defecto (D2 a TX y D3 a RX).
 * SI NO SE RECIBE NADA EN EL MONITOR SERIE:
 * - Poner la conexión DIRECTA (D2 con RX y D3 con TX).
 * Dependiendo de cómo esté etiquetado tu módulo APC220, 
 * funcionará de una forma o de la otra. COMPRUÉBALO SIEMPRE.
 */


#include <SoftwareSerial.h>

// Definimos los pines para la antena (RX=2, TX=3)
SoftwareSerial apcSerial(2, 3); 

void setup() {
  Serial.begin(9600);    // Puerto USB para ver mensajes en el PC [cite: 86]
  apcSerial.begin(9600); // Puerto para la antena APC220 [cite: 86]
  
  delay(1000);
  Serial.println("Emisor APC220 listo en pines D2 y D3...");
}

void loop() {
  // Enviamos el mensaje a través de la antena
  apcSerial.println("HOLA"); 
  
  // Mostramos en el PC lo que se acaba de enviar
  Serial.println("Enviado por antena: HOLA"); 
  
  delay(2000); // Espera 2 segundos entre envíos [cite: 88]
}