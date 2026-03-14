#include <SoftwareSerial.h>

// Definiciones según tu esquema
#define PIN_SET 8
#define PIN_RXD 10 
#define PIN_TXD 11 
#define PIN_EN  12 
#define PIN_VCC 13

SoftwareSerial APCport(PIN_RXD, PIN_TXD);

void setup() {
  // Comunicación con la PC
  Serial.begin(9600);
  
  // Configuración de pines de control
  pinMode(PIN_SET, OUTPUT);
  pinMode(PIN_EN, OUTPUT);
  pinMode(PIN_VCC, OUTPUT);
  
  // Encendido del módulo
  digitalWrite(PIN_VCC, HIGH);
  digitalWrite(PIN_EN, HIGH);
  digitalWrite(PIN_SET, HIGH); 
  
  delay(2000); // Espera para que el módulo inicie correctamente
  
  APCport.begin(9600);
  
  Serial.println(F("--- LEYENDO CONFIGURACIÓN DEL APC220 ---"));
  
  // Entrar en modo comando
  digitalWrite(PIN_SET, LOW);
  delay(200);
  
  // Enviar comando de lectura (Read)
  APCport.print("RD\r\n");
  
  // Pequeña espera para recibir los datos
  delay(500); 
  
  // Mostrar lo que responda el módulo
  if (APCport.available()) {
    Serial.print(F("Respuesta recibida: "));
    while (APCport.available()) {
      Serial.write(APCport.read()); 
    }
    Serial.println();
  } else {
    Serial.println(F("ERROR: El módulo no respondió."));
  }
  
  // Volver a modo normal (SET en HIGH)
  digitalWrite(PIN_SET, HIGH);
  Serial.println(F("---------------------------------------"));
}

void loop() {
  // No hace falta repetir el proceso
}