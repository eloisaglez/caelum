// ============================================================================
// CANSAT - INTELIGENCIA DE VUELO + SEGURIDAD RAM
// ============================================================================
// COMANDOS:
// - PRUEBA: Para laboratorio (Umbral 0.5m).
// - CONCURSO: Para lanzamiento real (Umbral 2.5m).
// - CSV: Recupera toda la misión en formato Excel.
// - BORRAR: Limpia la RAM para un nuevo test.
// ============================================================================

#include <Arduino_BMI270_BMM150.h>
#include <Arduino_HS300x.h>
#include <Arduino_LPS22HB.h>

// --- CONFIGURACIÓN ---
#define INTERVALO_RAM 2000      // Backup en RAM cada 2 segundos
#define MAX_REGISTROS 350       // ~11 minutos de vuelo completo
#define UMBRAL_PRUEBA 0.5
#define UMBRAL_CONCURSO 2.5

float umbralActivacion = UMBRAL_PRUEBA; //Cambiar opr el que se necesite

struct DatosSensor {
  uint32_t timestamp;
  int16_t temperatura, humedad, altitud;
  int16_t accX, accY, accZ;
};

DatosSensor registros[MAX_REGISTROS];
int numRegistros = 0;
float altitudBase = 0, altitudMax = -1000;
bool grabando = false;
unsigned long ultimaGrabacion = 0;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  
  // ESPERA INTELIGENTE (Para arranque con batería en el campo)
  unsigned long ventana = millis();
  while (!Serial && millis() - ventana < 5000); 

  if (!IMU.begin() || !HS300x.begin() || !BARO.begin()) {
    Serial.println(F(">>> ERROR SENSORES <<<"));
    while (1);
  }

  // Calibración inicial
  float suma = 0;
  for(int i=0; i<20; i++) { suma += leerAltitud(); delay(50); }
  altitudBase = suma / 20.0;

  Serial.println(F("--- CANSAT FLIGHT SYSTEM READY ---"));
  imprimirEstado();
}

void loop() {
  float altActual = leerAltitud() - altitudBase;
  if (altActual > altitudMax) altitudMax = altActual;

  // 1. DETECCIÓN AUTOMÁTICA DE DESCENSO
  if (!grabando && (altitudMax - altActual > umbralActivacion) && altitudMax > 0.3) {
    iniciarGrabacion();
  }

  // 2. GESTIÓN DE COMANDOS
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim(); cmd.toUpperCase();
    
    if (cmd == "CONCURSO") { umbralActivacion = UMBRAL_CONCURSO; Serial.println(F("[MODO CONCURSO]")); }
    else if (cmd == "PRUEBA") { umbralActivacion = UMBRAL_PRUEBA; Serial.println(F("[MODO PRUEBA]")); }
    else if (cmd == "CSV") exportarCSV();
    else if (cmd == "BORRAR") { numRegistros = 0; grabando = false; altitudMax = -1000; Serial.println(F("RAM Limpia")); }
  }

  // 3. GRABACIÓN EN RAM (Caja Negra)
  if (grabando && numRegistros < MAX_REGISTROS) {
    if (millis() - ultimaGrabacion >= INTERVALO_RAM) {
      ultimaGrabacion = millis();
      
      float x, y, z;
      IMU.readAcceleration(x, y, z);

      registros[numRegistros].timestamp = millis();
      registros[numRegistros].temperatura = (int16_t)(HS300x.readTemperature() * 100);
      registros[numRegistros].humedad = (int16_t)(HS300x.readHumidity() * 100);
      registros[numRegistros].altitud = (int16_t)(altActual * 10);
      registros[numRegistros].accX = (int16_t)(x * 100);
      registros[numRegistros].accY = (int16_t)(y * 100);
      registros[numRegistros].accZ = (int16_t)(z * 100);
      
      numRegistros++;
      digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN)); // Parpadeo de grabación
    }
  }
}

void iniciarGrabacion() {
  grabando = true;
  Serial.println(F("\n!!! LANZAMIENTO DETECTADO: GRABANDO MISION !!!"));
}

float leerAltitud() {
  float p = BARO.readPressure();
  return 44330.0 * (1.0 - pow(p / 1013.25, 0.1903));
}

void imprimirEstado() {
  Serial.print(F("Umbral: ")); Serial.print(umbralActivacion); Serial.println("m");
  Serial.println(F("Comandos: CONCURSO, PRUEBA, CSV, BORRAR"));
}

void exportarCSV() {
  Serial.println(F("\nms,temp,hum,alt,accX,accY,accZ"));
  for (int i = 0; i < numRegistros; i++) {
    Serial.print(registros[i].timestamp); Serial.print(",");
    Serial.print(registros[i].temperatura / 100.0); Serial.print(",");
    Serial.print(registros[i].humedad / 100.0); Serial.print(",");
    Serial.print(registros[i].altitud / 10.0); Serial.print(",");
    Serial.print(registros[i].accX / 100.0); Serial.print(",");
    Serial.print(registros[i].accY / 100.0); Serial.print(",");
    Serial.println(registros[i].accZ / 100.0);
  }
  Serial.println(F("--- FIN DE DATOS ---"));
}
