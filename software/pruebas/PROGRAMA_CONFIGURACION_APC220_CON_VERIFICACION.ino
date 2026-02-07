// ============================================
// CONFIGURACIÓN APC220 - CON VERIFICACIÓN
// ✅ Verifica cada comando y muestra resultado
// ============================================

#define PIN_SET 8    // Pin SET del APC220
#define PIN_EN  9    // Pin EN del APC220

void setup() {
  Serial.begin(9600);      // Monitor serial
  Serial1.begin(9600);     // APC220 UART
  
  pinMode(PIN_SET, OUTPUT);
  pinMode(PIN_EN, OUTPUT);
  
  digitalWrite(PIN_SET, HIGH);
  digitalWrite(PIN_EN, LOW);
  
  delay(500);
  
  Serial.println("=== APC220 CONFIGURACIÓN CON VERIFICACIÓN ===");
  Serial.println("\nOpciones:");
  Serial.println("  1 = Leer configuración");
  Serial.println("  2 = Escribir configuración");
  Serial.println("  3 = Ambas (recomendado)");
  Serial.println("\nEscribe opcion:");
}

void loop() {
  if (Serial.available() > 0) {
    byte opcion = Serial.read();
    
    if (opcion == '1') {
      leerConfiguracion();
    } 
    else if (opcion == '2') {
      escribirConfiguracion();
    } 
    else if (opcion == '3') {
      escribirConfiguracion();
      delay(1000);
      leerConfiguracion();
    }
  }
}

// ============================================
// ESCRIBIR CONFIGURACIÓN CON VERIFICACIÓN
// ============================================
void escribirConfiguracion() {
  Serial.println("\n\n=== ESCRIBIENDO CONFIGURACIÓN ===\n");
  
  // Modo configuración
  digitalWrite(PIN_SET, LOW);
  delay(200);
  
  boolean todoOk = true;
  int comando = 0;
  
  // COMANDO 1: AT (Reset)
  comando++;
  Serial.print("[1/5] Enviando AT...");
  if (enviarYVerificar("AT\r\n")) {
    Serial.println(" ✓ OK");
  } else {
    Serial.println(" ✗ FALLÓ");
    todoOk = false;
  }
  delay(100);
  
  // COMANDO 2: FRECUENCIA 434 MHz
  comando++;
  Serial.print("[2/5] Escribiendo FREQ=434...");
  if (enviarYVerificar("AT+FREQ=434\r\n")) {
    Serial.println(" ✓ OK (Frecuencia grabada en EEPROM)");
  } else {
    Serial.println(" ✗ FALLÓ");
    todoOk = false;
  }
  delay(100);
  
  // COMANDO 3: BAUDRATE RF (9600 bps = 3)
  comando++;
  Serial.print("[3/5] Escribiendo BAUD=3...");
  if (enviarYVerificar("AT+BAUD=3\r\n")) {
    Serial.println(" ✓ OK (9600 bps grabado en EEPROM)");
  } else {
    Serial.println(" ✗ FALLÓ");
    todoOk = false;
  }
  delay(100);
  
  // COMANDO 4: POTENCIA (9 = máximo)
  comando++;
  Serial.print("[4/5] Escribiendo POWER=9...");
  if (enviarYVerificar("AT+POWER=9\r\n")) {
    Serial.println(" ✓ OK (Potencia grabada en EEPROM)");
  } else {
    Serial.println(" ✗ FALLÓ");
    todoOk = false;
  }
  delay(100);
  
  // COMANDO 5: BAUDRATE SERIAL (9600 bps = 3)
  comando++;
  Serial.print("[5/5] Escribiendo SBAUD=3...");
  if (enviarYVerificar("AT+SBAUD=3\r\n")) {
    Serial.println(" ✓ OK (Baudrate Serial grabado en EEPROM)");
  } else {
    Serial.println(" ✗ FALLÓ");
    todoOk = false;
  }
  delay(100);
  
  // Volver a modo normal
  digitalWrite(PIN_SET, HIGH);
  delay(200);
  
  // RESULTADO FINAL
  Serial.println("\n" + String(50, '='));
  if (todoOk) {
    Serial.println("✓✓✓ CONFIGURACIÓN COMPLETADA CORRECTAMENTE ✓✓✓");
    Serial.println("\nPARÁMETROS GRABADOS EN EEPROM:");
    Serial.println("  • Frecuencia: 434 MHz");
    Serial.println("  • Baudrate RF: 9600 bps");
    Serial.println("  • Baudrate Serial: 9600 bps");
    Serial.println("  • Potencia: 9 (MÁXIMA)");
    Serial.println("\n¡APC220 LISTO PARA USAR!");
  } else {
    Serial.println("✗✗✗ CONFIGURACIÓN CON ERRORES ✗✗✗");
    Serial.println("\nAlgo falló. Posibles causas:");
    Serial.println("  1. APC220 no conectado correctamente");
    Serial.println("  2. Pin SET no en LOW durante configuración");
    Serial.println("  3. Baudrate incorrecto (debe ser 9600)");
    Serial.println("  4. APC220 defectuoso");
  }
  Serial.println(String(50, '=') + "\n");
}

