/*
 * ============================================
 * CANSAT - Grabación en Flash Interna
 * Para Arduino Nano 33 BLE Sense
 * ============================================
 * 
 * Guarda datos de sensores en la memoria Flash
 * interna del Nano 33 BLE (no necesita MicroSD)
 * 
 * USO:
 *   1. Cargar programa
 *   2. Abrir Monitor Serie a 9600 baud
 *   3. Comandos disponibles:
 *      - GRABAR  → Inicia grabación
 *      - PARAR   → Detiene grabación
 *      - LEER    → Muestra todos los datos guardados
 *      - BORRAR  → Borra todos los datos
 *      - ESTADO  → Muestra registros guardados
 * 
 * Autor: IES Diego Velázquez
 * Fecha: Febrero 2026
 */

#include <FlashIAPBlockDevice.h>
#include <TDBStore.h>

// ============================================
// CONFIGURACIÓN
// ============================================

// Dirección de inicio en Flash (últimos 256KB)
// El Nano 33 BLE tiene 1MB de Flash
#define FLASH_START_ADDRESS  0xC0000  // 768KB desde el inicio
#define FLASH_SIZE           0x40000  // 256KB para datos

// Máximo de registros
#define MAX_REGISTROS 3000  // Suficiente para ~50 minutos a 1 reg/seg

// Intervalo de grabación (ms)
#define INTERVALO_GRABACION 1000  // 1 segundo

// ============================================
// ESTRUCTURA DE DATOS
// ============================================

struct DatosSensor {
  uint32_t timestamp;    // Tiempo en ms desde inicio
  float temperatura;
  float humedad;
  float presion;
  float altitud;
  float co2;
  float latitud;
  float longitud;
  float altitudGPS;
  uint8_t satelites;
  float accX, accY, accZ;
  float gyrX, gyrY, gyrZ;
};

// ============================================
// VARIABLES GLOBALES
// ============================================

// Almacenamiento en RAM para luego volcar a Flash
DatosSensor registros[MAX_REGISTROS];
int numRegistros = 0;
bool grabando = false;
unsigned long tiempoInicio = 0;
unsigned long ultimaGrabacion = 0;

// Simulación de sensores (reemplazar con sensores reales)
float simTemp = 22.0;
float simHum = 65.0;
float simPres = 1013.25;
float simAlt = 500.0;

// ============================================
// SETUP
// ============================================

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  
  Serial.begin(9600);
  delay(3000);
  
  Serial.println();
  Serial.println("============================================");
  Serial.println("   CANSAT - Grabacion en Flash Interna");
  Serial.println("============================================");
  Serial.println();
  Serial.println("Comandos disponibles:");
  Serial.println("  GRABAR  - Inicia grabacion de datos");
  Serial.println("  PARAR   - Detiene grabacion");
  Serial.println("  LEER    - Muestra todos los datos");
  Serial.println("  BORRAR  - Borra todos los datos");
  Serial.println("  ESTADO  - Muestra estado actual");
  Serial.println("  CSV     - Exporta datos en formato CSV");
  Serial.println();
  Serial.println("Memoria disponible para ~" + String(MAX_REGISTROS) + " registros");
  Serial.println("============================================");
  Serial.println();
}

// ============================================
// LOOP PRINCIPAL
// ============================================

void loop() {
  // Procesar comandos del Serial
  if (Serial.available()) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();
    comando.toUpperCase();
    procesarComando(comando);
  }
  
  // Grabar datos si está activo
  if (grabando) {
    unsigned long ahora = millis();
    
    if (ahora - ultimaGrabacion >= INTERVALO_GRABACION) {
      ultimaGrabacion = ahora;
      grabarRegistro();
    }
    
    // Parpadear LED mientras graba
    digitalWrite(LED_BUILTIN, (millis() / 200) % 2);
  }
}

// ============================================
// PROCESAR COMANDOS
// ============================================

