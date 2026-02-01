# 🧪 ÍNDICE DE PRUEBAS - CanSat Misión 2
## Guía Práctica: Documento → Programa → Verificar

**Fecha:** Enero 2026  
**Proyecto:** CanSat - Detección de Firmas de Combustión

---

## 📋 ESTRUCTURA DE CADA PRUEBA

```
📄 DOCUMENTO → Aprende teoría + conexiones
📝 PROGRAMA → Carga código en Arduino
✅ VERIFICAR → Confirma que funciona
⏱️ TIEMPO → Cuánto tarda
```

---

## 🚀 PRUEBA 1: SENSORES INTEGRADOS

### 📖 Documento a Leer
**Archivo:** `DOCUMENTO_1_SENSORES_INTEGRADOS.md`

**Contenido:**
- ✅ Qué sensores tiene Arduino
- ✅ Cómo funcionan
- ✅ Precisión de cada uno
- ⚠️ Aclaraciones temperatura HS3003

### 💻 Programa a Cargar
**Archivo:** `PROGRAMA_1_SENSORES_INTEGRADOS.ino`

**Ubicación:** `arduino/PROGRAMA_1_SENSORES_INTEGRADOS.ino`

**Pasos:**
1. Abre `PROGRAMA_1_SENSORES_INTEGRADOS.ino` en Arduino IDE
2. Selecciona placa: `Arduino Nano 33 BLE`
3. Selecciona puerto: `COM[X]`
4. Presiona `Ctrl+U` para cargar

### ✅ Verificación
```
Monitor Serial (9600 baud):

❌ MALO:
  IMU... ❌ ERROR
  HS3003... ❌ ERROR

✅ BUENO:
  IMU (BMI270+BMM150)... ✓ OK
  HS3003 (Temp+Humedad)... ✓ OK
  LPS22HB (Presión)... ✓ OK
  
  N° | Temp(HS) | Humedad | Presion | Altitud | AccelZ | GyroX
  0 | 23.5°C   | 65.2%   | 929.5   | 620.1m  | 1.00   | 0.2
  1 | 23.5°C   | 65.1%   | 929.5   | 620.0m  | 1.00   | 0.1
```

### ⏱️ Tiempo
- Lectura documento: **10 min**
- Carga programa: **5 min**
- Verificación: **5 min**
- **Total: ~20 minutos**

### 📝 Datos Esperados
```
Temperatura HS3003:    20-25°C
Humedad:               40-70%
Presión:               ~930 hPa
Altitud:               ~620m
Aceleración Z:         ~1.0 m/s² (gravedad en reposo)
```

### 🚨 Si falla
```
❌ "Arduino no se reconoce"
  → Instalar driver
  → Cambiar puerto USB

❌ "Sensores en ERROR"
  → Presionar RESET doble
  → Verificar que Board sea "Arduino Nano 33 BLE"
  → Reinstalar librerías
```

---

## 🚀 PRUEBA 2: SENSOR SGP30 (GASES)

### 📖 Documento a Leer
**Archivo:** `DOCUMENTO_2_SGP30_GASES.md`

**Contenido:**
- ✅ Qué es SGP30
- ✅ Cómo conectar (⚠️ 3.3V CRÍTICO)
- ✅ Interpretación TVOC/eCO2
- ✅ Firmas de combustión detectables

### 🔌 Conexión Física (VERIFICAR ANTES)
```
Arduino Nano 33 BLE:
  A4 (SDA) ──→ SGP30 SDA
  A5 (SCL) ──→ SGP30 SCL
  3.3V     ──→ SGP30 VCC  (⚠️ NUNCA 5V)
  GND      ──→ SGP30 GND

🧪 VERIFICAR CON MULTÍMETRO:
  VCC en SGP30 = 3.3V exactamente
```

### 💻 Programa a Cargar
**Archivo:** `PROGRAMA_2_SGP30_GASES.ino`

**Ubicación:** `arduino/PROGRAMA_2_SGP30_GASES.ino`

**Pasos:**
1. Abre `PROGRAMA_2_SGP30_GASES.ino`
2. Carga en Arduino (`Ctrl+U`)
3. Abre Monitor Serial (9600 baud)

### ⏳ ESPERAR 15 SEGUNDOS
```
El sensor necesita calibración:
  0-15 seg: "⏳ Esperando estabilización"
  >15 seg:  "✓ Sensor listo"
```

### ✅ Verificación
```
Monitor Serial (9600 baud):

❌ MALO:
  "❌ ERROR"
  "No se encontró SGP30"

✅ BUENO:
  "✓ SGP30 OK"
  "⏳ Esperando estabilización (15 segundos)..."
  "✓ Sensor listo"
  
  N° | TVOC | eCO2 | H2_raw | Ethanol_raw | Estado
  0  | 45   | 410  | 12500  | 18000       | 🟢 Limpio
  1  | 48   | 412  | 12600  | 18100       | 🟢 Limpio
```

