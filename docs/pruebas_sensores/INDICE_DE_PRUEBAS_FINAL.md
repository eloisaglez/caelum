# ÍNDICE DE PRUEBAS - CanSat Misión 2
## Guía Práctica: Documento → Programa → Verificar

**Fecha:** Febrero 2026  
**Proyecto:** CanSat - Detección de Firmas de Combustión

---

## ESTRUCTURA DE CADA PRUEBA

```
DOCUMENTO → Aprende teoría + conexiones
PROGRAMA  → Carga código en Arduino
VERIFICAR → Confirma que funciona
TIEMPO    → Cuánto tarda
```

---

## PRUEBA 1: SENSORES INTEGRADOS

### Documento a Leer
**Archivo:** `DOCUMENTO_1_SENSORES_INTEGRADOS_PLACA.md`

**Contenido:**
- Qué sensores tiene Arduino
- Cómo funcionan
- Precisión de cada uno
- Aclaraciones temperatura HS3003

### Programa a Cargar
**Archivo:** `PROGRAMA_1_SENSORES_INTEGRADOS.ino`

**Pasos:**
1. Abre el programa en Arduino IDE
2. Selecciona placa: `Arduino Nano 33 BLE`
3. Selecciona puerto: `COM[X]`
4. Presiona `Ctrl+U` para cargar

### Verificación
```
Monitor Serial (9600 baud):

MALO:
  IMU... ERROR
  HS3003... ERROR

BUENO:
  IMU (BMI270+BMM150)... OK
  HS3003 (Temp+Humedad)... OK
  LPS22HB (Presión)... OK
  
  N° | Temp(HS) | Humedad | Presion | Altitud | AccelZ | GyroX
  0 | 23.5°C   | 65.2%   | 929.5   | 620.1m  | 1.00   | 0.2
```

### Tiempo
- Lectura documento: **10 min**
- Carga programa: **5 min**
- Verificación: **5 min**
- **Total: ~20 minutos**

### Datos Esperados
```
Temperatura HS3003:    20-25°C
Humedad:               40-70%
Presión:               ~930 hPa
Altitud:               ~620m
Aceleración Z:         ~1.0 m/s² (gravedad en reposo)
```

### Si falla
```
"Arduino no se reconoce"
  → Instalar driver
  → Cambiar puerto USB

"Sensores en ERROR"
  → Presionar RESET doble
  → Verificar que Board sea "Arduino Nano 33 BLE"
  → Reinstalar librerías
```

---

## PRUEBA 2: SENSOR SGP30 (GASES)

### Documento a Leer
**Archivo:** `DOCUMENTO_2_SGP30.md`

**Contenido:**
- Qué es SGP30
- Cómo conectar (⚠️ 3.3V CRÍTICO)
- Interpretación TVOC/eCO2
- Firmas de combustión detectables

### Conexión Física (VERIFICAR ANTES)
```
Arduino Nano 33 BLE:
  A4 (SDA) → SGP30 SDA
  A5 (SCL) → SGP30 SCL
  3.3V     → SGP30 VCC  (⚠️ NUNCA 5V)
  GND      → SGP30 GND

VERIFICAR CON MULTÍMETRO:
  VCC en SGP30 = 3.3V exactamente
```

### Programa a Cargar
**Archivo:** `PROGRAMA_2_SGP30_GASES.ino`

### ESPERAR 15 SEGUNDOS
```
El sensor necesita calibración:
  0-15 seg: "Esperando estabilización"
  >15 seg:  "Sensor listo"
```

### Verificación
```
Monitor Serial (9600 baud):

MALO:
  "ERROR"
  "No se encontró SGP30"

BUENO:
  "SGP30 OK"
  "Esperando estabilización (15 segundos)..."
  "Sensor listo"
  
  N° | TVOC | eCO2 | H2_raw | Ethanol_raw | Estado
  0  | 45   | 410  | 12500  | 18000       | Limpio
```

### Interpretación Valores
```
TVOC:
  0-220 ppb     Limpio
  220-660 ppb   Normal
  660-2200 ppb  Moderado
  >2200 ppb     Alto/Contaminado

eCO2:
  <400 ppm      Normal
  400-1000 ppm  Aceptable
  >1000 ppm     Malo
```

### Tiempo
- Lectura documento: **10 min**
- Conexión física: **5 min**
- Carga programa: **5 min**
- Espera calibración: **15 seg**
- Verificación: **5 min**
- **Total: ~30 minutos**