void procesarComando(String comando) {
  if (comando == "GRABAR") {
    iniciarGrabacion();
  }
  else if (comando == "PARAR") {
    detenerGrabacion();
  }
  else if (comando == "LEER") {
    leerDatos();
  }
  else if (comando == "BORRAR") {
    borrarDatos();
  }
  else if (comando == "ESTADO") {
    mostrarEstado();
  }
  else if (comando == "CSV") {
    exportarCSV();
  }
  else {
    Serial.println("Comando no reconocido: " + comando);
  }
}

// ============================================
// FUNCIONES DE GRABACIÓN
// ============================================

void iniciarGrabacion() {
  if (grabando) {
    Serial.println("Ya esta grabando...");
    return;
  }
  
  if (numRegistros >= MAX_REGISTROS) {
    Serial.println("ERROR: Memoria llena. Use BORRAR primero.");
    return;
  }
  
  grabando = true;
  tiempoInicio = millis();
  ultimaGrabacion = tiempoInicio;
  
  Serial.println();
  Serial.println(">>> GRABACION INICIADA <<<");
  Serial.println("Registros actuales: " + String(numRegistros));
  Serial.println("Espacio disponible: " + String(MAX_REGISTROS - numRegistros));
  Serial.println("Escriba PARAR para detener");
  Serial.println();
}

void detenerGrabacion() {
  if (!grabando) {
    Serial.println("No hay grabacion activa.");
    return;
  }
  
  grabando = false;
  digitalWrite(LED_BUILTIN, LOW);
  
  unsigned long duracion = millis() - tiempoInicio;
  
  Serial.println();
  Serial.println(">>> GRABACION DETENIDA <<<");
  Serial.println("Duracion: " + String(duracion / 1000) + " segundos");
  Serial.println("Registros totales: " + String(numRegistros));
  Serial.println();
}

void grabarRegistro() {
  if (numRegistros >= MAX_REGISTROS) {
    Serial.println("Memoria llena! Deteniendo grabacion...");
    detenerGrabacion();
    return;
  }
  
  // Leer sensores (reemplazar con lecturas reales)
  DatosSensor datos;
  datos.timestamp = millis() - tiempoInicio;
  
  // === AQUÍ VAN LOS SENSORES REALES ===
  // Por ahora, simulación:
  datos.temperatura = simTemp + random(-10, 10) / 10.0;
  datos.humedad = simHum + random(-20, 20) / 10.0;
  datos.presion = simPres + random(-10, 10) / 10.0;
  datos.altitud = simAlt - (numRegistros * 0.5);  // Simula descenso
  datos.co2 = 400 + random(0, 100);
  datos.latitud = 40.5795 + random(-100, 100) / 1000000.0;
  datos.longitud = -3.9184 + random(-100, 100) / 1000000.0;
  datos.altitudGPS = datos.altitud + random(-5, 5);
  datos.satelites = random(6, 12);
  datos.accX = random(-100, 100) / 100.0;
  datos.accY = random(-100, 100) / 100.0;
  datos.accZ = 9.8 + random(-10, 10) / 100.0;
  datos.gyrX = random(-50, 50) / 10.0;
  datos.gyrY = random(-50, 50) / 10.0;
  datos.gyrZ = random(-50, 50) / 10.0;
  // === FIN SENSORES ===
  
  // Guardar en array
  registros[numRegistros] = datos;
  numRegistros++;
  
  // Mostrar progreso cada 10 registros
  if (numRegistros % 10 == 0) {
    Serial.print("Grabando... ");
    Serial.print(numRegistros);
    Serial.print(" registros (Alt: ");
    Serial.print(datos.altitud, 1);
    Serial.println("m)");
  }
}

// ============================================
// FUNCIONES DE LECTURA
// ============================================

