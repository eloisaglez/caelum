/*
 * =========================================================================
 * TEST DE SENSOR GPS - ARDUINO NANO 33 BLE SENSE
 * =========================================================================
 * CONEXIÓN:
 * GPS TX  -->  Pin D0 (RX) del Arduino
 * GPS RX  -->  Pin D1 (TX) del Arduino
 * * NOTA: En este modelo de Arduino, puedes cargar el programa sin 
 * desconectar el GPS de los pines 0 y 1. No hay conflicto con el USB.
 * =========================================================================
 */

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
