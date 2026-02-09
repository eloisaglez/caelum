# CanSat Misión 2 - Documento 5
## Grabación en MicroSD - Almacenamiento Local

**Fecha:** Enero 2026  
**Proyecto:** CanSat - Detección de Firmas de Combustión  

---

## 📋 Objetivo

Grabar todos los datos de sensores en tarjeta MicroSD como respaldo (si APC220 falla).

---

## 💾 MicroSD - Especificaciones

```
Protocolo: SPI
Voltaje: 3.3V (crítico)
Capacidad: 2GB-32GB (recomendado 4-8GB)
Velocidad: Class 10+ (recomendado)
Archivo: MISSION2.CSV (formato CSV)
```

---

## 🔌 Conexión Física

**¡¡CRÍTICO!!** MicroSD es **SOLO 3.3V**. Si usas 5V → **SE DAÑA PERMANENTEMENTE**

```
Arduino Nano 33 BLE ← → Módulo MicroSD SPI

D10 (CS)   → MicroSD CS (Chip Select)
D11 (MOSI) → MicroSD MOSI (Master Out Slave In)
D12 (MISO) → MicroSD MISO (Master In Slave Out)
D13 (SCK)  → MicroSD SCK (Serial Clock)
GND        → GND
3.3V       → VCC (⚠️ NUNCA 5V)
```

**Verificar con multímetro:** VCC debe mostrar exactamente 3.3V

---

## 🛠️ Preparación MicroSD

### Paso 1: Formato

```
En Windows:
1. Inserta MicroSD en lector
2. Click derecho → Formatear
3. Sistema archivos: FAT32
4. Tamaño de unidad: 4096 bytes
5. Etiqueta: CANSAT
6. Click Iniciar → SÍ
```

### Paso 2: Crear carpeta (opcional)

```
Crear carpeta "DATOS" en MicroSD
Almacenaremos MISSION2.CSV aquí
```

---

## 📥 Instalación Librerías

```
Arduino IDE:

Sketch → Include Library → Manage Libraries

✅ Busca e instala:
   - SD (por Arduino - incluida por defecto)
```

---

## 💻 Programa: Grabar Sensores en MicroSD

```cpp
/*
 * Arduino Nano 33 BLE - MicroSD + Sensores
 * Graba CSV: Temperatura, Humedad, Presión, TVOC, eCO2, etc
 */

#include <SD.h>
#include <SPI.h>
#include "Adafruit_SGP30.h"
#include <ReefwingLPS22HB.h>
#include <Arduino_HS300x.h>
#include <Arduino_BMI270_BMM150.h>

// Pines SPI MicroSD
const int chipSelect = 10;

// Sensores
Adafruit_SGP30 sgp30;
ReefwingLPS22HB pressureSensor;

// Variables
File dataFile;
String filename = "MISSION2.CSV";
int contador = 0;

void setup() {
  Serial.begin(9600);
  delay(2000);
  
  Serial.println("╔════════════════════════════════════════╗");
  Serial.println("║  Arduino Nano 33 BLE - MicroSD        ║");
  Serial.println("║  Grabación MISSION2.CSV               ║");
  Serial.println("╚════════════════════════════════════════╝");
  Serial.println();
  
  // Inicializar MicroSD
  Serial.print("MicroSD (SPI D10/D11/D12/D13)... ");
  if (!SD.begin(chipSelect)) {
    Serial.println("❌ ERROR");
    Serial.println("VERIFICA:");
    Serial.println("  • D10 (CS)");
    Serial.println("  • D11 (MOSI)");
    Serial.println("  • D12 (MISO)");
    Serial.println("  • D13 (SCK)");
    Serial.println("  • 3.3V (NO 5V)");
    Serial.println("  • GND");
    while(1) delay(1000);
  }
  Serial.println("✓ OK");
  
  // Crear archivo CSV con cabecera
  if (!SD.exists(filename)) {
    dataFile = SD.open(filename, FILE_WRITE);
    if (dataFile) {
      dataFile.println("tiempo,temperatura,humedad,presion,tvoc,eco2,h2,ethanol,accelx,accely,accelz");
      dataFile.close();
      Serial.print("Archivo creado: ");
      Serial.println(filename);
    }
  } else {
    Serial.print("Archivo existe: ");
    Serial.println(filename);
  }
  
  // Inicializar SGP30
  Serial.print("SGP30... ");
  if (!sgp30.begin()) {
    Serial.println("ERROR");
  } else {
    Serial.println("OK");
  }
  
  // Inicializar LPS22HB
  Serial.print("LPS22HB... ");
  pressureSensor.begin();
  Serial.println("OK");
  
  // Inicializar HS3003
  Serial.print("HS3003... ");
  if (!HS300x.begin()) {
    Serial.println("ERROR");
  } else {
    Serial.println("OK");
  }
  
  // Inicializar IMU
  Serial.print("IMU... ");
  if (!IMU.begin()) {
    Serial.println("ERROR");
  } else {
    Serial.println("OK");
  }
  
  Serial.println();
  Serial.println("Grabando en MicroSD cada 2 segundos...");
  Serial.println();
}

void loop() {
  // Leer sensores
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
  
  float accelX = 0, accelY = 0, accelZ = 0;
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(accelX, accelY, accelZ);
  }
  
  // Abrir archivo
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
    dataFile.print((int)ethanol);
    dataFile.print(",");
    dataFile.print(accelX, 2);
    dataFile.print(",");
    dataFile.print(accelY, 2);
    dataFile.print(",");
    dataFile.println(accelZ, 2);
    
    dataFile.close();
    
    // Debug en USB
    Serial.print("✓ Grabado: ");
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
  delay(2000);  // Grabar cada 2 segundos
}
```

