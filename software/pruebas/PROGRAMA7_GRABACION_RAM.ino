/*
 * ============================================
 * CANSAT RAM - SOLO SENSORES INTERNOS REV2
 * Arduino Nano 33 BLE Sense
 * ============================================
 */

#include <Arduino_BMI270_BMM150.h>
#include <Arduino_HS300x.h>
#include <Arduino_LPS22HB.h>

#define MAX_REGISTROS 500
#define INTERVALO_GRABACION 1000

// ================= CONFIG =================
// AULA - Para pruebas en el aula
#define DESCENSO_INICIO 0.25 
#define ALT_ATERRIZAJE 0.1     
#define CICLOS_TRIGGER 3     // repetir 3 veces

// AULA - Para pruebas en el aula
//#define DESCENSO_INICIO 0.5
//#define CICLOS_TRIGGER 3
//#define ALT_ATERRIZAJE 0.3

// VUELO REAL
//#define DESCENSO_INICIO 8
//#define CICLOS_TRIGGER 6
//#define ALT_ATERRIZAJE 1.0

#define TIEMPO_ATERRIZAJE 5000

// ==========================================

struct DatosSensor {
  uint32_t timestamp;
  int16_t temperatura;
  int16_t humedad;
  int16_t presion;
  int16_t altitud;
  int16_t accX, accY, accZ;
};

DatosSensor registros[MAX_REGISTROS];

int numRegistros = 0;
bool grabando = false;
bool enDescenso = false;
bool aterrizado = false;

float altitudBase = 0;
float altitudMax = -1000;

int contadorDescenso = 0;
unsigned long tiempoInicio = 0;
unsigned long ultimaGrabacion = 0;
unsigned long tiempoPosibleAterrizaje = 0;

// ==========================================

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  delay(3000);

  IMU.begin();
  HS300x.begin();
  BARO.begin();

  Serial.println("CANSAT RAM MODO MISION");

  delay(3000);
  altitudBase = calcularAltitud();
}

// ==========================================

void loop() {

  if (!grabando) detectarDescenso();

  if (grabando) {
    if (millis() - ultimaGrabacion >= INTERVALO_GRABACION) {
      ultimaGrabacion = millis();
      grabarRegistro();
    }
    detectarAterrizaje();
    digitalWrite(LED_BUILTIN, (millis()/200)%2);
  }

  if (Serial.available()) {
    String c = Serial.readStringUntil('\n');
    c.trim(); c.toUpperCase();
    if (c=="CSV") exportarCSV();
    if (c=="BORRAR") numRegistros=0;
    if (c=="GRABAR") iniciarManual();
    if (c=="PARAR") detener();
  }
}

// ==========================================

float calcularAltitud(){
  float p = BARO.readPressure();
  return 44330.0 * (1.0 - pow(p/1013.25,0.1903));
}

// ==========================================
// DETECTAR DESCENSO (APOGEO)
// ==========================================

void detectarDescenso(){

  float alt = calcularAltitud();

  if (alt > altitudMax) altitudMax = alt;

  float bajada = altitudMax - alt;

  if (bajada > DESCENSO_INICIO){
    contadorDescenso++;
  } else {
    contadorDescenso = 0;
  }

  if (contadorDescenso >= CICLOS_TRIGGER){
    Serial.println(">>> DESCENSO DETECTADO <<<");
    iniciarAuto();
  }
}

// ==========================================

void iniciarAuto(){
  grabando = true;
  tiempoInicio = millis();
  ultimaGrabacion = millis();
}

// ==========================================

void iniciarManual(){
  grabando = true;
  tiempoInicio = millis();
  ultimaGrabacion = millis();
  Serial.println("MANUAL");
}

void detener(){
  grabando=false;
  Serial.println("STOP");
}

// ==========================================
// ATERRIZAJE
// ==========================================

void detectarAterrizaje(){

  float alt = calcularAltitud() - altitudBase;

  float x,y,z;
  IMU.readAcceleration(x,y,z);
  float a = sqrt(x*x+y*y+z*z);

  if (abs(alt) < ALT_ATERRIZAJE && abs(a-1.0)<0.05){
    if (tiempoPosibleAterrizaje==0)
      tiempoPosibleAterrizaje = millis();

    if (millis()-tiempoPosibleAterrizaje > TIEMPO_ATERRIZAJE){
      Serial.println(">>> ATERRIZAJE <<<");
      detener();
      aterrizado=true;
    }
  } else {
    tiempoPosibleAterrizaje=0;
  }
}

// ==========================================

void grabarRegistro(){

  if (numRegistros>=MAX_REGISTROS){
    detener();
    return;
  }

  DatosSensor d;
  d.timestamp = millis()-tiempoInicio;

  float t=HS300x.readTemperature();
  float h=HS300x.readHumidity();
  float p=BARO.readPressure();
  float alt=calcularAltitud();

  float x,y,z;
  IMU.readAcceleration(x,y,z);

  d.temperatura=t*100;
  d.humedad=h*100;
  d.presion=p;
  d.altitud=alt;
  d.accX=x*100;
  d.accY=y*100;
  d.accZ=z*100;

  registros[numRegistros++]=d;
}

// ==========================================

void exportarCSV(){

  Serial.println("t,temp,hum,pres,alt,ax,ay,az");

  for(int i=0;i<numRegistros;i++){
    auto d=registros[i];

    Serial.print(d.timestamp);Serial.print(",");
    Serial.print(d.temperatura/100.0);Serial.print(",");
    Serial.print(d.humedad/100.0);Serial.print(",");
    Serial.print(d.presion);Serial.print(",");
    Serial.print(d.altitud);Serial.print(",");
    Serial.print(d.accX/100.0);Serial.print(",");
    Serial.print(d.accY/100.0);Serial.print(",");
    Serial.print(d.accZ/100.0);Serial.println();
  }
}
