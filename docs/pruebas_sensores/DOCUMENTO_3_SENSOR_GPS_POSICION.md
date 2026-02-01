# 📋 DOCUMENTO 3: INTEGRACIÓN SENSOR GPS - POSICIÓN Y ALTITUD

## Objetivo
Integrar GPS para obtener coordenadas (lat/lon), altitud y número de satélites.

---

## 📡 SENSOR GPS - ESPECIFICACIONES

```
Modelo: ATGM336H (o compatible)
Protocolo: UART (comunicación serie)
Velocidad: 9600 baud (por defecto)
Salida: Sentencias NMEA ($GPRMC, $GPGGA, etc)
Función: Latitud, Longitud, Altitud, Satélites
```

---

## 🔌 CONEXIÓN FÍSICA

### Pines Arduino Nano 33 BLE

```
GPS ATGM336H:

VCC (rojo)     → Arduino 3.3V
GND (negro)    → Arduino GND
TX (amarillo)  → Arduino D2 (RX de SoftwareSerial)
RX (verde)     → Arduino D4 (TX de SoftwareSerial)
```

### Por qué no Serial1 (Grove)

```
❌ Serial1 se usa para APC220 (antena RF)
✅ GPS va en SoftwareSerial D2/D4
   (permite 2 puertos UART simultáneamente)
```

---

## 📥 INSTALACIÓN LIBRERÍAS

```
Sketch → Include Library → Manage Libraries

No necesita librería especial
- Wire.h → Incluida por defecto
- SoftwareSerial.h → Incluida por defecto
- Usamos parseo manual de NMEA
```

---

## ✅ VERIFICACIÓN GPS

Antes de integrar, verifica que envía datos:

```cpp
#include <SoftwareSerial.h>

SoftwareSerial gpsSerial(2, 4);  // RX=D2, TX=D4

void setup() {
  Serial.begin(9600);
  gpsSerial.begin(9600);
  delay(2000);
  
  Serial.println("Leyendo datos GPS RAW...");
}

void loop() {
  while (gpsSerial.available()) {
    char c = gpsSerial.read();
    Serial.write(c);  // Imprime exactamente lo que recibe
  }
}
```

**Resultado esperado:**

```
$GNGGA,225030.00,4027.80522,N,00345.83720,W,0,00,99.99,,,,,,*54
$GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99,1*01
$GPGSV,1,1,00,0*65
$GNRMC,,V,,,,,,,,,,M,V*34
...
```

Si NO ves datos → Revisa conexión TX/RX

---

## 💻 PROGRAMA PRUEBA GPS

```cpp
/*
 * Arduino Nano 33 BLE - Prueba GPS
 * Latitud + Longitud + Altitud + Satélites
 */

#include <SoftwareSerial.h>

SoftwareSerial gpsSerial(2, 4);  // RX=D2, TX=D4

// Variables GPS
float gps_lat = 0.0, gps_lon = 0.0;
float gps_alt = 0.0;
int gps_sats = 0;
boolean gps_fix = false;

String gpsData = "";

void setup() {
  Serial.begin(9600);
  gpsSerial.begin(9600);
  delay(2000);
  
  Serial.println();
  Serial.println("╔════════════════════════════════════════╗");
  Serial.println("║  Arduino Nano 33 BLE - GPS            ║");
  Serial.println("║  Latitud + Longitud + Altitud + Sats  ║");
  Serial.println("╚════════════════════════════════════════╝");
  Serial.println();
  Serial.println("Esperando fix GPS (puede tardar 2-5 min en exterior)...");
  Serial.println();
}

void loop() {
  // Leer datos GPS
  while (gpsSerial.available()) {
    char c = gpsSerial.read();
    gpsData += c;
    
    if (c == '\n') {
      parseGPS(gpsData);
      gpsData = "";
    }
  }
  
  // Mostrar estado
  if (gps_fix) {
    Serial.print("✓ FIX - Sats: ");
    Serial.print(gps_sats);
    Serial.print(" | Lat: ");
    Serial.print(gps_lat, 6);
    Serial.print(" | Lon: ");
    Serial.print(gps_lon, 6);
    Serial.print(" | Alt: ");
    Serial.print(gps_alt, 1);
    Serial.println("m");
  } else {
    Serial.println("⏳ Sin fix GPS (buscando satélites)...");
    delay(5000);
  }
}

void parseGPS(String sentence) {
  if (sentence.length() < 6) return;
  
  // Procesar GNGGA (satélites y altitud)
  if (sentence.startsWith("$GNGGA")) {
    parseGGA(sentence);
  }
  // Procesar GNRMC (posición y fix)
  else if (sentence.startsWith("$GNRMC")) {
    parseRMC(sentence);
  }
}

void parseGGA(String sentence) {
  int commaCount = 0;
  int lastIndex = 0;
  
  for (int i = 0; i < sentence.length(); i++) {
    if (sentence[i] == ',' || sentence[i] == '\n') {
      String field = sentence.substring(lastIndex, i);
      
      if (commaCount == 7) {
        gps_sats = field.toInt();
      } else if (commaCount == 9) {
        if (field.length() > 0) {
          gps_alt = field.toFloat();
        }
      }
      
      lastIndex = i + 1;
      commaCount++;
    }
  }
}

void parseRMC(String sentence) {
  int commaCount = 0;
  int lastIndex = 0;
  
  for (int i = 0; i < sentence.length(); i++) {
    if (sentence[i] == ',' || sentence[i] == '\n') {
      String field = sentence.substring(lastIndex, i);
      
      if (commaCount == 2) {
        gps_fix = (field == "A");  // A=activo, V=inválido
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
  
  int dotIndex = coord.indexOf('.');
  int degreeDigits = dotIndex - 2;
  
  if (degreeDigits <= 0) return 0.0;
  
  float degrees = coord.substring(0, degreeDigits).toFloat();
  float minutes = coord.substring(degreeDigits).toFloat();
  
  return degrees + (minutes / 60.0);
}
```

