// ============================================================
// DIAGNÓSTICO MicroSD - Adafruit + Arduino Nano 33 BLE
// Carga esto y abre Serial Monitor a 9600 baud
// ============================================================
#include "SdFat.h"

#define SD_CS_PIN  10
SdFat sd;
SdFile testFile;

void setup() {
  Serial.begin(9600);
  while (!Serial) delay(10);
  
  Serial.println("=== DIAGNÓSTICO MICROSD ===");
  Serial.println("");

  // PASO 1 - Verificar que SPI está activo
  Serial.println("PASO 1: Iniciando SPI...");
  SPI.begin();
  delay(100);
  Serial.println("  SPI OK");

  // PASO 2 - Intentar inicializar SD a velocidad muy baja
  Serial.println("PASO 2: Intentando SD a 1MHz...");
  if (!sd.begin(SD_CS_PIN, SD_SCK_MHZ(1))) {
    Serial.println("  ❌ FALLO a 1MHz");
    Serial.println("  Causa probable:");
    Serial.println("  - Tarjeta no insertada correctamente");
    Serial.println("  - VCC conectado a 5V en lugar de 3.3V");
    Serial.println("  - CS no está en D10");
    Serial.println("  - Tarjeta dañada o formato incorrecto");
    Serial.println("  - Tarjeta >32GB en exFAT (necesita FAT32)");
    while(1);
  }
  Serial.println("  ✅ SD detectada a 1MHz!");

  // PASO 3 - Info de la tarjeta
  Serial.println("PASO 3: Leyendo info de la tarjeta...");
  uint32_t cardSize = sd.card()->sectorCount();
  Serial.print("  Tamaño: ");
  Serial.print(cardSize / 2048);
  Serial.println(" MB");
  
  // PASO 4 - Verificar sistema de archivos
  Serial.println("PASO 4: Verificando sistema de archivos...");
  if (sd.fatType() == FAT_TYPE_EXFAT) {
    Serial.println("  ❌ Tarjeta en exFAT - reformatear en FAT32");
    while(1);
  }
  Serial.print("  Tipo: FAT");
  Serial.println(sd.fatType());
  Serial.println("  ✅ Sistema de archivos OK");

  // PASO 5 - Crear archivo de prueba
  Serial.println("PASO 5: Creando archivo test.txt...");
  if (!testFile.open("test.txt", O_WRONLY | O_CREAT | O_TRUNC)) {
    Serial.println("  ❌ No se pudo crear archivo");
    while(1);
  }
  testFile.println("Caelum I - Test OK");
  testFile.close();
  Serial.println("  ✅ Archivo creado correctamente");

  Serial.println("");
  Serial.println("✅✅ MICROSD FUNCIONA PERFECTAMENTE ✅✅");
  Serial.println("Puedes usar la SD en tu proyecto.");
}

void loop() {}