### Si falla
```
"No se encontró SGP30"
  → Verificar A4/A5 conectados
  → VERIFICAR 3.3V con multímetro
  → Presionar RESET doble

"Valores siempre 0"
  → Esperar 30 segundos más
  → Acerca trapo húmedo (debe cambiar TVOC)
```

---

## PRUEBA 3: GPS (POSICIÓN)

### Documento a Leer
**Archivo:** `DOCUMENTO_3_SENSOR_GPS_POSICION.md`

**Contenido:**
- Cómo funciona GPS
- Cómo conectar
- Tiempo obtención señal
- Funciona mejor en EXTERIOR

### Conexión Física
```
Arduino Nano 33 BLE:
  D2 (RX) ← GPS TX
  D4 (TX) → GPS RX
  3.3V    → GPS VCC
  GND     → GND
```

### Programa a Cargar
**Archivo:** `PROGRAMA_3_GPS_POSICION.ino`

### Verificación
```
Monitor Serial (9600 baud):

ESPERANDO (en exterior):
  N° | Status | Sat
  0  | Wait   | 0
  1  | Wait   | 0
  2  | Wait   | 2
  3  | Wait   | 4
  4  | FIX    | 6

FUNCIONANDO:
  N° | Status | Sat | Lat | Lon | Alt | Fix_Time
  100 | FIX   | 6   | 40.46... | -3.74... | 620m | 100s
```

### Si falla
```
"0 satélites después de 5+ min en exterior"
  → Problema: GPS defectuoso
  → O: Cables mal conectados
  → Verificar D2/D4 conectados

"Posición con 1-2 satélites (muy débil)"
  → Normal: espera más satélites
  → Mueve antena en diferentes ángulos
```

---

## PRUEBA 4: MICROSD (GRABACIÓN)

### Documento a Leer
**Archivo:** `DOCUMENTO_4_MICROSD_GRABACION.md`

**Contenido:**
- Cómo funciona MicroSD (SPI)
- Cómo conectar (⚠️ 3.3V CRÍTICO)
- Formato CSV generado
- Cómo leer datos después

### Conexión Física
```
Arduino Nano 33 BLE (SPI):
  D10 (CS)   → MicroSD CS
  D11 (MOSI) → MicroSD MOSI
  D12 (MISO) → MicroSD MISO
  D13 (SCK)  → MicroSD SCK
  3.3V       → MicroSD VCC  (⚠️ NUNCA 5V)
  GND        → GND

VERIFICAR CON MULTÍMETRO:
  VCC en MicroSD = 3.3V exactamente
```

### Preparar MicroSD
```
1. Formatea MicroSD en FAT32
2. Inserta en módulo MicroSD
3. Conecta a Arduino
```

### Programa a Cargar
**Archivo:** `PROGRAMA_4_MICROSD_GRABACION.ino`

### Verificación
```
Monitor Serial (9600 baud):

MALO:
  "MicroSD (SPI)... ERROR"
  "No se crea archivo"

BUENO:
  "MicroSD (SPI)... OK"
  "Archivo creado: MISSION2.CSV"
  
  Grabado #0 | T:23.5°C H:65.2% P:929.5hPa TVOC:45ppb
  Grabado #1 | T:23.5°C H:65.1% P:929.5hPa TVOC:48ppb
```

### Verificar Archivo
```
1. Detén programa
2. Saca MicroSD del módulo
3. Inserta en lector en PC
4. Abre MISSION2.CSV en Excel
5. Deberías ver datos en formato CSV
```

### Si falla
```
"MicroSD no inicializa"
  → Verificar 3.3V con multímetro
  → Verificar D10-D13 conectados
  → Formatear MicroSD FAT32 de nuevo

"No se graba archivo"
  → MicroSD no detectada
  → Probar otra MicroSD
```

---

## PRUEBA 5: APC220 (TELEMETRÍA RF)

### Documento a Leer
**Archivo:** `DOCUMENTO_5_APC220_TELEMETRIA.md`

**Contenido:**
- Cómo funciona APC220
- Configuración con Arduino UNO
- Conexiones correctas
- Pruebas de comunicación

### CONFIGURACIÓN CRÍTICA

**Nota:** Otros métodos como rfmagic, PuTTY o terminales no funcionaron. 
Usar Arduino UNO como configurador.

```
AMBOS APC220 DEBEN TENER LA MISMA CONFIGURACIÓN

Configuración recomendada:
  Frecuencia: 434 MHz (434000)
  Velocidad RF: 9600 bps
  Potencia: 9 (máxima)
  Puerto serie: 9600 bps
  Paridad: 0 (sin)

Comando: WR 434000 3 9 3 0
```

