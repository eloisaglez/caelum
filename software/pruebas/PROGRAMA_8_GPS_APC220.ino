/*
 * ========================================================================
 * PRUEBA GPS + APC220 SIMULTÁNEOS
 * ========================================================================
 * Arduino Nano 33 BLE Sense Rev2
 * 
 * GPS G10A-F30:
 *   TX GPS → D2  |  RX GPS → D3  |  38400 baudios
 *   VCC → 3.3V   |  GND → GND    |  EN → 3.3V
 * 
 * APC220:
 *   TXD APC → Pin 0 (RX Serial1)
 *   RXD APC → Pin 1 (TX Serial1)
 *   VCC → 3.3V  |  GND → GND
 * ========================================================================
 */

#include <Arduino.h>

// GPS en D2/D3 — UART hardware alternativo
UART gpsSerial(digitalPinToPinName(3), digitalPinToPinName(2), NC, NC);

// APC220 en Serial1 (pines 0/1)
#define APC_PORT  Serial1
#define APC_BAUD  9600

// Variables GPS
String gpsData  = "";
float  gps_lat  = 0.0;
float  gps_lon  = 0.0;
float  gps_alt  = 0.0;
int    gps_sats = 0;
bool   gps_fix  = false;

int           contador    = 0;
unsigned long lastSend    = 0;

// Prototipos
void  parseGPS(String sentence);
void  parseGGA(String sentence);
void  parseRMC(String sentence);
float parseCoordinate(String coord);

// ---------------------------------------------------------------
void setup() {
  Serial.begin(115200);
  while (!Serial);

  gpsSerial.begin(38400);
  APC_PORT.begin(APC_BAUD);

  delay(1000);
  Serial.println();
  Serial.println("=== PRUEBA GPS + APC220 ===");
  Serial.println("GPS:    D2(TX_GPS)/D3(RX_GPS) a 38400 baudios");
  Serial.println("APC220: Serial1 (pin0/pin1)   a 9600 baudios");
  Serial.println("Enviando datos GPS por radio cada segundo...");
  Serial.println();
}

// ---------------------------------------------------------------
void loop() {
  // Leer GPS
  while (gpsSerial.available()) {
    char c = gpsSerial.read();
    gpsData += c;
    if (c == '\n') {
      parseGPS(gpsData);
      gpsData = "";
    }
  }

  // Cada segundo: mostrar en monitor y enviar por APC220
  if (millis() - lastSend >= 1000) {
    lastSend = millis();

    // Construir mensaje
    String msg = "T=" + String(contador) + " ";
    if (gps_fix) {
      msg += "FIX Sats=" + String(gps_sats);
      msg += " Lat=" + String(gps_lat, 5);
      msg += " Lon=" + String(gps_lon, 5);
      msg += " Alt=" + String(gps_alt, 1) + "m";
    } else {
      msg += "WAIT Sats=" + String(gps_sats);
    }

    // Monitor serie
    Serial.println(msg);

    // Radio APC220
    APC_PORT.println(msg);

    contador++;
  }

  // Reenviar comandos del APC220 al monitor (para debug)
  while (APC_PORT.available()) {
    Serial.print("[APC->] ");
    Serial.write(APC_PORT.read());
  }
}

// ---------------------------------------------------------------
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
