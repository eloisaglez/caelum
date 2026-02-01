# 🧪 ÍNDICE DE PRUEBAS - CanSat Misión 2
## Guía Práctica: Documento → Programa → Verificar

**Fecha:** Enero 2026  
**Proyecto:** CanSat - Detección de Firmas de Combustión  
**Centro:** IES Diego Velázquez

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
Temperatura HS3003:    20-25°C (ambiente ~15-20°C)
Humedad:               40-70%
Presión:               ~930 hPa (Madrid)
Altitud:               ~620m (Las Rozas)
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

### 🎯 Próximo paso
⬇️ Si todo funciona → **PRUEBA 2**

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
- Verificación multímetro: **5 min**
- Carga programa: **5 min**
- Espera calibración: **15 seg**
- Verificación: **5 min**
- **Total: ~45 minutos**

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

⚠️ "Conecté a 5V accidentalmente"
  → SGP30 está DAÑADO
  → Conseguir otro
```

### ✅ Prueba Adicional
```
Acerca algo con olor (trapo con perfume/alcohol):
  → TVOC debe AUMENTAR
  → eCO2 debe cambiar
  → Si no cambia: problema de conexión
```

### 🎯 Próximo paso
⬇️ Si todo funciona → **PRUEBA 3**

---

## 🚀 PRUEBA 3: GPS (POSICIÓN)

### 📖 Documento a Leer
**Archivo:** `DOCUMENTO_3_GPS_POSICION.md`

**Contenido:**
- ✅ Cómo funciona GPS
- ✅ Cómo conectar (SoftwareSerial D2/D4)
- ✅ Tiempo obtención señal (2-5 min)
- ⚠️ SOLO funciona en EXTERIOR

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
3. **¡¡IMPORTANTE!!** Lleva Arduino a EXTERIOR
4. Abre Monitor Serial (9600 baud)
5. Apunta antena GPS AL CIELO

### ✅ Verificación
```
Monitor Serial (9600 baud):

❌ MALO (interior):
  N° | Status | Sat
  ───┼────────┼─────
  0  | ⏳ Wait | 0
  1  | ⏳ Wait | 0
  2  | ⏳ Wait | 0
  (después de 10 min: sigue 0 satélites)

✅ BUENO (exterior, 2-5 min):
  N° | Status | Sat | Lat | Lon | Alt | Fix_Time
  ───┼────────┼─────┼─────┼─────┼─────┼──────────
  120 | ✓ FIX | 6   | 40.4626 | -3.7463 | 620.1m | 120s
  121 | ✓ FIX | 7   | 40.4626 | -3.7463 | 620.2m | 121s
```

### 📊 Números Esperados (Brunete)
```
Latitud:  ~40.46°
Longitud: ~-3.74°
Altitud:  ~620m
Satélites: 4-10 (cuantos más, mejor)
Tiempo: 2-5 MINUTOS para primer fix
```

### ⏱️ Tiempo
- Lectura documento: **10 min**
- Conexión física: **5 min**
- Carga programa: **5 min**
- **Ir a exterior + esperar GPS: 5-10 MIN**
- **Total: ~35 minutos**

### ⚠️ IMPORTANTE
```
❌ NO FUNCIONA EN INTERIOR
   (aunque esperes 30 minutos)

✅ DEBE ESTAR EN EXTERIOR
   • Cielo despejado
   • Sin árboles/edificios
   • Antena hacia ARRIBA
```

### 🚨 Si falla
```
❌ "0 satélites después de 10 min en exterior"
  → Problema: GPS defectuoso
  → O: Cables mal conectados
  → Verificar D2/D4 conectados

❌ "Posición con 1-2 satélites (muy débil)"
  → Normal: espera más satélites
  → Mueve antena en diferentes ángulos
```

### 🎯 Próximo paso
⬇️ Si todo funciona → **PRUEBA 4**

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
1. Formatea MicroSD en FAT32 (Windows/Mac)
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
  ✓ Grabado #2 | T:23.5°C H:65.0% P:929.5hPa TVOC:50ppb
```

### 📄 Verificar Archivo
```
1. Detén programa (Ctrl+C)
2. Saca MicroSD del módulo
3. Inserta en lector en PC
4. Abre MISSION2.CSV en Notepad/Excel
5. Deberías ver datos en formato CSV:
   
   tiempo,temperatura,humedad,presion,tvoc,eco2,h2,ethanol
   0,23.50,65.2,929.5,45,410,12500,18000
   1,23.50,65.1,929.5,48,412,12600,18100
```

### ⏱️ Tiempo
- Lectura documento: **10 min**
- Preparar MicroSD: **5 min**
- Conexión física: **5 min**
- Carga programa: **5 min**
- Verificación: **10 min**
- **Total: ~35 minutos**

