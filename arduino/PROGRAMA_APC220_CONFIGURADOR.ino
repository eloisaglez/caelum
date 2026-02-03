// ============================================
// PROGRAMA_APC220_CONFIGURADOR.ino
// Arduino UNO
// 
// Configuración APC220
// ============================================
//
// DESCRIPCIÓN:
// Permite leer y escribir la configuración del módulo
// APC220 desde el monitor serie del Arduino IDE.
//
// NOTA: Otros métodos como rfmagic, PuTTY o terminales
// serie no funcionaron. Este método con Arduino UNO
// como intermediario sí funciona correctamente.
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
// IMPORTANTE: Conectar la antena antes de encender.
// Sin antena el módulo puede ser inestable.
//
// ============================================
// COMANDOS (escribir en monitor serie a 9600 baud)
// ============================================
//
// RD                    → Leer configuración actual
// WR 434000 3 9 3 0     → Escribir configuración
//
// ============================================
// FORMATO COMANDO WR
// ============================================
//
// WR FFFFFF V P S C
//
// FFFFFF = Frecuencia en KHz (418000 - 455000)
// V = Velocidad RF: 1=2400, 2=4800, 3=9600, 4=19200 bps
// P = Potencia: 0=mínima, 9=máxima
// S = Puerto serie: 0=1200, 1=2400, 2=4800, 3=9600, 4=19200, 5=38400, 6=57600 bps
// C = Paridad: 0=ninguna, 1=par, 2=impar
//
// Configuración recomendada: WR 434000 3 9 3 0
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
  digitalWrite(PIN_SET, HIGH);
  
  delay(1000);
  
  Serial.begin(9600);
  apcSerial.begin(9600);
  
  delay(500);
  
  Serial.println("");
  Serial.println("========================================");
  Serial.println("  APC220 - CONFIGURADOR");
  Serial.println("========================================");
  Serial.println("");
  Serial.println("Comandos:");
  Serial.println("  RD                   -> Leer config");
  Serial.println("  WR 434000 3 9 3 0    -> Escribir config");
  Serial.println("");
  Serial.println("========================================");
  Serial.println("");
  
  Serial.println("Configuracion actual:");
  leerConfiguracion();
}

void loop() {
  if (Serial.available()) {
    digitalWrite(PIN_SET, LOW);
    delay(50);
    
    String comando = Serial.readStringUntil('\n');
    comando.trim();
    
    apcSerial.print(comando);
    apcSerial.write(0x0D);
    apcSerial.write(0x0A);
    
    Serial.print("Enviado: ");
    Serial.println(comando);
    
    delay(100);
    
    Serial.print("Respuesta: ");
    while (apcSerial.available()) {
      Serial.write(apcSerial.read());
    }
    Serial.println("");
    
    digitalWrite(PIN_SET, HIGH);
  }
}

void leerConfiguracion() {
  digitalWrite(PIN_SET, LOW);
  delay(50);
  
  apcSerial.print("RD");
  apcSerial.write(0x0D);
  apcSerial.write(0x0A);
  
  delay(100);
  
  while (apcSerial.available()) {
    Serial.write(apcSerial.read());
  }
  Serial.println("");
  
  digitalWrite(PIN_SET, HIGH);
}
