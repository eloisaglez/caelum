/*
 * ========================================================================
 * PROGRAMA 4: GPS - PRUEBA G10A-F30
 * ========================================================================
 * Arduino Nano 33 BLE Sense Rev2
 * 
 * Conexiones:
 *   TX GPS → D2
 *   RX GPS → D3
 *   VCC    → 3.3V
 *   GND    → GND
 *   EN     → 3.3V
 *   PPS    → sin conectar
 * 
 * Baudios GPS: 38400
 * ========================================================================
 */

#include <Arduino.h>

// UART hardware en D2(TX_GPS) y D3(RX_GPS)
// Constructor: UART(TX_arduino, RX_arduino)
UART gpsSerial(digitalPinToPinName(3), digitalPinToPinName(2), NC, NC);

// Variables GPS
String gpsData    = "";
float  gps_lat    = 0.0;
float  gps_lon    = 0.0;
float  gps_alt    = 0.0;
int    gps_sats   = 0;
bool   gps_fix    = false;

int           contador    = 0;
unsigned long lastFixTime = 0;

// Prototipos
void  parseGPS(String sentence);
void  parseGGA(String sentence);
void  parseRMC(String sentence);
float parseCoordinate(String coord);

void setup() {
  Serial.begin(115200);
  while (!Serial);

  gpsSerial.begin(38400);

  delay(1000);
  Serial.println();
  Serial.println("Prueba GPS G10A-F30 en D2/D3");
  Serial.println("TX GPS->D2  |  RX GPS->D3  |  38400 baudios");
  Serial.println("Esperando tramas NMEA...");
  Serial.println();
}

void loop() {
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
      Serial.println("N  | Estado  | Sats | Latitud   | Longitud  | Altitud");
      Serial.println("---+---------+------+-----------+-----------+--------");
    } else {
      Serial.println("N  | Estado  | Sats");
      Serial.println("---+---------+------");
    }
  }

  Serial.print(contador);
  Serial.print(" | ");
  if (gps_fix) Serial.print("FIX     | ");
  else         Serial.print("Wait    | ");
  Serial.print(gps_sats);
  Serial.print("    | ");
  if (gps_fix) {
    Serial.print(gps_lat, 5);
    Serial.print(" | ");
    Serial.print(gps_lon, 5);
    Serial.print(" | ");
    Serial.print(gps_alt, 1);
    Serial.print("m");
  }
  Serial.println();
  contador++;
  delay(1000);
}

void parseGPS(String sentence) {
  if (sentence.length() < 6) return;
  if (sentence.startsWith("$GNGGA") || sentence.startsWith("$GPGGA")) parseGGA(sentence);
  else if (sentence.startsWith("$GNRMC") || sentence.startsWith("$GPRMC")) parseRMC(sentence);
}

void parseGGA(String sentence) {
  int commaCount = 0, lastIndex = 0;
  for (int i = 0; i < (int)sentence.length(); i++) {
    if (sentence[i] == ',' || sentence[i] == '\n') {
      String field = sentence.substring(lastIndex, i);
      if (commaCount == 7) gps_sats = field.toInt();
      else if (commaCount == 9 && field.length() > 0) gps_alt = field.toFloat();
      lastIndex = i + 1;
      commaCount++;
    }
  }
}

void parseRMC(String sentence) {
  int commaCount = 0, lastIndex = 0;
  for (int i = 0; i < (int)sentence.length(); i++) {
    if (sentence[i] == ',' || sentence[i] == '\n') {
      String field = sentence.substring(lastIndex, i);
      if (commaCount == 2) {
        gps_fix = (field == "A");
        if (gps_fix) lastFixTime = millis();
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

float parseCoordinate(String coord) {
  if (coord.length() < 5) return 0.0;
  int dotIndex     = coord.indexOf('.');
  int degreeDigits = dotIndex - 2;
  if (degreeDigits <= 0) return 0.0;
  float degrees = coord.substring(0, degreeDigits).toFloat();
  float minutes = coord.substring(degreeDigits).toFloat();
  return degrees + (minutes / 60.0);
}
