*
 * PROGRAMA 3: GPS - POSICIÓN Y ALTITUD
 * ADAPTADO A ARDUINO NANO 33 BLE SENSE
 */

 // NO SoftwareSerial en Nano 33 BLE
#include <Arduino.h>

// UART real en D3 (TX) y D2 (RX)
UART gpsSerial(digitalPinToPinName(3), digitalPinToPinName(2), NC, NC);

// Variables GPS
String gpsData = "";
float gps_lat = 0.0, gps_lon = 0.0;
float gps_alt = 0.0;
int gps_satellites = 0;
boolean gps_fix = false;

int contador = 0;
unsigned long lastFixTime = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial);

  gpsSerial.begin(9600);

  delay(2000);
  
  Serial.println();
  Serial.println("╔════════════════════════════════════════╗");
  Serial.println("║  Programa 3: GPS (Nano 33 BLE Sense)  ║");
  Serial.println("╚════════════════════════════════════════╝");
  Serial.println("⏳ Esperando señal GPS...");
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
  
  if (gps_fix) Serial.print("✓ FIX  | ");
  else Serial.print("⏳ Wait | ");
  
  Serial.print(gps_satellites);
  Serial.print("  | ");
  
  if (gps_fix) {
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
  } 
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
      
      if (commaCount == 2) {
        gps_fix = (field == "A");
        if (gps_fix) lastFixTime = millis();
      } 
      else if (commaCount == 3) {
        gps_lat = parseCoordinate(field);
      } 
      else if (commaCount == 5) {
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
      
      if (commaCount == 7) gps_satellites = field.toInt();
      else if (commaCount == 9 && field.length() > 0) gps_alt = field.toFloat();
      
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