### Paso 1: Configurar APC220 con Arduino UNO

**Conexión Arduino UNO ↔ APC220:**
```
Arduino UNO     APC220
───────────────────────
GND        →    GND
D13        →    VCC
D12        →    EN
D11        →    RXD
D10        →    TXD
D8         →    SET
```

**Programa:** `PROGRAMA_APC220_CONFIGURADOR.ino`

1. Carga el programa en Arduino UNO
2. Abre Monitor Serie a 9600 baud
3. Escribe: `WR 434000 3 9 3 0`
4. Verifica con: `RD`
5. Debe responder: `PARA 434000 3 9 3 0`
6. **REPITE con el segundo APC220**

### Paso 2: Conexión para Telemetría

**IMPORTANTE: Conexiones DIRECTAS (no cruzadas)**

La etiqueta TXD/RXD del APC220 indica dónde conectar el pin del micro:
- TX del micro → TXD del APC220
- RX del micro → RXD del APC220

**Emisor (Nano 33 BLE Sense):**
```
Nano 33 BLE     APC220
───────────────────────
Pin 0 (RX)  →   RXD
Pin 1 (TX)  →   TXD
3.3V        →   VCC
GND         →   GND

NOTA: El pin EN puede dejarse sin conectar.
Compatible con conector Grove.
```

**Receptor (Arduino UNO):**
```
Misma conexión que para configurar.
```

### Programas a Cargar

**Emisor (Nano 33 BLE):** `PROGRAMA_APC220_EMISOR.ino`
**Receptor (Arduino UNO):** `PROGRAMA_APC220_RECEPTOR.ino`

### Verificación
```
Monitor Serial del RECEPTOR debe mostrar:

Receptor APC220 listo...
Esperando datos...

HOLA
HOLA
HOLA
(cada 2 segundos)
```

### Si falla
```
"No hay comunicación"
  → ¿Misma configuración en ambos? Verificar con RD
  → ¿Conexiones directas (no cruzadas)?
  → ¿Antenas conectadas en ambos?

"Nano 33 BLE no funciona con SoftwareSerial"
  → Correcto, usar Serial1 (pines 0 y 1)
  → Arduino UNO sí funciona con SoftwareSerial
```

---

## CHECKLIST FINAL

Marca cada prueba completada:

```
PRUEBA 1: Sensores Integrados
  [ ] Cargado PROGRAMA_1
  [ ] Monitor Serial muestra datos

PRUEBA 2: SGP30 (Gases)
  [ ] Verificado 3.3V
  [ ] Cargado PROGRAMA_2
  [ ] TVOC y eCO2 estables

PRUEBA 3: GPS (Posición)
  [ ] Cargado PROGRAMA_3
  [ ] Probado en exterior
  [ ] Obtuvo 4+ satélites

PRUEBA 4: MicroSD (Grabación)
  [ ] Formateada FAT32
  [ ] Cargado PROGRAMA_4
  [ ] Datos se graban en CSV

PRUEBA 5: APC220 (Telemetría)
  [ ] APC220 configurados con Arduino UNO
  [ ] Ambos con PARA 434000 3 9 3 0
  [ ] Conexiones directas (no cruzadas)
  [ ] Datos se reciben en receptor

FINAL:
  [ ] Todas las pruebas OK
  [ ] Listo para cargar PROGRAMA_FINAL
  [ ] ¡MISIÓN CUMPLIDA!
```

---

## FLUJO COMPLETO

```
INICIO
  ↓
PRUEBA 1: Sensores Integrados
  ↓
PRUEBA 2: SGP30
  ↓
PRUEBA 3: GPS
  ↓
PRUEBA 4: MicroSD
  ↓
PRUEBA 5: APC220
  ↓
CARGAR: PROGRAMA_FINAL_CANSAT_TELEMETRIA.ino
  ↓
¡MISIÓN CUMPLIDA!
```

---

## AYUDA RÁPIDA

```
Si algo falla:

1. Consulta sección "Si falla" en la prueba
2. Verifica conexiones físicas
3. Usa multímetro para 3.3V/GND
4. Presiona RESET doble
5. Recarga programa
6. Consulta TROUBLESHOOTING_COMPLETO.md
```

---

**¡Buenas pruebas!**

**Siguiente:** PROGRAMA_FINAL_CANSAT_TELEMETRIA.ino (cuando todas las pruebas estén OK)

---

**Estado:** Índice de pruebas actualizado  
**Última actualización:** Febrero 2026