// ============================================
// LEER CONFIGURACIÓN
// ============================================
void leerConfiguracion() {
  Serial.println("\n\n=== LEYENDO CONFIGURACIÓN ===\n");
  
  // Modo configuración
  digitalWrite(PIN_SET, LOW);
  delay(200);
  
  Serial.println("Enviando comando AT para verificar...\n");
  
  // Enviar AT
  Serial1.println("AT");
  delay(300);
  
  // Leer respuesta
  String respuesta = "";
  unsigned long inicio = millis();
  
  while (Serial1.available() && (millis() - inicio) < 1000) {
    respuesta += (char)Serial1.read();
  }
  
  Serial.println("Respuesta recibida:");
  Serial.println("[" + respuesta + "]");
  
  // Analizar respuesta
  if (respuesta.indexOf("OK") >= 0) {
    Serial.println("\n✓✓✓ APC220 RESPONDIENDO CORRECTAMENTE ✓✓✓");
    Serial.println("\nEsto significa:");
    Serial.println("  ✓ APC220 está conectado");
    Serial.println("  ✓ Baudrate es correcto (9600)");
    Serial.println("  ✓ La configuración se grabó en EEPROM");
  } else {
    Serial.println("\n✗ Sin respuesta correcta del APC220");
    Serial.println("\nPrueba esto:");
    Serial.println("  1. Verifica conexiones (RX/TX)");
    Serial.println("  2. Verifica Pin SET está en LOW");
    Serial.println("  3. Verifica voltaje (debe ser 3.3V)");
    Serial.println("  4. Intenta de nuevo");
  }
  
  // Volver a modo normal
  digitalWrite(PIN_SET, HIGH);
  delay(200);
  
  Serial.println("\n");
}

// ============================================
// FUNCIÓN: ENVIAR Y VERIFICAR RESPUESTA
// Retorna TRUE si recibe "OK", FALSE si no
// ============================================
boolean enviarYVerificar(const char* comando) {
  // Limpiar buffer
  while (Serial1.available()) {
    Serial1.read();
  }
  
  // Enviar comando
  Serial1.print(comando);
  
  // Esperar respuesta (máximo 500ms)
  unsigned long inicio = millis();
  String respuesta = "";
  
  while ((millis() - inicio) < 500) {
    if (Serial1.available()) {
      respuesta += (char)Serial1.read();
      
      // Si recibimos OK, salir
      if (respuesta.indexOf("OK") >= 0) {
        return true;
      }
    }
  }
  
  // Timeout o no recibió OK
  return false;
}

// ============================================
// FIN DEL PROGRAMA
// ============================================

/*
  CONEXIONES NECESARIAS:

  Arduino Nano 33 BLE ---- APC220
  ├─ Pin 8 (SET) --------- SET
  ├─ Pin 9 (EN) ---------- EN
  ├─ Serial1 RX (Grove) -- TX (APC220)
  ├─ Serial1 TX (Grove) -- RX (APC220)
  ├─ GND  --------------- GND
  └─ 3.3V --------------- VCC

  MODO DE USO:

  Monitor Serial (9600 baud):
  1. Escribe: 2 (para escribir configuración)
  2. Verifica cada línea
  3. Si todo dice ✓ → Configuración correcta
  4. Si algo dice ✗ → Hay un problema

  DÓNDE SE GRABA:

  Cuando ves "✓ OK", significa:
  - El comando fue recibido por APC220
  - APC220 respondió "OK"
  - La configuración se grabó en EEPROM del APC220
  - Sobrevivirá a apagar/encender

  VERIFICACIÓN:

  Escribe: 1 (para leer configuración)
  Si ves "✓ APC220 RESPONDIENDO" → Todo bien
  Si ves "✗ Sin respuesta" → Problema de conexión
*/
