#include <Wire.h>

void setup() {
  Serial.begin(9600);
  delay(2000);
  Wire.begin();
  
  Serial.println("Buscando HM3301 en I2C...");
  Serial.println("Dirección esperada: 0x40");
  Serial.println();
  
  byte count = 0;
  for(byte i = 8; i < 120; i++) {
    Wire.beginTransmission(i);
    if(Wire.endTransmission() == 0) {
      Serial.print("✓ Encontrado en: 0x");
      if(i < 16) Serial.print("0");
      Serial.println(i, HEX);
      
      if(i == 0x40) {
        Serial.println("  → ¡Este es el HM3301!");
      }
      if(i == 0x62) {
        Serial.println("  → Este es el SCD40 (CO2)");
      }
      count++;
    }
  }
  
  if(count == 0) {
    Serial.println("❌ No se encontraron dispositivos I2C");
  }
}

void loop() {
  delay(10000);
}