### 📊 Interpretación Valores
```
TVOC:
  0-220 ppb     🟢 Limpio
  220-660 ppb   🟡 Normal
  660-2200 ppb  🟠 Moderado
  >2200 ppb     🔴 Alto/Contaminado

eCO2:
  <400 ppm      🟢 Normal
  400-1000 ppm  🟡 Aceptable
  >1000 ppm     🟠 Malo
```

### ⏱️ Tiempo
- Lectura documento: **10 min**
- Conexión física: **5 min**
- Carga programa: **5 min**
- Espera calibración: **15 seg**
- Verificación: **5 min**
- **Total: ~30 minutos**

### 🚨 Si falla
```
❌ "No se encontró SGP30"
  → Verificar A4/A5 conectados
  → VERIFICAR 3.3V con multímetro
  → Presionar RESET doble
  → Recarguar programa

❌ "Valores siempre 0"
  → Esperar 30 segundos más
  → Acerca trapo húmedo (debe cambiar TVOC)
```

---

## 🚀 PRUEBA 3: GPS (POSICIÓN)

### 📖 Documento a Leer
**Archivo:** `DOCUMENTO_3_GPS_POSICION.md`

**Contenido:**
- ✅ Cómo funciona GPS
- ✅ Cómo conectar (SoftwareSerial D2/D4)
- ✅ Tiempo obtención señal
- ⚠️ Funciona mejor en EXTERIOR

### 🔌 Conexión Física
```
Arduino Nano 33 BLE:
  D2 (RX) ← GPS TX
  D4 (TX) → GPS RX
  3.3V    → GPS VCC
  GND     → GND
```

### 💻 Programa a Cargar
**Archivo:** `PROGRAMA_3_GPS_POSICION.ino`

**Ubicación:** `arduino/PROGRAMA_3_GPS_POSICION.ino`

**Pasos:**
1. Abre `PROGRAMA_3_GPS_POSICION.ino`
2. Carga en Arduino
3. Abre Monitor Serial (9600 baud)

### ✅ Verificación
```
Monitor Serial (9600 baud):

⏳ ESPERANDO (en exterior):
  N° | Status | Sat
  0  | ⏳ Wait | 0
  1  | ⏳ Wait | 0
  2  | ⏳ Wait | 2
  3  | ⏳ Wait | 4
  4  | ✓ FIX | 6

✅ FUNCIONANDO:
  N° | Status | Sat | Lat | Lon | Alt | Fix_Time
  100 | ✓ FIX | 6   | 40.46... | -3.74... | 620m | 100s
  101 | ✓ FIX | 7   | 40.46... | -3.74... | 620m | 101s
```

### 🚨 Si falla
```
❌ "0 satélites después de 5+ min en exterior"
  → Problema: GPS defectuoso
  → O: Cables mal conectados
  → Verificar D2/D4 conectados

⚠️ "Posición con 1-2 satélites (muy débil)"
  → Normal: espera más satélites
  → Mueve antena en diferentes ángulos
```

---

## 🚀 PRUEBA 4: MICROSD (GRABACIÓN)

### 📖 Documento a Leer
**Archivo:** `DOCUMENTO_4_MICROSD_GRABACION.md`

**Contenido:**
- ✅ Cómo funciona MicroSD (SPI)
- ✅ Cómo conectar (⚠️ 3.3V CRÍTICO)
- ✅ Formato CSV generado
- ✅ Cómo leer datos después

### 🔌 Conexión Física
```
Arduino Nano 33 BLE (SPI):
  D10 (CS)   → MicroSD CS
  D11 (MOSI) → MicroSD MOSI
  D12 (MISO) → MicroSD MISO
  D13 (SCK)  → MicroSD SCK
  3.3V       → MicroSD VCC  (⚠️ NUNCA 5V)
  GND        → GND

🧪 VERIFICAR CON MULTÍMETRO:
  VCC en MicroSD = 3.3V exactamente
```

### 💾 Preparar MicroSD
```
1. Formatea MicroSD en FAT32
2. Inserta en módulo MicroSD
3. Conecta a Arduino
```

### 💻 Programa a Cargar
**Archivo:** `PROGRAMA_4_MICROSD_GRABACION.ino`

**Ubicación:** `arduino/PROGRAMA_4_MICROSD_GRABACION.ino`

**Pasos:**
1. Abre `PROGRAMA_4_MICROSD_GRABACION.ino`
2. Carga en Arduino
3. Abre Monitor Serial (9600 baud)
4. Espera a ver "Grabado: 0..."

### ✅ Verificación
```
Monitor Serial (9600 baud):

❌ MALO:
  "MicroSD (SPI)... ❌ ERROR"
  "No se crea archivo"

✅ BUENO:
  "MicroSD (SPI)... ✓ OK"
  "Archivo creado: MISSION2.CSV"
  
  ✓ Grabado #0 | T:23.5°C H:65.2% P:929.5hPa TVOC:45ppb
  ✓ Grabado #1 | T:23.5°C H:65.1% P:929.5hPa TVOC:48ppb
```

