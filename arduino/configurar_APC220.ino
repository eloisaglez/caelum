// ============================================
// PROGRAMA_APC220_SIMPLE.ino
// Arduino UNO
// 
// Configuración APC220 - VERSIÓN SIMPLE
// 
// CONEXIÓN:
// Arduino Pin 13 → APC220 VCC
// Arduino Pin 12 → APC220 EN
// Arduino Pin 11 → APC220 RXD
// Arduino Pin 10 → APC220 TXD
// Arduino Pin 9  → APC220 AUX
// Arduino Pin 8  → APC220 SET
// Arduino GND → APC220 GND
// ============================================

#include <SoftwareSerial.h>

// Definir pines
#define PIN_VCC 13
#define PIN_EN 12
#define PIN_RXD 11
#define PIN_TXD 10
#define PIN_AUX 9
#define PIN_SET 8

// SoftwareSerial para APC220 (igual que programa referencia)
SoftwareSerial apcSerial(PIN_TXD, PIN_RXD);

void setup() {
  // Configurar pines como OUTPUT/INPUT
  pinMode(PIN_VCC, OUTPUT);
  pinMode(PIN_EN, OUTPUT);
  pinMode(PIN_SET, OUTPUT);
  pinMode(PIN_AUX, INPUT);
  
  // Encender APC220
  digitalWrite(PIN_VCC, HIGH);
  digitalWrite(PIN_EN, HIGH);
  digitalWrite(PIN_SET, HIGH);      // Modo normal inicialmente
  
  delay(1000);
  
  // Inicializar comunicación
  Serial.begin(9600);
  apcSerial.begin(9600);
  
  delay(500);
  
  // Mensajes iniciales
  Serial.println("");
  Serial.println("╔════════════════════════════════════════╗");
  Serial.println("║  APC220 - CONFIGURADOR                ║");
  Serial.println("║  Modo: NORMAL                         ║");
  Serial.println("╚════════════════════════════════════════╝");
  Serial.println("");
  Serial.println("Comandos:");
  Serial.println("  AT           → Verificar conexión");
  Serial.println("  RD           → Leer configuración");
  Serial.println("  WR 434000 3 9 3 0  → Escribir configiguración nueva");
  Serial.println("");
  Serial.println("════════════════════════════════════════");
  Serial.println("");
  
  // Verificar conexión automáticamente
  Serial.println("Verificando conexión...\n");
  verificarConexion();
  
  // Leer configuración actual
  Serial.println("\nLeyendo configuración actual...\n");
  leerConfiguracion();
}

void loop() {
  // PC → APC220 (modo configuración para comandos)
  if (Serial.available()) {
    digitalWrite(PIN_SET, LOW);     // Entrar en modo configuración
    delay(50);
    
    String comando = Serial.readStringUntil('\n');
    comando.trim();
    
    apcSerial.print(comando);
    apcSerial.write(0x0D);
    apcSerial.write(0x0A);
    
    Serial.print("Enviado: ");
    Serial.println(comando);
    
    delay(100);
    
    // Leer respuesta
    while (apcSerial.available()) {
      Serial.write(apcSerial.read());
    }
    
    digitalWrite(PIN_SET, HIGH);    // Volver a modo normal
  }
  
  // APC220 → PC (para datos en modo normal)
  if (apcSerial.available()) {
    Serial.write(apcSerial.read());
  }
}

// Función para verificar conexión
void verificarConexion() {
  digitalWrite(PIN_SET, LOW);       // Modo configuración
  delay(50);
  
  apcSerial.print("RD");            // Usamos RD en lugar de AT
  apcSerial.write(0x0D);
  apcSerial.write(0x0A);
  
  delay(100);
  
  String respuesta = "";
  while (apcSerial.available()) {
    respuesta += (char)apcSerial.read();
  }
  
  digitalWrite(PIN_SET, HIGH);      // Volver a modo normal
  
  if (respuesta.indexOf("PARA") >= 0) {
    Serial.println("✅ CONEXIÓN OK - APC220 responde correctamente");
    Serial.print("   ");
    Serial.println(respuesta);
  } else if (respuesta.length() > 0) {
    Serial.print("⚠️ Respuesta: ");
    Serial.println(respuesta);
  } else {
    Serial.println("❌ SIN RESPUESTA - Verificar conexión");
    Serial.println("");
    Serial.println("Posibles causas:");
    Serial.println("  1. Pines invertidos");
    Serial.println("  2. Velocidad incorrecta");
    Serial.println("  3. APC220 sin alimentación");
    Serial.println("  4. Cable dañado");
  }
  
  Serial.println("");
}

// Función para leer configuración
void leerConfiguracion() {
  digitalWrite(PIN_SET, LOW);       // Modo configuración
  delay(50);
  
  apcSerial.print("RD");
  apcSerial.write(0x0D);
  apcSerial.write(0x0A);
  
  delay(100);
  
  Serial.print("Configuración: ");
  while (apcSerial.available()) {
    Serial.write(apcSerial.read());
  }
  Serial.println("");
  
  digitalWrite(PIN_SET, HIGH);      // Volver a modo normal
}

// ============================================
// CONFIGURACIÓN APC220:
//
// COMANDO ESCRIBIR:
// WR 434000 3 9 3 0
//
// Parámetros:
// • 434000 = Frecuencia 434 MHz
// • 3 = Velocidad RF: 9600 bps
// • 9 = Potencia: MÁXIMA
// • 3 = Velocidad Serial: 9600 bps
// • 0 = Paridad: Ninguna
//
// COMANDO LEER:
// RD
//
// Respuesta esperada:
// PARAM 434000 3 9 3 0
//
// ============================================
