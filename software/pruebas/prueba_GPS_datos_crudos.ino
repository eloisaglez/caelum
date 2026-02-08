/*
 * TEST SIMPLE: GPS -> PC
 * Placa: Arduino Nano 33 BLE Sense
 * Conexión:
 * GPS TX  -> Arduino RX (Pin 0)
 * GPS RX  -> Arduino TX (Pin 1)
 * GPS VCC -> 3.3V 
 * GPS GND -> GND
 */

void setup() {
  // 1. Iniciar comunicación con el Ordenador
  Serial.begin(115200);

  // --- PROTECCIÓN ANTIBLOQUEO (IMPORTANTE) ---
  // Esperamos 5 segundos antes de activar el puerto del GPS.
  // Esto te da tiempo a abrir el monitor serie y evita que el
  // GPS bloquee el arranque del USB.
  for(int i = 10; i > 0; i--) {
    Serial.print("Iniciando prueba GPS en... ");
    Serial.println(i);
    delay(1000);
  }
  Serial.println("--- ACTIVANDO PUERTO GPS ---");

  // 2. Iniciar comunicación con el GPS (Pines 0 y 1)
  // La mayoría de módulos GPS vienen a 9600 baudios por defecto.
  Serial1.begin(9600); 
}

void loop() {
  // Si el GPS manda algo, lo mostramos en la pantalla del PC
  if (Serial1.available()) {
    char c = Serial1.read();
    Serial.write(c);
  }

  // (Opcional) Si tú escribes algo en el PC, se lo mandamos al GPS
  // Esto sirve si quisieras configurar el GPS con comandos.
  if (Serial.available()) {
    char c = Serial.read();
    Serial1.write(c);
  }
}