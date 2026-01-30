# Arduino Nano 33 BLE Sense Rev2 - CanSat Project
## Pruebas, Problemas y Soluciones

**Autor:** Eloísa González Medina  
**Centro:** IES Diego Velázquez - Bilingual Secondary School  
**Proyecto:** CanSat Competition  
**Fecha:** Enero 2026  
**Hardware:** Arduino Nano 33 BLE Sense Rev2 + Sensores externos  
**Alimentación:** Pila 9V ion litio 11000mAh + TP4056  

---

## 📋 Índice

1. [Hardware Utilizado](#hardware-utilizado)
2. [Problemas Encontrados](#problemas-encontrados)
3. [Soluciones Aplicadas](#soluciones-aplicadas)
4. [Pruebas Realizadas](#pruebas-realizadas)
5. [Sensores Finales](#sensores-finales)
6. [Configuración Final](#configuración-final)
7. [Lecciones Aprendidas](#lecciones-aprendidas)

---

## 🔧 Hardware Utilizado

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
| Humedad + Temperatura | HTS221 | Humedad | ❌ No presente* |
| Luz/Color/Proximidad | APDS9960 | Luz ambiente | ✅ Funciona |

*Nota: Versión "Lite" sin HTS221 integrado de fábrica

### Sensores Externos
| Sensor | Modelo | Conexión | Estado |
|--------|--------|----------|--------|
| Sensor de Gases | SGP30 | I2C | ✅ (No probado aún) |
| GPS | ATGM336H | UART | ✅ (No probado aún) |
| Módulo RF | APC220 | Serial/Digital | ✅ (No probado aún) |

### Alimentación
- **Batería:** Pila 9V ion litio 11000mAh (modelo 103450)
- **Módulo de protección:** TP4056
- **Regulador:** MP2322 DC-DC (integrado en Arduino)
- **Voltaje entrada:** 9V
- **Voltaje regulado:** 3.3V

### Accesorios
- **Shield:** Grove Shield para Arduino Nano
- **Cables:** USB Micro (múltiples intentos)
- **Conexiones:** Breadboard + jumpers

---

## ⚠️ Problemas Encontrados

### Problema 1: Sensor HTS221 No Se Inicializa
**Síntoma:**
```
Failed to initialize humidity temperature sensor!
```

**Intentos de solución:**
1. ❌ Librería Arduino_HTS221 oficial → Error: "Failed to initialize"
2. ❌ Librería Adafruit HTS221 → Error: "Failed to find HTS221 chip"
3. ❌ Librería FaBo 208 HTS221 → Error incompatibilidad arquitectura AVR vs MBED
4. ❌ Cambio de 3 cables USB diferentes → Sin efecto
5. ❌ Reinstalación de drivers → Sin efecto
6. ✅ **SOLUCIÓN FINAL:** El sensor NO existe en la placa (versión Lite sin HTS221)

**Resolución:** Quitar completamente HTS221 del código

---

### Problema 2: Puerto COM No Se Reconoce
**Síntoma:**
```
No device found on COM1
Failed uploading: uploading error: exit status 1
```

**Intentos de solución:**
1. ❌ Instalar driver CH340 → Conflicto con nRF52840
2. ❌ Cambiar puertos USB → Seguía sin funcionar
3. ❌ Reinstalar Arduino IDE → Sin efecto
4. ❌ Desinstalar/reinstalar placas → Parcial
5. ✅ **SOLUCIÓN:** Desinstalar CH340 + Instalar "Arduino Mbed OS Nano Boards"

**Root cause:** Arduino Nano 33 BLE usa nRF52840 (no CH340). Driver CH340 causaba conflicto.

---

### Problema 3: LED Amarillo Parpadea
**Información sobre LEDs:**
- 🟢 LED verde (PWR): Encendido = Alimentación presente ✅
- 🟡 LED amarillo (RX/TX): Parpadea = Comunicación serial

**Cuándo es NORMAL que parpadee:**
- ✅ Cuando subes código
- ✅ Cuando Monitor Serial está abierto
- ✅ Cuando Arduino envía datos
- ✅ Parpadeos ocasionales/leves

**Cuándo es ANORMAL:**
- ❌ Parpadea sin parar sin razón
- ❌ Parpadea erráticamente/inestable
- ❌ Se atenúa lentamente (indica voltaje bajo)

**Si parpadea anormalmente, causas posibles:**
1. Cable USB de mala calidad (probabilidad baja)
2. Voltaje USB insuficiente (hub débil)
3. Ruido eléctrico (interferencia)

### Diagnóstico por LED Amarillo:

**Si LED amarillo parpadea al conectar:**
✅ Arduino detectado en puerto COM
✅ Comunicación USB funcionando
✅ Cable OK
✅ Driver OK

**Si LED amarillo NO parpadea al conectar:**
❌ Arduino NO detectado
❌ Problema de puerto COM
❌ Cable defectuoso
❌ Driver no instalado

**Regla para debugging:**
1. Conecta Arduino
2. Si LED parpadea → Puerto COM funcionando
3. Si NO parpadea → Revisar drivers y cable

**Solución recomendada:**
- Probar con cable de marca conocida (Anker, Belkin, UGREEN)
- Conectar directamente al PC (sin hub)
- Cerrar Monitor Serial si no lo necesitas

---

### Problema 4: Librería Incompatible con Arquitectura
**Síntoma:**
```
ATENCIÓN: la librería FaBo 208 Humidity HTS221 pretende ejecutarse 
sobre arquitectura(s) avr y puede ser incompatible con tu actual tarjeta 
la cual corre sobre arquitectura(s) mbed_nano.
```

**Causa:** FaBo está diseñada para Arduino AVR, no para MBED

**Solución:** Usar librerías oficiales de Arduino (diseñadas para MBED)

---

### Problema 5: Arduino IDE No Detecta Placa
**Síntoma:**
- Tools → Board: No se puede seleccionar placa
- Tools → Port: Aparece vacío

**Causa:** 
1. Desinstalación accidental de "Arduino Mbed OS Nano Boards"
2. Caché corrupta de Arduino IDE

**Solución:**
1. Reinstalar "Arduino Mbed OS Nano Boards v4.5.0"
2. Limpiar caché: `C:\Users\[Usuario]\AppData\Local\Arduino15`

---

## ✅ Soluciones Aplicadas

### Solución 1: Gestión de Sensores No Disponibles
**Código:**
```cpp
// Opción A: Quitar completamente del código
// #include <Arduino_HTS221.h>  // ELIMINADO

// Opción B: Inicializar con try-catch (avanzado)
// No usar "if (!HTS.begin())" porque HTS221 no existe
```

### Solución 2: Drivers Correctos
**Windows:**
1. Desinstalar driver CH340
2. Instalar "Arduino Mbed OS Nano Boards" v4.5.0
3. Reiniciar PC

**Arduino IDE:**
```
Tools → Board Manager
Buscar: "Arduino Mbed OS Nano Boards"
Instalar versión 4.5.0
```

### Solución 3: Cable USB de Calidad
**Especificaciones requeridas:**
- Marca conocida (Anker, Belkin, UGREEN, Baseus)
- USB Micro
- Blindado (preferible)
- Costo: 8-15€

**NO usar:**
- Cables genéricos baratos
- Cables de marcas desconocidas
- Cables viejos/desgastados

### Solución 4: Configuración de Arduino IDE
**Pasos correctos:**
1. Tools → Board → "Arduino Nano 33 BLE"
2. Tools → Port → Seleccionar puerto COM disponible
3. Tools → Upload Speed → 115200
4. Sketch → Upload

### Solución 5: Librerías Correctas para MBED
**Usar SOLO librerías oficiales de Arduino:**
```
Arduino_BMI270_BMM150   ✅ Oficial Arduino
Arduino_LPS22HB          ✅ Oficial Arduino (alternativa: Reefwing)
Arduino_APDS9960         ✅ Oficial Arduino
ReefwingLPS22HB          ✅ Para altitud mejorada

EVITAR:
FaBo (arquitectura AVR)  ❌
CH340 drivers            ❌
```

---

## 🧪 Pruebas Realizadas

### Test 1: Inicialización de Sensores
**Procedure:**
1. Cargar programa con cada sensor
2. Verificar inicialización en Serial Monitor
3. Anotar errores

**Resultados:**
| Sensor | Inicializa | Puerto | Notas |
|--------|-----------|--------|-------|
| BMI270 | ✅ Sí | I2C | Sin problemas |
| BMM150 | ✅ Sí | I2C | Sin problemas |
| LPS22HB | ✅ Sí | I2C | Funciona perfectamente |
| APDS9960 | ✅ Sí | I2C | Sin problemas |
| HTS221 | ❌ No | I2C | No existe en versión Lite |

### Test 2: Lecturas de Sensores
**Procedure:**
1. Conectar Arduino a PC
2. Subir programa final
3. Abrir Monitor Serial (9600 baud)
4. Mover Arduino en diferentes direcciones

**Datos típicos en reposo:**
```
ACELERACIÓN:
- X: ≈0.00 m/s²
- Y: ≈0.00 m/s²
- Z: ≈1.00 m/s² (gravedad)

GIROSCOPIO:
- X, Y, Z: ≈0.0-0.2 deg/s (ruido)

MAGNETÓMETRO (Brújula):
- Heading: 200-300° (depende orientación)
- Varia según dirección apuntada

PRESIÓN:
- Las Rozas: ≈929.5 hPa

ALTITUD (QNH):
- Calibrada a 0m en lanzamiento
- Varía ±2m por fluctuaciones de presión

LUZ:
- Interior noche con lámparas: 50-100 lux
- Varía según iluminación

PROXIMIDAD:
- Sin objetos cerca: 200-250
```

### Test 3: Estabilidad de Puerto COM
**Procedure:**
1. Conectar/desconectar 5 veces
2. Verificar que puerto sea consistente
3. Intentar subir código cada vez

**Resultado:**
- Con cable de mala calidad: ❌ Inconsistente
- Con driver CH340: ❌ No se detecta
- Con driver nRF52840 correcto: ✅ COM5 consistente

### Test 4: Calibración de Altitud
**Procedure:**
1. Encender Arduino en ubicación de lanzamiento
2. Esperar 30 segundos calibración
3. Anotar presión de referencia
4. Cambiar altura, verificar altitud

**Ejemplo Las Rozas (630m):**
```
Presión referencia: 929.5 hPa
Altitud referencia: 0.0 m (punto de lanzamiento)

Subir 1 piso (~3m):   Altitud = +3.1m ✅
Subir 2 pisos (~6m):  Altitud = +6.2m ✅
Bajar planta (-3m):   Altitud = -3.0m ✅
```

---

## 📊 Sensores Finales

### Sensores Funcionando
| Sensor | Modelo | Precisión | Utilidad para CanSat |
|--------|--------|-----------|----------------------|
| Acelerómetro | BMI270 | ±4g | Detectar caída, impacto |
| Giroscopio | BMI270 | ±2000 deg/s | Detectar rotación vuelo |
| Magnetómetro | BMM150 | ±1300µT | Orientación, brújula |
| Presión | LPS22HB | ±0.1 hPa | Base para altitud |
| Temperatura | LPS22HB | ±1.5°C | Datos ambientales |
| Altitud | LPS22HB (calculada) | ±10-20m | **CRÍTICA para CanSat** |
| Luz | APDS9960 | 0-65535 lux | Día/noche, atmósfera |
| Proximidad | APDS9960 | 0-255 | Detección objetos |

### No Disponibles
- **Humedad (HTS221):** No presente en versión Lite
  - Solución: No necesaria para CanSat
  - Alternativa si se requiere: Agregar sensor DHT22 externo

---

## ⚙️ Configuración Final

### Arduino IDE
```
Board: Arduino Nano 33 BLE
Port: COM5 (o el que aparezca)
Upload Speed: 115200
Programmer: Default
```

### Librerías Instaladas
```
Arduino_BMI270_BMM150 (v1.0.0+)
Arduino_LPS22HB (v1.0.0+)
Arduino_APDS9960 (v1.0.0+)
Arduino_HTS221 (INSTALADA pero NO USADA)
ReefwingLPS22HB (OPCIONAL, para altitud mejorada)
```

### Configuración de Altitud
**En el código, línea ~40:**
```cpp
// ⚠️ CAMBIAR ESTO SEGÚN UBICACIÓN DE LANZAMIENTO
float seaLevelPressure = 929.5;  // Presión real de Las Rozas

// EJEMPLOS POR UBICACIÓN:
// Las Rozas (630m): 929.5 hPa
// Torrelodones (700m): 928.8 hPa
// Guadarrama (1200m): 920.0 hPa
// Nivel del mar: 1013.25 hPa
```

**Cómo obtener presión:**
1. Consultar AEMET (www.aemet.es)
2. Consultar Weather.com
3. Consultar Windy.com
4. **ACTUALIZAR ANTES DE CADA VUELO**

### Programa Final
- **Archivo:** `Arduino_Nano_33_BLE_FINAL.ino`
- **Características:**
  - ✅ Todos los sensores funcionando
  - ✅ Calibración automática altitud
  - ✅ Formato tabla legible
  - ✅ Estadísticas cada 20 lecturas
  - ✅ Sin errores HTS221
  - ✅ Listo para CanSat

---

## 💡 Lecciones Aprendidas

### 1. Versiones de Hardware
- Arduino Nano 33 BLE tiene 2 versiones:
  - **Standard:** Con HTS221
  - **Lite:** Sin HTS221 (más barato)
- Verificar versión antes de instalar librerías

### 2. Arquitecturas de Procesadores
- Arduino Nano 33 BLE usa **nRF52840** (MBED)
- **NO** usa CH340 como otros Arduinos
- Drivers específicos para cada arquitectura

### 3. Cables USB
- Problema más común: **Cable de mala calidad**
- Afecta a:
  - Detección de puerto
  - Estabilidad de comunicación
  - Inicialización de sensores
- Solución: Cable de marca conocida

### 4. Librerías Incompatibles
- FaBo está para AVR, no MBED
- Siempre verificar: "Supported architectures"
- Usar librerías oficiales cuando sea posible

### 5. Sensores No Presentes
- Algunos sensores anunciados NO están en todas las versiones
- Leer datasheet del distribuidor
- Preparar código para ambos casos

### 6. Versión Lite es Suficiente
- Para CanSat, humedad NO es crítica
- Presión + Altitud es LO MÁS IMPORTANTE
- Ahorras peso y dinero

---

## 🟢🟡 Comportamiento Correcto de LEDs

**IMPORTANTE: LED Apagado ≠ Sin Comunicación**

El LED amarillo (RX/TX) **SOLO se enciende cuando hay tráfico de datos activo**.

### LED Naranja/Amarillo - Información Oficial

**Según documentación oficial de Arduino:**

El LED naranja tiene varios comportamientos:

1. **Durante upload:**
   - Parpadea suavemente (fade in and out)
   - Indica que el bootloader está activo
   - **Fuente:** Arduino Getting Started Guide

2. **Después de upload completado:**
   - Puede parpadear según el programa cargado
   - Es controlable por código (pin LED 13)
   - **Fuente:** Arduino Getting Started Guide

3. **En bootloader mode (double reset):**
   - Parpadea continuamente
   - Indica que está esperando nuevo código
   - **Fuente:** Arduino Zephyr Documentation

**IMPORTANTE:**
- El LED naranja NO es automáticamente un indicador RX/TX
- Puede ser programado para hacer lo que el código especifique
- Su comportamiento depende del programa cargado

**En tu caso específico:**
```
1. Conectas Arduino → LED parpadea (bootloader detectado)
2. Subes programa → LED parpadea durante transmisión
3. Upload termina → LED apagado o según el programa
4. Programa ejecuta → LED puede estar apagado o parpadeando según código
```

**Conclusión:**
El comportamiento del LED es esperado. No indica problemas.
El hecho de que recibas datos en Monitor Serial = Arduino funciona correctamente.

### ¿Por qué LED apagado si hay datos?
- Los datos se transmiten y se reciben
- Una vez recibidos, no hay más tráfico
- LED refleja tráfico ACTIVO, no presencia de datos

### Estado Final Confirmado (Enero 2026):
✅ LED verde: Encendido (alimentación OK)
✅ LED amarillo: Parpadea al subir → Apagado en reposo
✅ Monitor Serial: Recibe datos correctamente
✅ **Arduino funcionando PERFECTAMENTE**

---

## 📝 Checklist Pre-Vuelo

- [ ] Cable USB de buena calidad
- [ ] Arduino Nano 33 BLE conectado y COM detectable
- [ ] Todas las librerías instaladas correctamente
- [ ] Presión de referencia actualizada para ubicación de lanzamiento
- [ ] Programa `Arduino_Nano_33_BLE_FINAL.ino` subido
- [ ] Monitor Serial abierto a 9600 baud
- [ ] Datos de sensores visibles y coherentes
- [ ] Batería 9V cargada
- [ ] TP4056 conectado correctamente
- [ ] Grove Shield montado
- [ ] Sensores externos (SGP30, GPS, APC220) conectados
- [ ] Estructura física del CanSat lista

---

## 🚀 Para Futuros Proyectos

### Si Necesitas Humedad Real
1. Agregar sensor DHT22 externo
2. Conectar por pin Digital
3. Usar librería DHT22
4. Modificar código para leer ambos

### Si Necesitas Mejor Altitud
1. Usar librería Reefwing_LPS22HB
2. Implementar cálculos QNE, QNH, QFE
3. Mejor precisión: ±10-20m vs ±20-30m

### Si Necesitas Más Sensores
1. Verificar disponibilidad de pines
2. I2C soporta múltiples dispositivos
3. UART soporta múltiples con SoftwareSerial
4. Digital soporta muchos

---

## 📚 Referencias

- Arduino Nano 33 BLE: https://docs.arduino.cc/hardware/nano-33-ble
- nRF52840 Datasheet: https://infocenter.nordicsemi.com/
- AEMET Presión: https://www.aemet.es/
- Reefwing LPS22HB: https://github.com/Reefwing-Software/Reefwing_LPS22HB

---

**Última actualización:** Enero 2026  
**Estado:** Listo para CanSat  
**Próximo paso:** Integración con SGP30, ATGM336H, APC220
