#include <Wire.h>
#define SDA_PIN PIN_WIRE_SDA
#define SCL_PIN PIN_WIRE_SCL

void liberarBus() {
  pinMode(SCL_PIN, OUTPUT);
  pinMode(SDA_PIN, INPUT_PULLUP);
  // 9 pulsos de reloj para liberar un esclavo atascado
  for (int i = 0; i < 9; i++) {
    digitalWrite(SCL_PIN, LOW);
    delayMicroseconds(5);
    digitalWrite(SCL_PIN, HIGH);
    delayMicroseconds(5);
  }
}

void setup() {
  Serial.begin(115200);
  unsigned long t0 = millis();
  while (!Serial && millis() - t0 < 3000) {}
  Serial.println("Liberando bus I2C...");
  liberarBus();
  Wire.begin();
  Wire.setClock(100000);
  Serial.println("Listo. Ahora vuelve a cargar el escaner doble.");
}

void loop() {}