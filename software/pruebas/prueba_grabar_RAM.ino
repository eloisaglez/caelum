// =====================================================
// TEST_RAM_MINIMO.ino - Solo para probar la memoria
// =====================================================

#include <Arduino_HS300x.h> // Solo usamos un sensor para el test

#define MAX_REGISTROS 100
int numRegistros = 0;
float registros[MAX_REGISTROS]; // Array simple de temperaturas

void setup() {
  Serial.begin(9600);
  while (!Serial); 
  
  if (!HS300x.begin()) {
    Serial.println("Error sensor");
    while (1);
  }

  Serial.println("--- TEST RAM ---");
  Serial.println("Envia 'G' para GRABAR 100 datos");
  Serial.println("Envia 'V' para VER los datos");
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();

    if (c == 'G') {
      numRegistros = 0;
      Serial.println("Grabando...");
      for (int i = 0; i < MAX_REGISTROS; i++) {
        registros[i] = HS300x.readTemperature();
        delay(100); // Graba rápido para el test
      }
      Serial.println("¡Hecho! Escribe 'V' para verlos.");
    }

    if (c == 'V') {
      Serial.println("Datos guardados en RAM:");
      for (int i = 0; i < MAX_REGISTROS; i++) {
        Serial.print("Dato "); Serial.print(i);
        Serial.print(": "); Serial.println(registros[i]);
      }
    }
  }
}