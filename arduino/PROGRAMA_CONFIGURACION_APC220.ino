/*
 * ========================================================================
 * CONFIGURACIÓN APC220 - Arduino Nano 33 BLE Sense
 * ========================================================================
 * 
 * Programa para configurar el módulo APC220 directamente desde Arduino
 * sin necesidad de rfmagic en PC
 * 
 * Autor: CanSat Misión 2
 * Fecha: Enero 2026
 * Fuente: https://github.com/inopya/APC220_Transceiver
 * 
 * ========================================================================
 * CONEXIÓN APC220 ← → Arduino Nano 33 BLE
 * ========================================================================
 * 
 * Pines digitales (SoftwareSerial):
 *   D10 (RXD) ← APC220 TX (RXD)
 *   D11 (TXD) → APC220 RX (TXD)
 *   D8 (SET)  → APC220 SET (configuración)
 *   D9 (EN)   → APC220 EN (habilitado)
 *   D12 (AUX) ← APC220 AUX
 *   3.3V      → APC220 VCC
 *   GND       → APC220 GND
 * 
 * ========================================================================
 * PARÁMETROS DE CONFIGURACIÓN
 * ========================================================================
 * 
 * Formato: WR AAAAAA B C D E
 * 
 * AAAAAA = Frecuencia en KHz (418000-455000)
 *          434000 = 434 MHz (RECOMENDADO)
 * 
 * B = Velocidad RF
 *     1 = 2400 bps
 *     2 = 4800 bps
 *     3 = 9600 bps (RECOMENDADO)
 *     4 = 19200 bps
 * 
 * C = Potencia (0-9)
 *     0 = Mínima
 *     9 = Máxima (RECOMENDADO)
 * 
 * D = Velocidad Puerto Serie
 *     0 = 1200 bps
 *     1 = 2400 bps
 *     2 = 4800 bps
 *     3 = 9600 bps (RECOMENDADO)
 *     4 = 19200 bps
 *     5 = 38400 bps
 *     6 = 57600 bps
 * 
 * E = Paridad
 *     0 = Sin paridad (RECOMENDADO)
 *     1 = Paridad par
 *     2 = Paridad impar
 * 
 * EJEMPLO: WR 434000 3 9 3 0
 *   → Frecuencia 434 MHz
 *   → Velocidad RF 9600 bps
 *   → Potencia máxima
 *   → Puerto serie 9600 bps
 *   → Sin paridad
 * 
 * ========================================================================
 */

#include <SoftwareSerial.h>

// ========== CONFIGURACIÓN DE PINES ==========
#define SET      8      // Pin SET del APC220
#define EN       9      // Pin EN del APC220 (enable)
#define RXD      10     // RX (recibe datos del APC220)
#define TXD      11     // TX (envía datos al APC220)
#define AUX      12     // Pin AUX del APC220 (entrada)

// ========== PUERTO SERIE SOFTWARE PARA APC220 ==========
SoftwareSerial APCport(RXD, TXD);

// ========== VARIABLES ==========
String config_current = "";

void setup() {
  Serial.begin(9600);
  delay(2000);
  
  Serial.println();
  Serial.println("╔════════════════════════════════════════╗");
  Serial.println("║  Configuración APC220                 ║");
  Serial.println("║  Arduino Nano 33 BLE Sense            ║");
  Serial.println("╚════════════════════════════════════════╝");
  Serial.println();
  
  // Inicializar pines de control
  pinMode(SET, OUTPUT);
  pinMode(EN, OUTPUT);
  pinMode(AUX, INPUT);
  
  // Estados iniciales
  digitalWrite(SET, HIGH);      // Modo normal (no configuración)
  digitalWrite(EN, HIGH);       // Habilitado
  
  // Inicializar puerto serie software
  APCport.begin(9600);
  
  Serial.println("Inicializando APC220...");
  delay(500);
  
  // Esperar a que APC220 esté listo
  Serial.println();
  Serial.println("═══════════════════════════════════════════════════");
  Serial.println("Presiona una tecla para comenzar configuración:");
  Serial.println("  1 = Leer configuración actual");
  Serial.println("  2 = Escribir nueva configuración (434MHz, 9600bps, Pot max)");
  Serial.println("  3 = Ambas (leer, escribir, leer)");
  Serial.println("═══════════════════════════════════════════════════");
  Serial.println();
}

