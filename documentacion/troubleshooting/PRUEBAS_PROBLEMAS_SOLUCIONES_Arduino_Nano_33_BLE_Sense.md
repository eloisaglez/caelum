# Arduino Nano 33 BLE Sense Rev2 - CanSat Project
## Pruebas, Problemas y Soluciones

**Autor:** Eloísa González Medina  
**Centro:** IES Diego Velázquez - Bilingual Secondary School  
**Proyecto:** CanSat Competition 2026  
**Fecha:** Enero–Febrero 2026  
**Hardware:** Arduino Nano 33 BLE Sense Rev2 + Sensores externos  
**Alimentación:** Pila 9V ion litio + TP4056  

---

## Índice

1. [Hardware Utilizado](#hardware-utilizado)
2. [Problemas Encontrados y Soluciones](#problemas-encontrados-y-soluciones)
3. [Errores Comunes y Cómo Solucionarlos](#errores-comunes-y-cómo-solucionarlos)
4. [Pruebas Realizadas](#pruebas-realizadas)
5. [Sensores Finales](#sensores-finales)
6. [Configuración Final](#configuración-final)
7. [Lecciones Aprendidas](#lecciones-aprendidas)

---

## Hardware Utilizado

### Arduino Principal
- **Arduino Nano 33 BLE Sense Rev2**
- Procesador: nRF52840 (ARM Cortex-M4)
- Arquitectura: MBED (NO AVR)
- Puerto: COM5 (después de resolver drivers)

### Sensores Integrados
| Sensor | Modelo | Función | Estado |
|--------|--------|---------|--------|
| Acelerómetro + Giroscopio | BMI270 | Movimiento + Rotación | ✅ Funciona |
| Magnetómetro | BMM150 | Brújula/Orientación | ✅ Funciona |
| Presión + Temperatura | LPS22HB | Altitud + Temperatura | ✅ Funciona |
| Humedad + Temperatura | HS300x | Humedad + Temperatura | ✅ Funciona |
| Humedad + Temperatura | HTS221 | — | ❌ No presente (versión Lite) |
| Luz/Color/Proximidad | APDS9960 | Luz ambiente | ✅ Funciona |

### Sensores Externos
| Sensor | Modelo | Conexión | Estado |
|--------|--------|----------|--------|
| CO₂ + T + HR | SCD40 | I2C | ✅ Funciona |
| Partículas PM1.0/PM2.5/PM10 | HM3301 | I2C | ✅ Funciona |
| GPS | ATGM336H | UART | ✅ Funciona (fix en exterior) |
| Módulo RF | APC220 | UART | ⚠️ Requiere configuración frecuencia |

### Almacenamiento
- **MicroSD:** Adafruit MicroSD breakout board
- **Librería:** SdFat (NO la librería SD estándar — incompatible con MBED)
- **Formato:** FAT32

### Alimentación
- **Batería:** Pila 9V ion litio
- **Módulo de protección:** TP4056
- **Voltaje regulado:** 3.3V (integrado en Arduino)

---

## Problemas Encontrados y Soluciones

### Problema 1: Sensor HTS221 No Se Inicializa
**Síntoma:**
```
Failed to initialize humidity temperature sensor!
```

**Causa:** La placa es versión "Lite" — el HTS221 no está soldado.

**Intentos fallidos:**
- ❌ Librería Arduino_HTS221 oficial
- ❌ Librería Adafruit HTS221
- ❌ Librería FaBo 208 HTS221 (además incompatible AVR vs MBED)
- ❌ Cambiar cables USB
- ❌ Reinstalar drivers

**Solución:** Eliminar completamente HTS221 del código. Usar HS300x (sí presente en Rev2) para humedad y temperatura.

---

### Problema 2: Puerto COM No Se Reconoce
**Síntoma:**
```
No device found on COM1
Failed uploading: uploading error: exit status 1
```

**Causa:** Faltan drivers — el Arduino Nano 33 BLE Sense necesita DOS cosas:
1. Driver CH340 en Windows
2. Paquete "Arduino Mbed OS Nano Boards" en Arduino IDE

**Solución:**
1. Descargar e instalar driver CH340: https://www.wch.cn/downloads/CH341SER_EXE.html
2. En Arduino IDE → Tools → Board Manager → instalar "Arduino Mbed OS Nano Boards" v4.5.0+
3. Reiniciar PC y Arduino IDE
4. Conectar Arduino → debería aparecer el puerto COM

---

### Problema 3: Librería SD Incompatible con MBED
**Síntoma:**
```
SD initialization failed!
```
O el programa compila pero la MicroSD no responde.

**Causa:** La librería `SD` estándar de Arduino usa funciones AVR incompatibles con la arquitectura MBED del nRF52840.

**Solución:** Usar **SdFat** en vez de SD:
```cpp
// MAL — no funciona con MBED
#include <SD.h>

// BIEN — compatible con MBED
#include <SdFat.h>
SdFat sd;
SdFile archivo;
```

---

### Problema 4: Librería Incompatible con Arquitectura
**Síntoma:**
```
ATENCIÓN: la librería FaBo 208 Humidity HTS221 pretende ejecutarse 
sobre arquitectura(s) avr y puede ser incompatible con tu actual tarjeta 
la cual corre sobre arquitectura(s) mbed_nano.
```

**Causa:** La librería está diseñada para Arduino AVR, no para MBED.

**Solución:** Usar únicamente librerías oficiales de Arduino o compatibles con MBED. Verificar siempre "Supported architectures" antes de instalar.

---

### Problema 5: Arduino IDE No Detecta Placa
**Síntoma:**
- Tools → Board: No se puede seleccionar placa
- Tools → Port: Aparece vacío

**Causa:**
- Desinstalación accidental de "Arduino Mbed OS Nano Boards"
- Caché corrupta de Arduino IDE

**Solución:**
1. Reinstalar "Arduino Mbed OS Nano Boards v4.5.0+"
2. Si persiste, limpiar caché: `C:\Users\[Usuario]\AppData\Local\Arduino15`
3. Reiniciar Arduino IDE

---

### Problema 6: APC220 No Comunica
**Síntoma:** El módulo de tierra no recibe datos aunque el CanSat esté transmitiendo.

**Causa:** Los dos módulos APC220 tienen parámetros diferentes (frecuencia, baudrate).

**Solución:** Configurar ambos módulos con exactamente los mismos parámetros usando el software rfmagic. Ver `IMPORTANTE_CAMBIO_FRECUENCIA.md` para detalles completos.

---

### Problema 7: Firebase Error 400 al Limpiar Datos
**Síntoma:**
```
Error 400: Data to write exceeds maximum size
```

**Causa:** Intentar borrar demasiados datos de Firebase en una sola petición DELETE.

**Solución:** Usar `limpiar_firebase.py` que borra por lotes con ThreadPoolExecutor en vez de una sola petición.

---

### Problema 8: Firebase Saturado con Datos de Espera
**Síntoma:** Firebase acumula miles de registros de fase `espera` antes del lanzamiento, saturando la base de datos.

**Causa:** `receptor_telemetria.py` enviaba todos los datos a Firebase independientemente de la fase.

**Solución:** Filtrar por fase en `receptor_telemetria.py` — solo enviar a Firebase durante fases activas (`caida_libre`, `apertura`, `descenso`, `tierra`). El CSV local (`datos_SD_raw.csv`) sigue guardando todo.

---

## Errores Comunes y Cómo Solucionarlos

### Errores de compilación Arduino

| Error | Causa | Solución |
|-------|-------|---------|
| `'SD' was not declared` | Librería SD no compatible con MBED | Usar SdFat |
| `Failed to initialize HTS221` | Sensor no presente en versión Lite | Eliminar del código |
| `architecture avr incompatible with mbed_nano` | Librería para AVR, no MBED | Usar librería oficial Arduino |
| `exit status 1` al subir | Driver CH340 no instalado | Instalar CH340 + Mbed OS Nano Boards |
| `No device found on COMx` | Puerto no detectado | Instalar drivers, reiniciar |

### Errores de sensores en tiempo de ejecución

| Error en Serial Monitor | Causa | Solución |
|------------------------|-------|---------|
| `BMI270 init failed` | I2C desconectado o voltaje incorrecto | Verificar conexión 3.3V y GND |
| `LPS22HB init failed` | I2C desconectado | Verificar conexión |
| `SCD40 init failed` | I2C desconectado o dirección incorrecta | Verificar dirección I2C (0x62) |
| `HM3301 init failed` | I2C desconectado | Verificar conexión |
| `SD init failed` | MicroSD no formateada o no insertada | Formatear FAT32, verificar inserción |
| CO₂ = 0 ppm | SCD40 no listo (tarda ~5s en arrancar) | Esperar inicialización, filtrar 0 en código |
| GPS sin fix | En interior o señal débil | Probar en exterior, esperar 1-2 min |

### Errores de Python — análisis post-vuelo

| Error | Causa | Solución |
|-------|-------|---------|
| `ModuleNotFoundError: folium` | Librería no instalada | `pip install folium` |
| `KeyError: 'pm2_5'` | Nombre de columna incorrecto en CSV | Verificar cabecera del CSV (27 columnas) |
| `No such file: datos_SD.csv` | CSV no encontrado | Verificar ruta y nombre del fichero |
| `UserWarning: Glyph missing` | Emoji en título de gráfica matplotlib | Sustituir emojis por texto en títulos |
| Sin datos GPS en mapa | lat/lon = 0 en todo el CSV | Normal si no hubo fix GPS — mapa omitido |

### Errores de Firebase

| Error | Causa | Solución |
|-------|-------|---------|
| Error 400 al borrar | Petición demasiado grande | Usar `limpiar_firebase.py` con batch |
| Dashboard no actualiza | `limitToLast(1)` no recibe nuevos datos | Verificar que el playback está corriendo |
| Línea trayectoria completa al abrir | Datos históricos en Firebase | Dashboard filtra por timestamp de conexión |
| Firebase lleno con datos `espera` | Receptor enviaba todos los datos | Filtro de fases en `receptor_telemetria.py` |

### Errores de comunicación APC220

| Síntoma | Causa | Solución |
|---------|-------|---------|
| Sin datos en receptor | Frecuencias diferentes | Configurar ambos módulos con rfmagic |
| Datos corruptos | Baudrate diferente entre módulos | Igualar baudrate (9600) en ambos módulos |
| Módulo no detectado por PC | Driver USB-TTL no instalado | Instalar driver CH340 para el adaptador |
| Alcance muy corto | Potencia TX baja | Configurar potencia máxima (9) en rfmagic |

---

## Pruebas Realizadas

### Test 1: Inicialización de Sensores
| Sensor | Inicializa | Puerto | Notas |
|--------|-----------|--------|-------|
| BMI270 | ✅ Sí | I2C | Sin problemas |
| BMM150 | ✅ Sí | I2C | Sin problemas |
| LPS22HB | ✅ Sí | I2C | Funciona perfectamente |
| HS300x | ✅ Sí | I2C | Humedad + temperatura |
| APDS9960 | ✅ Sí | I2C | Sin problemas |
| HTS221 | ❌ No | I2C | No existe en versión Lite |
| SCD40 | ✅ Sí | I2C | CO₂ + T + HR |
| HM3301 | ✅ Sí | I2C | PM1.0/PM2.5/PM10 |
| ATGM336H | ✅ Sí | UART | Fix en exterior |
| MicroSD (SdFat) | ✅ Sí | SPI | FAT32, datos_SD_raw.csv (datos crudos) |

### Test 2: Lecturas de Sensores en Reposo
```
ACELERACIÓN (BMI270):
- X: ≈0.00 m/s²  Y: ≈0.00 m/s²  Z: ≈1.00 m/s² (gravedad)

GIROSCOPIO (BMI270):
- X, Y, Z: ≈0.0-0.2 deg/s (ruido normal)

PRESIÓN (LPS22HB):
- Las Rozas: ≈929.5 hPa

ALTITUD:
- Calibrada a 0m en lanzamiento — varía ±2m por fluctuaciones

CO₂ (SCD40):
- Reposo interior: ≈420-450 ppm

PARTÍCULAS (HM3301):
- Interior limpio: PM2.5 ≈ 5-15 µg/m³
```

### Test 3: Calibración de Altitud
```
Presión referencia Las Rozas: 929.5 hPa
Altitud referencia: 0.0 m (punto de lanzamiento)

Subir 1 piso (~3m):   Altitud = +3.1m ✅
Subir 2 pisos (~6m):  Altitud = +6.2m ✅
Bajar planta (-3m):   Altitud = -3.0m ✅
```

### Test 4: Detección de Fases de Vuelo
| Fase | Condición | Resultado |
|------|-----------|-----------|
| espera | Estático en tierra | ✅ Detectada |
| caida_libre | Aceleración < umbral | ✅ Detectada |
| apertura | Cambio brusco aceleración | ✅ Detectada |
| descenso | Bajada lenta estable | ✅ Detectada |
| tierra | Sin movimiento en suelo | ✅ Detectada |

### Test 5: Almacenamiento MicroSD
- Escritura de `datos_SD_raw.csv`: ✅ 1 muestra/segundo
- 27 columnas: ✅ Formato correcto (num_paquete, equipo + 25 campos)
- Backup RAM: ✅ Cada 2 segundos
- Extracción con `extraer_ram.py`: ✅ Funciona por serial

---

## Sensores Finales

| Sensor | Modelo | Precisión | Utilidad para CanSat |
|--------|--------|-----------|----------------------|
| Acelerómetro | BMI270 | ±4g | Detectar caída, impacto, fases |
| Giroscopio | BMI270 | ±2000 deg/s | Detectar rotación en vuelo |
| Magnetómetro | BMM150 | ±1300µT | Orientación, brújula |
| Presión | LPS22HB | ±0.1 hPa | Base para cálculo de altitud |
| Temperatura | LPS22HB | ±1.5°C | Validación cruzada |
| Altitud | LPS22HB (calculada) | ±10-20m | Crítica para perfiles verticales |
| Humedad + Temp | HS300x | ±3% HR / ±0.3°C | Referencia principal T+HR |
| CO₂ + T + HR | SCD40 | ±10 ppm / ±0.5°C | Validación sensor + T+HR |
| PM1.0/PM2.5/PM10 | HM3301 | ±10% | Detección de partículas — misión principal |
| GPS | ATGM336H | ±2.5m | Trayectoria, mapa, KML |

---

## Configuración Final

### Arduino IDE
```
Board: Arduino Nano 33 BLE
Port: COM5 (o el que aparezca)
Upload Speed: 115200
Programmer: Default
```

### Librerías necesarias
```
Arduino_BMI270_BMM150    ✅ Sensores IMU
Arduino_LPS22HB          ✅ Presión/Temperatura
Arduino_HS300x           ✅ Humedad/Temperatura
Arduino_APDS9960         ✅ Luz/Proximidad
SdFat                    ✅ MicroSD (MBED compatible)
ReefwingLPS22HB          ✅ Altitud mejorada
SoftwareSerial           ✅ GPS y APC220

EVITAR:
SD (estándar)            ❌ Incompatible con MBED
FaBo (cualquier)         ❌ Arquitectura AVR, no MBED
Arduino_HTS221           ❌ Sensor no presente en Rev2 Lite
```

### Programa principal
- **Archivo:** `CANSAT_VUELO_INTEGRADO.ino`
- Todos los sensores integrados y externos
- Detección automática de fases de vuelo
- Almacenamiento en MicroSD (datos_SD_raw.csv, datos crudos) + backup RAM
- Telemetría via APC220

### Configuración de altitud
```cpp
// ACTUALIZAR ANTES DE CADA VUELO según AEMET
float seaLevelPressure = 929.5;  // hPa

// Ejemplos:
// Las Rozas (630m):    929.5 hPa
// Torrelodones (700m): 928.8 hPa
// Nivel del mar:       1013.25 hPa
```

---

## Lecciones Aprendidas

1. **Verificar la versión exacta del hardware** — Arduino Nano 33 BLE Sense Rev2 Lite no tiene HTS221. Comprobar siempre el datasheet del distribuidor.

2. **MBED ≠ AVR** — Las librerías para arquitectura AVR no funcionan en el nRF52840. Usar siempre librerías oficiales Arduino o verificar compatibilidad con MBED.

3. **SdFat obligatorio** — La librería SD estándar no es compatible con MBED. SdFat es el reemplazo correcto.

4. **El Arduino Nano 33 BLE necesita DOS drivers** — CH340 en Windows Y Arduino Mbed OS Nano Boards en el IDE. Sin ambos, no detecta puerto COM.

5. **El CO₂ a 1000m es siempre ~420 ppm** — No sirve para detectar combustión a esa altitud. El valor real del SCD40 es temperatura y humedad para validación cruzada.

6. **Doble almacenamiento es crítico** — SD + RAM backup protege contra fallos. La telemetría radio es el seguro si no se recupera el CanSat.

7. **Filtrar fases en telemetría** — Enviar solo datos de fases activas a Firebase evita saturación durante la espera previa al lanzamiento.

---

## Referencias

- Arduino Nano 33 BLE: https://docs.arduino.cc/hardware/nano-33-ble
- nRF52840 Datasheet: https://infocenter.nordicsemi.com/
- SdFat librería: https://github.com/greiman/SdFat
- AEMET Presión: https://www.aemet.es/
- APC220 rfmagic: Ver `IMPORTANTE_CAMBIO_FRECUENCIA.md`

---

**Última actualización:** Febrero 2026  
**Estado:** Sistema completo y funcional  
**Programa principal:** CANSAT_VUELO_INTEGRADO.ino
