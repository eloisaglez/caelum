/*
 * =========================================================================
 * CANSAT RAM - PROGRAMA INTEGRADO DE MISIÓN FINAL
 * =========================================================================
 * PLACA: Arduino Nano 33 BLE Sense
 * SENSORES: GPS (Serial1), SCD40/41 (I2C), APC220 (Serial1)
 * * CONEXIÓN DE PINES:
 * - Pin D0 (RX): Conectar TX del GPS
 * - Pin D1 (TX): Conectar RX de la Radio APC220
 * - SDA / SCL: Sensor de CO2 SCD40
 * - VIN / GND: Batería de alimentación (3.7V-12V)
 * =========================================================================
 */

#include <SensirionI2cScd4x.h>
#include <Wire.h>

// Definición del puerto para GPS y Radio
#define telemetriaSerial Serial1 

// --- VARIABLES GPS ---
String gpsBuffer = "";
int satelites = 0;
float latitud = 0, longitud = 0, altitudGPS = 0;
bool tieneFix = false;
unsigned long ultimoDatoRecibido = 0;
const unsigned long TIMEOUT_CONEXION = 3000; 

// --- VARIABLES SCD40 (CO2) ---
SensirionI2cScd4x scd4x;
uint16_t co2 = 0;
float temperatura = 0.0, humedad = 0.0;

void setup() {
  // Ambas comunicaciones a 9600 para máxima estabilidad de radio
  Serial.begin(9600);           // Monitor USB (PC)
  telemetriaSerial.begin(9600); // Radio y GPS (Misión)

  // --- CONTROL DE ARRANQUE AUTÓNOMO Y GESTIÓN DE ENERGÍA ---
  unsigned long ventanaEspera = millis();
  while (!Serial && millis() - ventanaEspera < 5000) {
    // Esta espera de 5s permite abrir el Monitor Serie durante las pruebas.
    // Si no se detecta USB (vuelo con batería), el programa rompe el bucle 
    // y toma el control de forma autónoma para evitar que el sistema se 
    // quede bloqueado esperando un cable, garantizando el envío de telemetría.
  }

  // Inicialización del bus I2C y sensor de CO2
  Wire.begin();
  scd4x.begin(Wire, SCD41_I2C_ADDR_62);
  
  // Reiniciar sensor para asegurar lectura limpia
  scd4x.stopPeriodicMeasurement();
  delay(500);
  scd4x.startPeriodicMeasurement();

  Serial.println("SISTEMA CANSAT RAM: INICIADO");
  telemetriaSerial.println("RADIO_OK: TRANSMISION INICIADA");
}

void loop() {
  // 1. LECTURA DEL GPS (Entrada por Pin 0)
  while (telemetriaSerial.available()) {
    char c = telemetriaSerial.read();
    gpsBuffer += c;
    ultimoDatoRecibido = millis(); // Pulso de vida del GPS

    if (c == '\n') {
      procesarSentenciaNMEA(gpsBuffer);
      gpsBuffer = "";
    }
  }

  // 2. ENVÍO DE TELEMETRÍA CADA 2 SEGUNDOS (Salida por Pin 1)
  static unsigned long ultimaTransmision = 0;
  if (millis() - ultimaTransmision > 2000) {
    
    // Leer datos del sensor de CO2
    bool scdListos = false;
    scd4x.getDataReadyStatus(scdListos);
    if (scdListos) {
      scd4x.readMeasurement(co2, temperatura, humedad);
    }

    // --- LÓGICA DE SALIDA ---
    if (millis() - ultimoDatoRecibido > TIMEOUT_CONEXION) {
      // Si el sensor GPS no responde o el cable está suelto
      String errorMsg = "ALERTA: [CHECK GPS WIRE]";
      Serial.println(errorMsg);
      telemetriaSerial.println(errorMsg);
    } 
    else {
      // CONSTRUCCIÓN DE LA TRAMA CSV (Para Excel posterior)
      // Formato: Milisegundos, Satélites, Lat, Lon, Alt, CO2, Temp, Hum
      String datos = String(millis()) + "," +
                     String(satelites) + "," +
                     (tieneFix ? String(latitud, 6) : "XXXXXX") + "," +
                     (tieneFix ? String(longitud, 6) : "XXXXXX") + "," +
                     String(altitudGPS, 1) + "," +
                     String(co2) + "," +
                     String(temperatura, 1) + "," +
                     String(humedad, 1);

      // Enviar a la vez por cable (PC) y por Radio (Misión)
      Serial.println(datos);
      telemetriaSerial.println(datos);
    }
    
    ultimaTransmision = millis();
  }
}

// Función para extraer datos de las sentencias $GPGGA o $GNGGA
void procesarSentenciaNMEA(String sen) {
  if (sen.startsWith("$GNGGA") || sen.startsWith("$GPGGA")) {
    int comas[15];
    int contadorComas = 0;
    
    // Localizar las posiciones de las comas en la frase
    for (int i = 0; i < sen.length() && contadorComas < 15; i++) {
      if (sen[i] == ',') comas[contadorComas++] = i;
    }

    if (contadorComas >= 10) {
      satelites = sen.substring(comas[6] + 1, comas[7]).toInt();
      
      if (satelites > 0) {
        tieneFix = true;
        // Parseo básico de coordenadas (GradosMinutos -> Grados Decimales aprox)
        latitud = sen.substring(comas[1] + 1, comas[2]).toFloat() / 100.0;
        longitud = sen.substring(comas[3] + 1, comas[4]).toFloat() / 100.0;
        altitudGPS = sen.substring(comas[8] + 1, comas[9]).toFloat();
      } else {
        tieneFix = false;
        latitud = 0; longitud = 0; altitudGPS = 0;
      }
    }
  }
}