### 🚨 Si falla
```
❌ "MicroSD no inicializa"
  → Verificar 3.3V con multímetro
  → Verificar D10/D11/D12/D13 conectados
  → Formatear MicroSD de nuevo

❌ "No se graba archivo"
  → MicroSD no detectada
  → Probar otra MicroSD

❌ "Archivo vacío después de 30 seg"
  → Buffer no se flushed
  → Código no cierra archivo correctamente
```

### 🎯 Próximo paso
⬇️ Si todo funciona → **PRUEBA 5**

---

## 🚀 PRUEBA 5: APC220 (TELEMETRÍA RF)

### 📖 Documento a Leer
**Archivo:** `DOCUMENTO_5_APC220_TELEMETRIA.md`

**Contenido:**
- ✅ Cómo funciona APC220
- ✅ Cómo conectar (Serial1 Grove)
- ✅ Alcance RF (300-1000m)
- ✅ Pruebas de recepción

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

❌ MALO:
  (Nada aparece)
  o
  "ERROR: No data"

✅ BUENO:
  "Enviando 'HOLA #0'"
  "Enviando 'HOLA #1'"
  "Enviando 'HOLA #2'"
```

### 📡 Prueba de Recepción (CON SEGUNDO ARDUINO/PC)
```
1. Conecta receptor APC220 a otro Arduino o PC
2. Abre terminal en puerto COM
3. Deberías recibir:
   "HOLA #0"
   "HOLA #1"
   "HOLA #2"
```

### 🧪 Test de Alcance
```
1. Carga programa en Arduino CanSat
2. Aleja receptor APC220 paulatinamente
3. Anota distancia a la que falla recepción

Esperado:
  • 100m línea vista: ✅ Perfectamente
  • 300m línea vista: ✅ Bueno
  • 500m línea vista: ⚠️ Débil
  • >1000m: ❌ Falla
```

### ⏱️ Tiempo
- Lectura documento: **10 min**
- Conexión física: **5 min**
- Carga programa: **5 min**
- Verificación básica: **5 min**
- Test de alcance: **15 min** (opcional)
- **Total: ~40 minutos**

### 🚨 Si falla
```
❌ "No se reciben datos"
  → Verificar conexión Serial1 (Grove)
  → Comprobar que APC220 está alimentado
  → Verificar antena conectada

❌ "Alcance muy corto"
  → Interferencia RF en zona
  → Antenas desalineadas
  → Normal en ambiente urbano
```

### 🎯 ¿Próximo paso?
✅ **TODAS LAS PRUEBAS COMPLETADAS** 

Ahora puedes:
- ✅ Cargar **PROGRAMA_FINAL_CANSAT_MISION2.ino**
- ✅ Todos los sensores funcionan juntos
- ✅ Listo para **BRUNETE 2026**

---

## 📋 CHECKLIST FINAL

Marca cada prueba completada:

```
PRUEBA 1: Sensores Integrados
  ☐ Leído DOCUMENTO_1
  ☐ Cargado PROGRAMA_1
  ☐ Monitor Serial muestra datos
  ☐ Valores coherentes

PRUEBA 2: SGP30 (Gases)
  ☐ Leído DOCUMENTO_2
  ☐ Verificado 3.3V con multímetro
  ☐ Cargado PROGRAMA_2
  ☐ Esperado 15 segundos calibración
  ☐ TVOC y eCO2 estables

PRUEBA 3: GPS (Posición)
  ☐ Leído DOCUMENTO_3
  ☐ Cargado PROGRAMA_3
  ☐ Probado en EXTERIOR
  ☐ Antena hacia ARRIBA
  ☐ Obtuvo 4+ satélites
  ☐ Posición dentro de Brunete

PRUEBA 4: MicroSD (Grabación)
  ☐ Leído DOCUMENTO_4
  ☐ Verificado 3.3V con multímetro
  ☐ MicroSD formateada FAT32
  ☐ Cargado PROGRAMA_4
  ☐ Datos se graban en MISSION2.CSV
  ☐ Archivo legible en Excel

PRUEBA 5: APC220 (Telemetría)
  ☐ Leído DOCUMENTO_5
  ☐ Cargado PROGRAMA_5
  ☐ Datos se envían correctamente
  ☐ Receptor recibe datos (opcional)
  ☐ Alcance verificado

FINAL:
  ☐ Todas las pruebas VERDES
  ☐ Listo para cargar PROGRAMA_FINAL
  ☐ ¡¡A BRUNETE!!
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
VERIFICAR: Todos juntos funcionan ✓
  ↓
🚀 ¡¡A BRUNETE!!
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

**Estado:** ✅ Índice de pruebas completo  
**Última actualización:** Enero 2026  
**Autor:** IES Diego Velázquez
