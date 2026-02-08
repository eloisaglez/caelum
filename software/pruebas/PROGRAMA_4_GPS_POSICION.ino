/*
 * =========================================================================
 * TEST DE SENSOR GPS - CON AUTODIAGNÓSTICO DE CABLEADO- ARDUINO NANO 33 BLE SENSE
 * =========================================================================
 * CONEXIÓN:
 * GPS TX  -->  Pin D0 (RX) del Arduino
 * GPS RX  -->  Pin D1 (TX) del Arduino
 * * NOTA: En este modelo de Arduino, puedes cargar el programa sin 
 * desconectar el GPS de los pines 0 y 1. No hay conflicto con el USB.
 * =========================================================================
 */

#include <TinyGPSPlus.h>

#define gpsSerial Serial1
TinyGPSPlus gps;

// Tiempo máximo sin recibir datos antes de dar error de conexión
const unsigned long TIMEOUT_CONEXION = 3000; 

void setup() {
  Serial.begin(115200);
  gpsSerial.begin(9600); 

  while (!Serial); 
  delay(1000);

  Serial.println("===========================================");
  Serial.println("       SISTEMA DE NAVEGACIÓN CANSAT        ");
  Serial.println("===========================================");
}

void loop() {
  // 1. Leer datos y actualizar contador de actividad
  static unsigned long ultimoDatoRecibido = 0;
  
  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
    ultimoDatoRecibido = millis(); // Actualizamos cada vez que entra un byte
  }

  // 2. Mostrar información cada 2 segundos
  static unsigned long ultimaActualizacion = 0;
  if (millis() - ultimaActualizacion > 2000) {
    
    // VERIFICACIÓN DE CABLEADO
    if (millis() - ultimoDatoRecibido > TIMEOUT_CONEXION) {
      Serial.println(" [!] ERROR: CHECK THE WIRE / NO GPS DATA DETECTED ");
      Serial.println("     Verifica: TX->Pin 0, RX->Pin 1, VCC y GND.");
    } 
    else {
      imprimirDatosGPS();
    }
    
    ultimaActualizacion = millis();
  }
}

void imprimirDatosGPS() {
  Serial.print("Sats: ");
  Serial.print(gps.satellites.value());
  
  Serial.print(" | Lat: ");
  if (gps.location.isValid()) {
    Serial.print(gps.location.lat(), 6);
  } else {
    Serial.print("XXXXXX");
  }

  Serial.print(" | Lon: ");
  if (gps.location.isValid()) {
    Serial.print(gps.location.lng(), 6);
  } else {
    Serial.print("XXXXXX");
  }

  Serial.print(" | Alt: ");
  if (gps.altitude.isValid()) {
    Serial.print(gps.altitude.meters(), 1);
    Serial.print("m");
  } else {
    Serial.print("0.0m");
  }

  // Mensaje de estado dinámico según satélites
  if (gps.satellites.value() == 0) {
    Serial.println(" [ BUSCANDO SEÑAL... ]");
  } else if (!gps.location.isValid()) {
    Serial.println(" [ SEÑAL DÉBIL - ESPERANDO FIX ]");
  } else {
    Serial.println(" [ FIX OK ✓ ]");
  }
}

#define gpsSerial Serial1 // Serial1 usa los pines D0 y D1

// Variables para el procesado simple
String gpsBuffer = "";
int satelites = 0;
float latitud = 0, longitud = 0, altitudGPS = 0;
bool tieneFix = false;

void setup() {
  // El monitor serie del PC va a 115200
  Serial.begin(115200);
  while (!Serial); 

  // El GPS suele venir de fábrica a 9600
  gpsSerial.begin(9600);

  Serial.println("========================================");
  Serial.println("   TEST DE SENSOR GPS - NANO 33 BLE     ");
  Serial.println("========================================");
  Serial.println("Buscando satelites... (Sal fuera si no hay señal)");
}

void loop() {
  // 1. Leer datos del GPS
  while (gpsSerial.available()) {
    char c = gpsSerial.read();
    gpsBuffer += c;

    // Si llega un fin de línea, procesamos la sentencia
    if (c == '\n') {
      procesarNMEA(gpsBuffer);
      gpsBuffer = "";
    }
  }

  // 2. Mostrar resumen cada 2 segundos
  static unsigned long lastPrint = 0;
  if (millis() - lastPrint > 2000) {
    Serial.println("\n--- ESTADO ACTUAL DEL GPS ---");
    if (tieneFix) {
      Serial.print(" [OK] FIX CONSEGUIDO!");
    } else {
      Serial.print(" [..] BUSCANDO SEÑAL...");
    }
    
    Serial.print(" | Satelites: "); Serial.println(satelites);
    Serial.print(" Latitud: ");  Serial.println(latitud, 6);
    Serial.print(" Longitud: "); Serial.println(longitud, 6);
    Serial.print(" Altitud: ");  Serial.print(altitudGPS); Serial.println(" m");
    Serial.println("-----------------------------");
    
    lastPrint = millis();
  }
}

void procesarNMEA(String sen) {
  // Buscamos la sentencia $GNGGA o $GPGGA (contiene posición y satélites)
  if (sen.startsWith("$GNGGA") || sen.startsWith("$GPGGA")) {
    
    // Dividimos por comas (formato NMEA estándar)
    // Ejemplo: $GPGGA,hhmmss.ss,llll.ll,a,yyyyy.yy,a,x,xx,x.x,x.x,M,x.x,M,x.x,xxxx*hh
    int indices[15];
    int count = 0;
    for (int i = 0; i < sen.length() && count < 15; i++) {
      if (sen[i] == ',') indices[count++] = i;
    }

    if (count >= 10) {
      satelites = sen.substring(indices[6] + 1, indices[7]).toInt();
      
      if (satelites > 0) {
        tieneFix = true;
        // Parseo simple de lat/lon (formato grados y minutos decimales)
        latitud = sen.substring(indices[1] + 1, indices[2]).toFloat() / 100.0;
        longitud = sen.substring(indices[3] + 1, indices[4]).toFloat() / 100.0;
        altitudGPS = sen.substring(indices[8] + 1, indices[9]).toFloat();
      } else {
        tieneFix = false;
      }
    }
  }
}
