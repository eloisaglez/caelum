/*
 * =========================================================================
 * PROGRAMA DE PRUEBA GPS - CANSAT (FINAL)
 * PLACA: Arduino Nano 33 BLE Sense
 * =========================================================================
 * CONEXIÓN DE HARDWARE:
 * - GPS TX  --> Arduino RX (Pin 0)
 * - GPS RX  --> Arduino TX (Pin 1)
 * - GPS VCC --> 3.3V 
 * - GPS GND --> GND
 * =========================================================================
 */

#include <Arduino.h>

// Definimos el puerto del GPS/Radio para que sea fácil de leer
#define gpsPort Serial1 

// --- VARIABLES GLOBALES ---
String gpsData = "";
float gps_lat = 0.0;
float gps_lon = 0.0;
float gps_alt = 0.0;
int gps_satellites = 0;
boolean gps_fix = false;

int contador = 0;
unsigned long lastFixTime = 0;

void setup() {
  // 1. INICIAR PUERTO USB (Para el ordenador)
  Serial.begin(115200); 

  // -----------------------------------------------------------------------
  // 2. BLOQUE DE ARRANQUE INTELIGENTE (Seguridad + Modo Vuelo)
  // -----------------------------------------------------------------------
  
  // Paso A: Esperar al USB (Máximo 4 segundos)
  // Si estamos en el laboratorio, esto espera a que abras el monitor.
  // Si estamos en el cohete (batería), se salta esto tras 4s.
  unsigned long inicio = millis();
  while (!Serial && millis() - inicio < 4000) {
    // Esperando conexión...
  }

  Serial.println("--- SISTEMA DE ARRANQUE CANSAT ---");

  // Paso B: Cuenta atrás de seguridad (Vital para evitar 'Port Busy')
  // Da tiempo a estabilizar el sistema antes de abrir el puerto ruidoso del GPS.
  for(int i = 5; i > 0; i--) {
     if(Serial) {
       Serial.print("⚠️ Activando GPS en: ");
       Serial.println(i);
     }
     delay(1000); 
  }
  
  if(Serial) Serial.println("✅ ACTIVANDO PUERTO SERIAL1 (GPS/RADIO)...");

  // -----------------------------------------------------------------------
  // 3. INICIAR GPS (Puerto Hardware)
  // -----------------------------------------------------------------------
  gpsPort.begin(9600); // La mayoría de GPS funcionan a 9600 baudios
}

void loop() {
  // -----------------------------------------------------------------------
  // LECTURA DE DATOS (Lo que entra por el Pin 0)
  // -----------------------------------------------------------------------
  while (gpsPort.available()) {
    char c = gpsPort.read();
    gpsData += c;
    
    // Si detectamos un salto de línea, procesamos la frase completa
    if (c == '\n') {
      parseGPS(gpsData);
      gpsData = ""; // Limpiar buffer para la siguiente frase
    }
  }
  
  // -----------------------------------------------------------------------
  // MOSTRAR DATOS (Solo cada cierto tiempo para no saturar la pantalla)
  // -----------------------------------------------------------------------
  static unsigned long ultimaImpresion = 0;
  
  // Imprimimos cada 1 segundo (1000 ms)
  if (millis() - ultimaImpresion > 1000) {
      
      // Solo imprimimos si hay un cable USB conectado
      if(Serial) {
        Serial.println("\n--------------------------------------------------");
        if (gps_fix) {
          Serial.println("ESTADO: FIJADO (FIX OK) ✅");
          Serial.print("Satélites: "); Serial.println(gps_satellites);
          Serial.print("Latitud:   "); Serial.println(gps_lat, 6);
          Serial.print("Longitud:  "); Serial.println(gps_lon, 6);
          Serial.print("Altitud:   "); Serial.print(gps_alt); Serial.println(" m");
        } else {
          Serial.println("ESTADO: BUSCANDO SATÉLITES... ⏳");
          Serial.print("Satélites vistos: "); Serial.println(gps_satellites);
          Serial.println("(Saca la antena al exterior y espera unos minutos)");
        }
        Serial.println("--------------------------------------------------");
      }
      
      ultimaImpresion = millis();
  }
}

// =========================================================================
// FUNCIONES DE PARSEO MANUAL (Tu lógica original mejorada)
// =========================================================================

void parseGPS(String sentence) {
  // Filtro de seguridad: ignorar frases corruptas o muy cortas
  if (sentence.length() < 6) return;
  
  // $GNGGA o $GPGGA -> Datos de Altitud y Satélites
  if (sentence.startsWith("$GNGGA") || sentence.startsWith("$GPGGA")) {
    parseGGA(sentence);
  } 
  // $GNRMC o $GPRMC -> Datos de Posición y Estado
  else if (sentence.startsWith("$GNRMC") || sentence.startsWith("$GPRMC")) {
    parseRMC(sentence);
  }
}

void parseRMC(String sentence) {
  int commaCount = 0;
  int lastIndex = 0;
  
  for (int i = 0; i < sentence.length(); i++) {
    if (sentence[i] == ',' || sentence[i] == '\n') {
      String field = sentence.substring(lastIndex, i);
      
      // Campo 2: Estado (A=Active, V=Void)
      if (commaCount == 2) {
        gps_fix = (field == "A");
        if (gps_fix) lastFixTime = millis();
      } 
      // Campo 3: Latitud
      else if (commaCount == 3) {
        gps_lat = parseCoordinate(field);
      } 
      // Campo 4: N/S (Hemisferio)
      else if (commaCount == 4) {
        if (field == "S") gps_lat = -gps_lat;
      }
      // Campo 5: Longitud
      else if (commaCount == 5) {
        gps_lon = parseCoordinate(field);
      }
      // Campo 6: E/W (Hemisferio)
      else if (commaCount == 6) {
        if (field == "W") gps_lon = -gps_lon;
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
      
      // Campo 7: Número de satélites
      if (commaCount == 7) gps_satellites = field.toInt();
      // Campo 9: Altitud
      else if (commaCount == 9 && field.length() > 0) gps_alt = field.toFloat();
      
      lastIndex = i + 1;
      commaCount++;
    }
  }
}

// Función auxiliar para convertir coordenadas NMEA (GradosMinutos) a Decimal
float parseCoordinate(String coord) {
  if (coord.length() < 5) return 0.0;
  int dotIndex = coord.indexOf('.');
  int degreeDigits = dotIndex - 2; // Los minutos siempre son los 2 dígitos antes del punto
  
  if (degreeDigits <= 0) return 0.0;
  
  float degrees = coord.substring(0, degreeDigits).toFloat();
  float minutes = coord.substring(degreeDigits).toFloat();
  
  return degrees + (minutes / 60.0);
}
