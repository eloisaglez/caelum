/*
 * ========================================================================
 * PROGRAMA 3: GPS - POSICIÓN Y ALTITUD
 * ========================================================================
 * 
 * Autor: CanSat Misión 2
 * Fecha: Enero 2026
 * Proyecto: CanSat Misión 2
 * 
 * SENSOR: ATGM336H (o compatible NEO-6M/7M/8M)
 * FUNCIÓN: Latitud, Longitud, Altitud, Número de satélites
 * 
 * CONEXIÓN (SoftwareSerial):
 *   D2 (RX) ← GPS TX
 *   D4 (TX) → GPS RX
 *   3.3V → GPS VCC
 *   GND → GND
 * 
 * OBJETIVO: Obtener posición georreferenciada
 * 
 * ========================================================================
 */

#include <SoftwareSerial.h>

// Crear puerto serial por software
// D2 = RX, D4 = TX
SoftwareSerial gpsSerial(2, 4);

// Variables GPS
String gpsData = "";
float gps_lat = 0.0, gps_lon = 0.0;
float gps_alt = 0.0;
int gps_satellites = 0;
boolean gps_fix = false;

int contador = 0;
unsigned long lastFixTime = 0;

void setup() {
  Serial.begin(9600);
  gpsSerial.begin(9600);
  delay(2000);
  
  Serial.println();
  Serial.println("╔════════════════════════════════════════╗");
  Serial.println("║  Programa 3: GPS                       ║");
  Serial.println("║  Posición + Altitud + Satélites       ║");
  Serial.println("╚════════════════════════════════════════╝");
  Serial.println();
  Serial.println("⏳ Esperando señal GPS...");
  Serial.println("(Puede tardar 2-5 minutos en EXTERIOR)");
  Serial.println();
  Serial.println("Asegúrate de que:");
  Serial.println("  • Antena GPS apunta AL CIELO");
  Serial.println("  • Sin obstáculos (árboles/edificios)");
  Serial.println("  • Está conectado correctamente");
  Serial.println();
}

void loop() {
  // LEER DATOS GPS
  while (gpsSerial.available()) {
    char c = gpsSerial.read();
    gpsData += c;
    
    if (c == '\n') {
      parseGPS(gpsData);
      gpsData = "";
    }
  }
  
  // MOSTRAR ESTADO
  if (contador % 20 == 0) {
    Serial.println();
    if (gps_fix) {
      Serial.println("N° | Status | Sat | Lat | Lon | Alt | Fix_Time");
      Serial.println("───┼────────┼─────┼─────┼─────┼─────┼──────────");
    } else {
      Serial.println("N° | Status | Sat");
      Serial.println("───┼────────┼─────");
    }
  }
  
  Serial.print(contador);
  Serial.print(" | ");
  
  if (gps_fix) {
    Serial.print("✓ FIX  | ");
  } else {
    Serial.print("⏳ Wait | ");
  }
  
  // Satélites
  Serial.print(gps_satellites);
  Serial.print("  | ");
  
  if (gps_fix) {
    // Mostrar posición
    Serial.print(gps_lat, 4);
    Serial.print(" | ");
    Serial.print(gps_lon, 4);
    Serial.print(" | ");
    Serial.print(gps_alt, 1);
    Serial.print("m | ");
    Serial.print((millis() - lastFixTime) / 1000);
    Serial.print("s");
  }
  
  Serial.println();
  
  contador++;
  delay(1000);
}

void parseGPS(String sentence) {
  if (sentence.length() < 6) return;
  
  if (sentence.startsWith("$GNGGA") || sentence.startsWith("$GPGGA")) {
    parseGGA(sentence);
  } else if (sentence.startsWith("$GNRMC") || sentence.startsWith("$GPRMC")) {
    parseRMC(sentence);
  }
}

void parseRMC(String sentence) {
  int commaCount = 0;
  int lastIndex = 0;
  
  for (int i = 0; i < sentence.length(); i++) {
    if (sentence[i] == ',' || sentence[i] == '\n') {
      String field = sentence.substring(lastIndex, i);
      
      if (commaCount == 2) {
        gps_fix = (field == "A");
        if (gps_fix) {
          lastFixTime = millis();
        }
      } else if (commaCount == 3) {
        gps_lat = parseCoordinate(field);
      } else if (commaCount == 5) {
        gps_lon = parseCoordinate(field);
      }
      
      lastIndex = i + 1;
      commaCount++;
    }
  }
}

void parseGGA(String sentence) {
  int commaCount = 0;
  int lastIndex = 0;
  
  for (int i = 0; i < sentence.length(); i++) {
    if (sentence[i] == ',' || sentence[i] == '\n') {
      String field = sentence.substring(lastIndex, i);
      
      if (commaCount == 7) {
        gps_satellites = field.toInt();
      } else if (commaCount == 9) {
        if (field.length() > 0) {
          gps_alt = field.toFloat();
        }
      }
      
      lastIndex = i + 1;
      commaCount++;
    }
  }
}

float parseCoordinate(String coord) {
  if (coord.length() < 5) return 0.0;
  
  int dotIndex = coord.indexOf('.');
  int degreeDigits = dotIndex - 2;
  
  if (degreeDigits <= 0) return 0.0;
  
  float degrees = coord.substring(0, degreeDigits).toFloat();
  float minutes = coord.substring(degreeDigits).toFloat();
  
  return degrees + (minutes / 60.0);
}

/*
 * ========================================================================
 * TIEMPOS DE OBTENCIÓN DE FIX:
 * 
 * PRIMER ENCENDIDO (Cold Start):
 *   ⏱️ 2-5 MINUTOS
 *   Requiere: Exterior, sin obstáculos
 * 
 * ENCENDIMIENTO POSTERIOR (Warm Start):
 *   ⏱️ 30-60 segundos
 *   Mejor si está en misma ubicación
 * 
 * ENCENDIMIENTO CON ÚLTIMA POSICIÓN (Hot Start):
 *   ⏱️ 5-15 segundos
 * 
 * ========================================================================
 * SATÉLITES NECESARIOS:
 * 
 * 0 satélites      ❌ Sin fix (buscando)
 * 3 satélites      ⚠️ Fix débil (evitar)
 * 4-5 satélites    ✓ Fix normal
 * 6-10 satélites   ✓✓ Fix excelente
 * 
 * ========================================================================
 * PRECISIÓN GPS:
 * 
 * Latitud/Longitud: ±5-30 metros típicamente
 * Altitud:          ±10-20 metros típicamente
 * 
 * Mejor precisión cuantos MÁS satélites
 * 
 * ========================================================================
 * IMPORTANTE:
 * 
 * ❌ GPS NO FUNCIONA EN INTERIOR
 *    Necesita línea directa con satélites
 *    Árboles/edificios bloquean señal
 * 
 * ✅ FUNCIONA EN EXTERIOR
 *    Cielo despejado
 *    Antena hacia arriba
 *    Esperar 2-5 minutos
 * 
 * ========================================================================
 */