---

## ⏱️ TIEMPO OBTENCIÓN FIX GPS

```
PRIMER ENCENDIDO (Cold Start):
  ⏱️ 2-5 MINUTOS en exterior
  ⏱️ Sin obstáculos (cielo abierto)
  ⏱️ Antena hacia arriba

ENCENDIMIENTO POSTERIOR (Warm Start):
  ⏱️ 30-60 segundos
  
ENCENDIMIENTO CON ÚLTIMA POSICIÓN (Hot Start):
  ⏱️ 5-15 segundos
```

---

## 📍 VERIFICACIÓN EXTERIOR

**⚠️ GPS funciona mejor en EXTERIOR**

```
✅ Funciona mejor en EXTERIOR:
   - Cielo completamente despejado
   - Sin árboles/edificios cerca
   - Antena apuntando al cielo
   - Esperar 2-5 MINUTOS la primera vez

⚠️ En interior: Difícil obtener señal (0 satélites)
```

---

## 📊 INTERPRETACIÓN DATOS

### Satélites

```
0 satélites       ❌ Sin fix (sigue buscando)
3 satélites       ⚠️ Fix débil
4-5 satélites     ✓ Fix normal
6-10 satélites    ✓✓ Fix excelente
```

### Altitud GPS

```
Altitud es MSLM (sobre nivel del mar):

Madrid centro:    ~640m
Guadarrama:       ~1200m
Nivel del mar:    ~0m
```

### Precisión

```
Altitud GPS: ±5-20 metros típicamente
Lat/Lon:     ±5-30 metros típicamente

Mejor precisión cuantos más satélites
```

---

## ⚠️ CHECKLIST ANTES DE VUELO

```
☐ GPS conectado a D2 (RX) y D4 (TX)
☐ 3.3V conectado
☐ GND conectado
☐ Programa carga sin errores
☐ GPS obtiene fix en 2-5 minutos (en exterior)
☐ Mínimo 4 satélites para datos confiables
☐ Altitud dentro de rango esperado
```

---

## 🚨 TROUBLESHOOTING

### Problema: "Sin fix GPS" después de 10 min

```
Causas:
  ❌ En INTERIOR (GPS no funciona adentro)
  ❌ Antena apuntando al suelo
  ❌ Bajo árboles/edificios
  ❌ Antena defectuosa

Solución:
  1. Ir a exterior completamente despejado
  2. Antena HACIA EL CIELO
  3. Esperar 5 minutos
  4. Mover GPS en diferentes ángulos
```

### Problema: 0 satélites siempre

```
Posibles causas:
  1. GPIO/UART no inicializado (raro)
  2. GPS defectuoso
  3. Antena no conectada

Solución:
  1. Reinicia Arduino
  2. Verifica SoftwareSerial en D2/D4
  3. Prueba con datos GPS RAW (ver verificación)
```

### Problema: Altitud incorrecta

```
GPS altitud puede variar ±20m:
  - Es normal
  - Cuantos más satélites, más precisión
  - No confíes en altitud con <4 satélites
```

---

## 📝 NOTAS IMPORTANTES

```
✅ GPS NECESITA TIEMPO
   Primera búsqueda: 2-5 minutos
   Planifica esto en competencia

✅ GPS es LENTO
   Actualiza posición cada 1 segundo
   No es ideal para datos en tiempo real

✅ GPS es PESADO
   Usa bastante corriente (>100mA)
   Verifica que batería aguante

✅ GPS + Altitud barométrica
   Combinar GPS alt + LPS22HB da mejor precisión
   GPS: posición
   LPS22HB: altitud continua
```

---

## 🚀 SIGUIENTE PASO

Una vez que GPS funcione correctamente, pasar al **Documento 4: Integración APC220**

---

**Fecha:** Enero 2026  
**Proyecto:** CanSat Misión 2  
**Estado:** ✅ Completado
