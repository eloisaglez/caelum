/*
 * ========================================================================
 * PROGRAMA 4: MICROSD - GRABACIÓN DE DATOS
 * ========================================================================
 * 
 * Autor: CanSat Misión 2
 * Fecha: Enero 2026
 * Proyecto: CanSat Misión 2
 * 
 * FUNCIÓN: Grabar datos de sensores en archivo CSV
 * 
 * CONEXIÓN (SPI):
 *   D10 (CS)   → MicroSD CS
 *   D11 (MOSI) → MicroSD MOSI
 *   D12 (MISO) → MicroSD MISO
 *   D13 (SCK)  → MicroSD SCK
 *   3.3V → MicroSD VCC (⚠️ NUNCA 5V)
 *   GND → GND
 * 
 * OBJETIVO: Almacenamiento de datos como respaldo
 * 
 * ========================================================================
 */

#include <SD.h>
#include <SPI.h>
#include "Adafruit_SGP30.h"
#include <ReefwingLPS22HB.h>
#include <Arduino_HS300x.h>

const int chipSelect = 10;
File dataFile;
String filename = "MISSION2.CSV";

Adafruit_SGP30 sgp30;
ReefwingLPS22HB pressureSensor;

int contador = 0;
boolean sdOk = false;

void setup() {
  Serial.begin(9600);
  delay(2000);
  
  Serial.println();
  Serial.println("╔════════════════════════════════════════╗");
  Serial.println("║  Programa 4: MicroSD                  ║");
  Serial.println("║  Grabación en CSV                     ║");
  Serial.println("╚════════════════════════════════════════╝");
  Serial.println();
  
  // Inicializar MicroSD
  Serial.print("Inicializando MicroSD (SPI)... ");
  if (!SD.begin(chipSelect)) {
    Serial.println("❌ ERROR");
    Serial.println();
    Serial.println("VERIFICA:");
    Serial.println("  • D10 (CS) conectado");
    Serial.println("  • D11 (MOSI) conectado");
    Serial.println("  • D12 (MISO) conectado");
    Serial.println("  • D13 (SCK) conectado");
    Serial.println("  • 3.3V (NO 5V) conectado");
    Serial.println("  • GND conectado");
    Serial.println("  • MicroSD formateada FAT32");
    while(1) delay(1000);
  }
  Serial.println("✓ OK");
  sdOk = true;
  
  // Crear archivo con cabecera
  if (!SD.exists(filename)) {
    dataFile = SD.open(filename, FILE_WRITE);
    if (dataFile) {
      dataFile.println("tiempo,temperatura,humedad,presion,tvoc,eco2,h2,ethanol");
      dataFile.close();
      Serial.print("Archivo creado: ");
      Serial.println(filename);
    }
  } else {
    Serial.print("Archivo existe: ");
    Serial.println(filename);
  }
  
  // Inicializar sensores
  Serial.print("SGP30... ");
  if (sgp30.begin()) {
    Serial.println("✓");
  } else {
    Serial.println("❌");
  }
  
  Serial.print("LPS22HB... ");
  pressureSensor.begin();
  Serial.println("✓");
  
  Serial.print("HS3003... ");
  if (HS300x.begin()) {
    Serial.println("✓");
  } else {
    Serial.println("❌");
  }
  
  Serial.println();
  Serial.println("═══════════════════════════════════════════════════");
  Serial.println("Grabando en MicroSD cada 2 segundos...");
  Serial.println("═══════════════════════════════════════════════════");
  Serial.println();
}

void loop() {
  if (!sdOk) {
    delay(1000);
    return;
  }
  
  // LEER SENSORES
  float temp = HS300x.readTemperature();
  float humedad = HS300x.readHumidity();
  float presion = pressureSensor.readPressure() / 100.0;
  
  float tvoc = 0, eco2 = 0, h2 = 0, ethanol = 0;
  if (sgp30.IAQmeasure()) {
    tvoc = sgp30.TVOC;
    eco2 = sgp30.eCO2;
    h2 = sgp30.rawH2;
    ethanol = sgp30.rawEthanol;
  }
  
  // ABRIR ARCHIVO
  dataFile = SD.open(filename, FILE_WRITE);
  if (dataFile) {
    // Escribir línea CSV
    dataFile.print(contador);
    dataFile.print(",");
    dataFile.print(temp, 2);
    dataFile.print(",");
    dataFile.print(humedad, 1);
    dataFile.print(",");
    dataFile.print(presion, 1);
    dataFile.print(",");
    dataFile.print((int)tvoc);
    dataFile.print(",");
    dataFile.print((int)eco2);
    dataFile.print(",");
    dataFile.print((int)h2);
    dataFile.print(",");
    dataFile.println((int)ethanol);
    
    dataFile.close();
    
    // DEBUG en USB
    Serial.print("✓ Grabado #");
    Serial.print(contador);
    Serial.print(" | T:");
    Serial.print(temp, 1);
    Serial.print("°C H:");
    Serial.print(humedad, 1);
    Serial.print("% P:");
    Serial.print(presion, 1);
    Serial.print("hPa TVOC:");
    Serial.print((int)tvoc);
    Serial.println("ppb");
    
  } else {
    Serial.println("❌ Error al abrir archivo");
  }
  
  contador++;
  delay(2000);
}

/*
 * ========================================================================
 * FORMATO CSV GRABADO:
 * 
 * Encabezado:
 * tiempo,temperatura,humedad,presion,tvoc,eco2,h2,ethanol
 * 
 * Datos (ejemplo):
 * 0,23.50,65.2,929.5,45,410,12500,18000
 * 1,23.50,65.1,929.5,48,412,12600,18100
 * 2,23.50,65.0,929.5,50,415,12700,18200
 * 
 * ========================================================================
 * CHECKLIST PRE-VUELO:
 * 
 * ☐ MicroSD insertada en módulo
 * ☐ Módulo conectado (D10/D11/D12/D13)
 * ☐ 3.3V verificado con multímetro
 * ☐ Programa carga sin errores
 * ☐ Monitor Serial muestra "Grabado: 0..."
 * ☐ MicroSD formateada FAT32
 * ☐ Datos coherentes después de 1 minuto
 * 
 * ========================================================================
 * TROUBLESHOOTING:
 * 
 * Error: "MicroSD no inicializa"
 *   1. Verificar 3.3V con multímetro
 *   2. Verificar D10 conectado (CS)
 *   3. Formatear en FAT32
 * 
 * Error: "No se crea archivo"
 *   1. MicroSD no detectada
 *   2. Tarjeta sin espacio
 *   3. Formatear de nuevo
 * 
 * Error: "Datos no se graban"
 *   1. Archivo no se cierra (dataFile.close())
 *   2. MicroSD llena
 *   3. Probar otra MicroSD
 * 
 * ========================================================================
 * ANÁLISIS POSTERIOR:
 * 
 * En Excel:
 *   1. Abre MISSION2.CSV
 *   2. Data → Text to Columns
 *   3. Delimitador: Coma
 *   4. Crea gráficos de TVOC vs tiempo
 * 
 * En Python:
 *   import pandas as pd
 *   df = pd.read_csv('MISSION2.CSV')
 *   print(df.describe())  # Estadísticas
 * 
 * ========================================================================
 */