void loop() {
  // Limpiar buffer
  while (Serial.available() <= 0) {
    delay(100);
  }
  
  char opcion = Serial.read();
  
  Serial.println();
  Serial.println("═══════════════════════════════════════════════════");
  
  switch(opcion) {
    case '1':
      Serial.println("Leyendo configuración actual...");
      read_config();
      break;
      
    case '2':
      Serial.println("Escribiendo nueva configuración...");
      write_config();
      break;
      
    case '3':
      Serial.println("Leyendo configuración inicial...");
      read_config();
      delay(2000);
      
      Serial.println();
      Serial.println("Escribiendo nueva configuración...");
      write_config();
      delay(2000);
      
      Serial.println();
      Serial.println("Leyendo configuración final...");
      read_config();
      break;
      
    default:
      Serial.println("Opción no válida. Intenta de nuevo.");
      break;
  }
  
  Serial.println("═══════════════════════════════════════════════════");
  Serial.println();
  Serial.println("Presiona una tecla para continuar:");
  Serial.println("  1 = Leer configuración");
  Serial.println("  2 = Escribir configuración");
  Serial.println("  3 = Ambas");
  Serial.println();
}

// ========== FUNCIÓN: ESCRIBIR CONFIGURACIÓN ==========
void write_config() {
  Serial.println();
  Serial.println("▼ ESCRIBIENDO CONFIGURACIÓN:");
  Serial.println();
  
  // Poner en modo configuración
  digitalWrite(SET, LOW);
  delay(100);
  
  // Parámetros de configuración
  // WR AAAAAA B C D E
  // 434000 = 434 MHz
  // 3 = 9600 bps (velocidad RF)
  // 9 = Potencia máxima
  // 3 = 9600 bps (puerto serie)
  // 0 = Sin paridad
  
  String config_string = "WR 434000 3 9 3 0";
  
  Serial.print("Enviando: ");
  Serial.println(config_string);
  
  // Enviar comando
  APCport.print(config_string);
  APCport.write(0x0D);  // Carriage return
  APCport.write(0x0A);  // Line feed
  
  delay(200);
  
  // Volver a modo normal
  digitalWrite(SET, HIGH);
  
  Serial.println("✓ Configuración enviada");
  Serial.println();
  Serial.println("Parámetros escritos:");
  Serial.println("  • Frecuencia: 434 MHz");
  Serial.println("  • Velocidad RF: 9600 bps");
  Serial.println("  • Potencia: 9 (máxima)");
  Serial.println("  • Puerto serie: 9600 bps");
  Serial.println("  • Paridad: sin");
  Serial.println();
}

// ========== FUNCIÓN: LEER CONFIGURACIÓN ==========
void read_config() {
  Serial.println();
  Serial.println("▲ LEYENDO CONFIGURACIÓN:");
  Serial.println();
  
  // Limpiar buffer
  while (APCport.available()) {
    APCport.read();
  }
  
  // Poner en modo configuración
  digitalWrite(SET, LOW);
  delay(100);
  
  // Pedir lectura de configuración
  Serial.println("Enviando comando RD...");
  
  APCport.print("RD");
  APCport.write(0x0D);  // Carriage return
  APCport.write(0x0A);  // Line feed
  
  delay(300);
  
  // Leer respuesta
  Serial.print("Respuesta: ");
  
  config_current = "";
  
  unsigned long timeout = millis() + 2000;
  while (millis() < timeout) {
    if (APCport.available()) {
      char c = APCport.read();
      Serial.write(c);
      config_current += c;
    }
  }
  
  Serial.println();
  
  // Volver a modo normal
  digitalWrite(SET, HIGH);
  
  Serial.println();
  
  // Interpretar respuesta
  if (config_current.indexOf("PARAM") >= 0) {
    Serial.println("✓ Respuesta recibida correctamente");
    Serial.println();
    Serial.println("Parámetros leídos:");
    
    // Parsear respuesta
    int pos1 = config_current.indexOf("PARAM") + 6;
    int pos2 = config_current.indexOf(" ", pos1);
    
    if (pos2 > pos1) {
      String freq_str = config_current.substring(pos1, pos2);
      Serial.print("  • Frecuencia: ");
      Serial.print(freq_str);
      Serial.println(" KHz");
    }
  } else if (config_current.length() == 0) {
    Serial.println("❌ NO RECIBIDA respuesta");
    Serial.println();
    Serial.println("VERIFICA:");
    Serial.println("  1. APC220 conectado correctamente");
    Serial.println("  2. Pines D10, D11 conectados (RXD, TXD)");
    Serial.println("  3. Pines D8, D9 conectados (SET, EN)");
    Serial.println("  4. Alimentación 3.3V en APC220");
    Serial.println("  5. GND conectado");
  } else {
    Serial.println("⚠️ Respuesta incompleta o confusa");
    Serial.println("Dato recibido:");
    Serial.println(config_current);
  }
  
  Serial.println();
}