void leerDatos() {
  if (numRegistros == 0) {
    Serial.println("No hay datos guardados.");
    return;
  }
  
  Serial.println();
  Serial.println("============================================");
  Serial.println("   DATOS GUARDADOS (" + String(numRegistros) + " registros)");
  Serial.println("============================================");
  Serial.println();
  
  for (int i = 0; i < numRegistros; i++) {
    DatosSensor d = registros[i];
    
    Serial.print("#");
    Serial.print(i + 1);
    Serial.print(" | t=");
    Serial.print(d.timestamp / 1000.0, 1);
    Serial.print("s | T=");
    Serial.print(d.temperatura, 1);
    Serial.print("C | H=");
    Serial.print(d.humedad, 1);
    Serial.print("% | Alt=");
    Serial.print(d.altitud, 1);
    Serial.print("m | CO2=");
    Serial.print(d.co2, 0);
    Serial.println("ppm");
    
    // Pausa cada 20 líneas para no saturar el buffer
    if ((i + 1) % 20 == 0) {
      delay(100);
    }
  }
  
  Serial.println();
  Serial.println("============================================");
}

void exportarCSV() {
  if (numRegistros == 0) {
    Serial.println("No hay datos para exportar.");
    return;
  }
  
  Serial.println();
  Serial.println("=== INICIO CSV (copiar desde aqui) ===");
  Serial.println();
  
  // Cabecera
  Serial.println("timestamp,temp,hum,pres,alt,co2,lat,lon,altGPS,sat,accX,accY,accZ,gyrX,gyrY,gyrZ");
  
  // Datos
  for (int i = 0; i < numRegistros; i++) {
    DatosSensor d = registros[i];
    
    Serial.print(d.timestamp);
    Serial.print(",");
    Serial.print(d.temperatura, 2);
    Serial.print(",");
    Serial.print(d.humedad, 2);
    Serial.print(",");
    Serial.print(d.presion, 2);
    Serial.print(",");
    Serial.print(d.altitud, 2);
    Serial.print(",");
    Serial.print(d.co2, 0);
    Serial.print(",");
    Serial.print(d.latitud, 6);
    Serial.print(",");
    Serial.print(d.longitud, 6);
    Serial.print(",");
    Serial.print(d.altitudGPS, 2);
    Serial.print(",");
    Serial.print(d.satelites);
    Serial.print(",");
    Serial.print(d.accX, 2);
    Serial.print(",");
    Serial.print(d.accY, 2);
    Serial.print(",");
    Serial.print(d.accZ, 2);
    Serial.print(",");
    Serial.print(d.gyrX, 2);
    Serial.print(",");
    Serial.print(d.gyrY, 2);
    Serial.print(",");
    Serial.println(d.gyrZ, 2);
    
    // Pausa para no saturar buffer
    if ((i + 1) % 50 == 0) {
      delay(100);
    }
  }
  
  Serial.println();
  Serial.println("=== FIN CSV ===");
  Serial.println();
  Serial.println("Copie el contenido y guardelo como archivo .csv");
}

// ============================================
// OTRAS FUNCIONES
// ============================================

void borrarDatos() {
  if (grabando) {
    Serial.println("Detenga la grabacion primero (PARAR)");
    return;
  }
  
  numRegistros = 0;
  
  Serial.println();
  Serial.println(">>> DATOS BORRADOS <<<");
  Serial.println("Memoria lista para nueva grabacion.");
  Serial.println();
}

void mostrarEstado() {
  Serial.println();
  Serial.println("============================================");
  Serial.println("   ESTADO ACTUAL");
  Serial.println("============================================");
  Serial.println();
  Serial.print("Grabando: ");
  Serial.println(grabando ? "SI" : "NO");
  Serial.print("Registros guardados: ");
  Serial.println(numRegistros);
  Serial.print("Espacio usado: ");
  Serial.print((numRegistros * sizeof(DatosSensor)) / 1024.0, 2);
  Serial.println(" KB");
  Serial.print("Espacio disponible: ");
  Serial.print(((MAX_REGISTROS - numRegistros) * sizeof(DatosSensor)) / 1024.0, 2);
  Serial.println(" KB");
  Serial.print("Capacidad: ");
  Serial.print((numRegistros * 100) / MAX_REGISTROS);
  Serial.println("%");
  Serial.println();
}