---

## 📊 Estructura del Archivo CSV

```
Archivo: MISSION2.CSV

Cabecera:
tiempo,temperatura,humedad,presion,tvoc,eco2,h2,ethanol,accelx,accely,accelz

Datos:
0,23.50,65.2,929.5,45,410,12500,18000,0.02,-0.01,1.00
1,23.50,65.1,929.5,48,412,12600,18100,0.01,-0.02,1.00
2,23.50,65.0,929.5,50,415,12700,18200,0.00,-0.01,1.00
```

---

## ✅ Verificación

### Paso 1: Cargar programa

```
1. Copia código arriba
2. Arduino IDE → Nuevo
3. Pega
4. RESET doble
5. Ctrl+U
```

### Paso 2: Verificar Monitor Serial

```
Deberías ver:
✓ MicroSD (SPI) OK
✓ SGP30 OK
✓ LPS22HB OK
✓ HS3003 OK
✓ IMU OK
✓ Grabado: 0 | T:23.5°C...
✓ Grabado: 1 | T:23.5°C...
```

### Paso 3: Leer archivo

```
1. Presiona Ctrl+C después de 30 segundos
2. Saca MicroSD del Arduino
3. Inserta en lector en PC
4. Abre MISSION2.CSV en Excel/notepad
5. Deberías ver datos en formato CSV
```

---

## 📈 Análisis de Datos

### En Excel

```
1. Abre MISSION2.CSV en Excel
2. Data → Text to Columns
3. Delimitador: Coma
4. Finish

Ahora puedes:
  ✓ Crear gráficos
  ✓ Analizar tendencias
  ✓ Buscar anomalías
```

### En Python

```python
import pandas as pd
import matplotlib.pyplot as plt

# Leer CSV
df = pd.read_csv('MISSION2.CSV')

# Gráfica temperatura
plt.plot(df['tiempo'], df['temperatura'])
plt.xlabel('Tiempo (s)')
plt.ylabel('Temperatura (°C)')
plt.title('CanSat - Temperatura durante vuelo')
plt.show()

# Gráfica TVOC (gases)
plt.plot(df['tiempo'], df['tvoc'], color='red')
plt.xlabel('Tiempo (s)')
plt.ylabel('TVOC (ppb)')
plt.title('CanSat - Contaminación detectada')
plt.show()
```

---

## ⚠️ Checklist Antes de Vuelo

```
☐ MicroSD insertada en módulo
☐ Módulo conectado D10/D11/D12/D13
☐ 3.3V verificado con multímetro
☐ Programa carga sin errores
☐ Monitor Serial muestra "Grabado: 0..."
☐ MicroSD formateada en FAT32
☐ Archivo MISSION2.CSV se crea correctamente
☐ Datos coherentes después de 1 minuto
```

---

## 🚨 Troubleshooting

### Error: "MicroSD no inicializa"

```
Causas:
  1. Voltaje incorrecto (5V en lugar de 3.3V)
  2. Cable CS (D10) no conectado
  3. MicroSD no formateada

Soluciones:
  1. Verificar 3.3V con multímetro
  2. Verificar D10 conectado
  3. Formatear en FAT32
```

### Archivo no se crea

```
Causas:
  1. MicroSD no detectada
  2. Tarjeta no tiene espacio
  3. Permiso de escritura denegado

Soluciones:
  1. Verificar inicialización
  2. Formatear MicroSD
  3. Probar otra MicroSD
```

### Datos no se graban

```
Causas:
  1. dataFile.close() no ejecutado
  2. Búfer no flushed
  3. MicroSD llena

Soluciones:
  1. Verificar cerrar archivo
  2. Reducir frecuencia de grabación
  3. Usar MicroSD más grande
```

---

## 🎯 Próximo Paso

**Documento 6:** Presentación de datos y conexión con Firebase

---

**Estado:** ✅ MicroSD funcionando con grabación CSV  
**Última actualización:** Enero 2026