### 📄 Verificar Archivo
```
1. Detén programa (Ctrl+C)
2. Saca MicroSD del módulo
3. Inserta en lector en PC
4. Abre MISSION2.CSV en Excel
5. Deberías ver datos en formato CSV
```

### 🚨 Si falla
```
❌ "MicroSD no inicializa"
  → Verificar 3.3V con multímetro
  → Verificar D10-D13 conectados
  → Formatear MicroSD FAT32 de nuevo

❌ "No se graba archivo"
  → MicroSD no detectada
  → Probar otra MicroSD
```

---

## 🚀 PRUEBA 5: APC220 (TELEMETRÍA RF)

### 📖 Documento a Leer
**Archivo:** `DOCUMENTO_5_APC220_TELEMETRIA_ACTUALIZADO.md`

**Contenido:**
- ✅ Cómo funciona APC220
- ✅ Configuración (parámetros críticos)
- ✅ Cómo conectar (Serial1 Grove)
- ✅ Pruebas de comunicación

### ⚙️ CONFIGURACIÓN CRÍTICA
```
⚠️ AMBOS APC220 DEBEN ESTAR EN MISMA ONDA

Configuración recomendada:
  Frecuencia: 434 MHz
  Velocidad RF: 9600 bps
  Potencia: 9 (máxima)
  Puerto serie: 9600 bps
  Paridad: 0 (sin)

Comando: WR 434000 3 9 3 0
```

### 🔧 Configurar APC220
**Opción A: Con rfmagic (si tienes Windows)**
- Ver: GUIA_RAPIDA_CONFIGURACION_APC220.md

**Opción B: Con Arduino (más simple)**
- Ver: GUIA_PROGRAMA_CONFIGURACION_APC220.md

### 🔌 Conexión Física
```
Arduino Nano 33 BLE (Serial1):
  RX (Grove pin) ← APC220 TX
  TX (Grove pin) → APC220 RX
  3.3V-5V        → APC220 VCC
  GND            → GND
  
  Antena → Conectada a APC220
```

### 💻 Programa a Cargar
**Archivo:** `PROGRAMA_5_APC220_TELEMETRIA.ino`

**Ubicación:** `arduino/PROGRAMA_5_APC220_TELEMETRIA.ino`

**Pasos:**
1. Abre `PROGRAMA_5_APC220_TELEMETRIA.ino`
2. Carga en Arduino
3. Abre Monitor Serial (9600 baud)

### ✅ Verificación
```
Monitor Serial (9600 baud):

✅ BUENO:
  "Enviando 'HOLA #0'"
  "Enviando 'HOLA #1'"
  "Enviando 'HOLA #2'"
```

---

## 📋 CHECKLIST FINAL

Marca cada prueba completada:

```
PRUEBA 1: Sensores Integrados
  ☐ Cargado PROGRAMA_1
  ☐ Monitor Serial muestra datos

PRUEBA 2: SGP30 (Gases)
  ☐ Verificado 3.3V
  ☐ Cargado PROGRAMA_2
  ☐ TVOC y eCO2 estables

PRUEBA 3: GPS (Posición)
  ☐ Cargado PROGRAMA_3
  ☐ Probado en exterior
  ☐ Obtuvo 4+ satélites

PRUEBA 4: MicroSD (Grabación)
  ☐ Formatada FAT32
  ☐ Cargado PROGRAMA_4
  ☐ Datos se graban en CSV

PRUEBA 5: APC220 (Telemetría)
  ☐ APC220 configurados (ambos igual)
  ☐ Cargado PROGRAMA_5
  ☐ Datos se envían

FINAL:
  ☐ Todas las pruebas OK
  ☐ Listo para cargar PROGRAMA_FINAL
  ☐ ¡¡MISIÓN CUMPLIDA!!
```

---

## 🚀 FLUJO COMPLETO

```
INICIO
  ↓
PRUEBA 1: Sensores Integrados ✓
  ↓
PRUEBA 2: SGP30 ✓
  ↓
PRUEBA 3: GPS ✓
  ↓
PRUEBA 4: MicroSD ✓
  ↓
PRUEBA 5: APC220 ✓
  ↓
CARGAR: PROGRAMA_FINAL_CANSAT_MISION2.ino
  ↓
🚀 ¡¡MISIÓN CUMPLIDA!!
```

---

## 📞 AYUDA RÁPIDA

```
Si algo falla:

1. Consulta sección "Si falla" en la prueba
2. Verifica conexiones físicas
3. Usa multímetro para 3.3V/GND
4. Presiona RESET doble
5. Recarga programa
6. Leer documento completo si persiste
```

---

**¡Buenas pruebas!** 🧪✅

**Siguiente:** PROGRAMA_FINAL_CANSAT_MISION2.ino (cuando todas las pruebas estén OK)

---

**Estado:** ✅ Índice de pruebas actualizado  
**Última actualización:** Enero 2026
**Versión:** Ajustada según pruebas reales
