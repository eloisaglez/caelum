/*
 * ============================================
 * CANSAT - Grabación en RAM
 * Para Arduino Nano 33 BLE Sense
 * ============================================
 * 
 * Guarda datos de sensores en RAM
 * Reducido a 500 registros para no saturar memoria
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
 *      - CSV     → Exporta datos en formato CSV
 * 
 * Autor: IES Diego Velázquez
 * Fecha: Febrero 2026
 */

// ============================================
// CONFIGURACIÓN
// ============================================

// Máximo de registros (reducido para caber en RAM)
#define MAX_REGISTROS 500  // ~8 minutos a 1 reg/seg

// Intervalo de grabación (ms)
#define INTERVALO_GRABACION 1000  // 1 segundo

// ============================================
// ESTRUCTURA DE DATOS (reducida)
// ============================================

struct DatosSensor {
  uint32_t timestamp;    // 4 bytes
  int16_t temperatura;   // 2 bytes (x100 para decimales)
  int16_t humedad;       // 2 bytes (x100)
  int16_t presion;       // 2 bytes (hPa - 900, para ahorrar)
  int16_t altitud;       // 2 bytes (metros)
  int16_t co2;           // 2 bytes
  int32_t latitud;       // 4 bytes (x1000000)
  int32_t longitud;      // 4 bytes (x1000000)
  int16_t altitudGPS;    // 2 bytes
  uint8_t satelites;     // 1 byte
  int16_t accX, accY, accZ;  // 6 bytes (x100)
};  // Total: ~31 bytes por registro

// ============================================
// VARIABLES GLOBALES
// ============================================

DatosSensor registros[MAX_REGISTROS];
int numRegistros = 0;
bool grabando = false;
unsigned long tiempoInicio = 0;
unsigned long ultimaGrabacion = 0;

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
  Serial.println("   CANSAT - Grabacion en RAM");
  Serial.println("============================================");
  Serial.println();
  Serial.println("Comandos: GRABAR, PARAR, LEER, CSV, BORRAR, ESTADO");
  Serial.println();
  Serial.println("Capacidad: " + String(MAX_REGISTROS) + " registros (~8 min)");
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
  
  DatosSensor datos;
  datos.timestamp = millis() - tiempoInicio;
  
  // === AQUÍ VAN LOS SENSORES REALES ===
  // Por ahora, simulación:
  float tempSim = 22.0 + random(-10, 10) / 10.0;
  float humSim = 65.0 + random(-20, 20) / 10.0;
  float presSim = 1013.25 + random(-10, 10) / 10.0;
  float altSim = 500.0 - (numRegistros * 0.5);
  
  // Convertir a enteros para ahorrar espacio
  datos.temperatura = (int16_t)(tempSim * 100);
  datos.humedad = (int16_t)(humSim * 100);
  datos.presion = (int16_t)(presSim - 900);  // Guardar offset
  datos.altitud = (int16_t)altSim;
  datos.co2 = 400 + random(0, 100);
  datos.latitud = (int32_t)(40.5795 * 1000000) + random(-100, 100);
  datos.longitud = (int32_t)(-3.9184 * 1000000) + random(-100, 100);
  datos.altitudGPS = (int16_t)altSim + random(-5, 5);
  datos.satelites = random(6, 12);
  datos.accX = (int16_t)(random(-100, 100));
  datos.accY = (int16_t)(random(-100, 100));
  datos.accZ = (int16_t)(980 + random(-10, 10));
  // === FIN SENSORES ===
  
  registros[numRegistros] = datos;
  numRegistros++;
  
  // Mostrar progreso cada 10 registros
  if (numRegistros % 10 == 0) {
    Serial.print("Grabando... ");
    Serial.print(numRegistros);
    Serial.print(" reg (Alt: ");
    Serial.print(datos.altitud);
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
  Serial.println("=== DATOS (" + String(numRegistros) + " registros) ===");
  Serial.println();
  
  for (int i = 0; i < numRegistros; i++) {
    DatosSensor d = registros[i];
    
    Serial.print("#");
    Serial.print(i + 1);
    Serial.print(" t=");
    Serial.print(d.timestamp / 1000.0, 1);
    Serial.print("s T=");
    Serial.print(d.temperatura / 100.0, 1);
    Serial.print("C Alt=");
    Serial.print(d.altitud);
    Serial.println("m");
    
    if ((i + 1) % 20 == 0) delay(50);
  }
  
  Serial.println();
}

void exportarCSV() {
  if (numRegistros == 0) {
    Serial.println("No hay datos para exportar.");
    return;
  }
  
  Serial.println();
  Serial.println("=== INICIO CSV ===");
  Serial.println();
  
  // Cabecera
  Serial.println("timestamp,temp,hum,pres,alt,co2,lat,lon,altGPS,sat,accX,accY,accZ");
  
  // Datos
  for (int i = 0; i < numRegistros; i++) {
    DatosSensor d = registros[i];
    
    Serial.print(d.timestamp);
    Serial.print(",");
    Serial.print(d.temperatura / 100.0, 2);
    Serial.print(",");
    Serial.print(d.humedad / 100.0, 2);
    Serial.print(",");
    Serial.print(d.presion + 900.0, 2);
    Serial.print(",");
    Serial.print(d.altitud);
    Serial.print(",");
    Serial.print(d.co2);
    Serial.print(",");
    Serial.print(d.latitud / 1000000.0, 6);
    Serial.print(",");
    Serial.print(d.longitud / 1000000.0, 6);
    Serial.print(",");
    Serial.print(d.altitudGPS);
    Serial.print(",");
    Serial.print(d.satelites);
    Serial.print(",");
    Serial.print(d.accX / 100.0, 2);
    Serial.print(",");
    Serial.print(d.accY / 100.0, 2);
    Serial.print(",");
    Serial.println(d.accZ / 100.0, 2);
    
    if ((i + 1) % 50 == 0) delay(50);
  }
  
  Serial.println();
  Serial.println("=== FIN CSV ===");
}

void borrarDatos() {
  if (grabando) {
    Serial.println("Detenga la grabacion primero (PARAR)");
    return;
  }
  
  numRegistros = 0;
  Serial.println(">>> DATOS BORRADOS <<<");
}

void mostrarEstado() {
  Serial.println();
  Serial.println("=== ESTADO ===");
  Serial.print("Grabando: ");
  Serial.println(grabando ? "SI" : "NO");
  Serial.print("Registros: ");
  Serial.print(numRegistros);
  Serial.print("/");
  Serial.println(MAX_REGISTROS);
  Serial.print("Tiempo restante: ~");
  Serial.print((MAX_REGISTROS - numRegistros) / 60);
  Serial.println(" minutos");
  Serial.println();
}
