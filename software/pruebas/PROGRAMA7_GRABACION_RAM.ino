/*
 * ============================================
 * GRABACIÓN EN RAM - SOLO SENSORES INTERNOS REV2
 * Arduino Nano 33 BLE Sense
 * ============================================
 */

#include <Arduino_BMI270_BMM150.h>
#include <Arduino_HS300x.h>
#include <Arduino_LPS22HB.h>

// ============================================

#define MAX_REGISTROS 500
#define INTERVALO_GRABACION 1000

// ============================================

struct DatosSensor {
  uint32_t timestamp;
  int16_t temperatura;   // x100
  int16_t humedad;       // x100
  int16_t presion;       // hPa
  int16_t altitud;       // m
  int16_t accX, accY, accZ; // x100
};

DatosSensor registros[MAX_REGISTROS];

int numRegistros = 0;
bool grabando = false;
unsigned long tiempoInicio = 0;
unsigned long ultimaGrabacion = 0;

// ============================================

void setup() {

  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  delay(2000);

  Serial.println("CANSAT RAM REV2");

  if (!IMU.begin()) {
    Serial.println("Error IMU");
    while (1);
  }

  if (!HS300x.begin()) {
    Serial.println("Error Temp/Hum");
    while (1);
  }

  if (!BARO.begin()) {
    Serial.println("Error BARO");
    while (1);
  }

  Serial.println("Sensores OK");
  Serial.println("Comandos: GRABAR PARAR CSV BORRAR ESTADO");
}

// ============================================

void loop() {

  if (Serial.available()) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();
    comando.toUpperCase();
    procesarComando(comando);
  }

  if (grabando) {
    if (millis() - ultimaGrabacion >= INTERVALO_GRABACION) {
      ultimaGrabacion = millis();
      grabarRegistro();
    }

    digitalWrite(LED_BUILTIN, (millis() / 200) % 2);
  }
}

// ============================================

void procesarComando(String comando) {

  if (comando == "GRABAR") iniciarGrabacion();
  else if (comando == "PARAR") detenerGrabacion();
  else if (comando == "CSV") exportarCSV();
  else if (comando == "BORRAR") borrarDatos();
  else if (comando == "ESTADO") mostrarEstado();
}

// ============================================

void iniciarGrabacion() {
  if (grabando) return;

  grabando = true;
  tiempoInicio = millis();
  ultimaGrabacion = millis();

  Serial.println(">>> GRABANDO <<<");
}

void detenerGrabacion() {
  grabando = false;
  digitalWrite(LED_BUILTIN, LOW);
  Serial.println(">>> STOP <<<");
}

// ============================================

void grabarRegistro() {

  if (numRegistros >= MAX_REGISTROS) {
    Serial.println("RAM LLENA");
    detenerGrabacion();
    return;
  }

  DatosSensor d;
  d.timestamp = millis() - tiempoInicio;

  // --- temperatura humedad ---
  float temp = HS300x.readTemperature();
  float hum  = HS300x.readHumidity();

  // --- presión ---
  float pres = BARO.readPressure(); // hPa

  // --- altitud ---
  float alt = 44330.0 * (1.0 - pow(pres / 1013.25, 0.1903));

  // --- acelerómetro ---
  float x, y, z;
  IMU.readAcceleration(x, y, z);

  d.temperatura = temp * 100;
  d.humedad = hum * 100;
  d.presion = pres;
  d.altitud = alt;
  d.accX = x * 100;
  d.accY = y * 100;
  d.accZ = z * 100;

  registros[numRegistros++] = d;

  if (numRegistros % 10 == 0) {
    Serial.print("Registros: ");
    Serial.println(numRegistros);
  }
}

// ============================================

void exportarCSV() {

  Serial.println("t,temp,hum,pres,alt,ax,ay,az");

  for (int i = 0; i < numRegistros; i++) {
    DatosSensor d = registros[i];

    Serial.print(d.timestamp); Serial.print(",");
    Serial.print(d.temperatura / 100.0); Serial.print(",");
    Serial.print(d.humedad / 100.0); Serial.print(",");
    Serial.print(d.presion); Serial.print(",");
    Serial.print(d.altitud); Serial.print(",");
    Serial.print(d.accX / 100.0); Serial.print(",");
    Serial.print(d.accY / 100.0); Serial.print(",");
    Serial.print(d.accZ / 100.0); Serial.println(
