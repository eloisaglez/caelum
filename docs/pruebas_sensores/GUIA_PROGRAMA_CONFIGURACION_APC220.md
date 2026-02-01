# 🔧 GUÍA: Programa de Configuración APC220

## Archivo
**`PROGRAMA_CONFIGURACION_APC220.ino`**

---

## 📋 Objetivo

Configurar módulo APC220 **directamente desde Arduino Nano 33 BLE**, sin necesidad de:
- ❌ rfmagic
- ❌ PC adicional
- ❌ Drivers especiales

---

## 🔌 Conexión Física

```
Arduino Nano 33 BLE ← → APC220

D10 (RXD) ← APC220 TX (RXD)
D11 (TXD) → APC220 RX (TXD)
D8 (SET)  → APC220 SET
D9 (EN)   → APC220 EN
D12 (AUX) ← APC220 AUX
3.3V      → APC220 VCC
GND       → APC220 GND
```

---

## 📥 Cómo Usar

### Paso 1: Conectar Hardware

```
1. APC220 conectado a Arduino según esquema arriba
2. Arduino conectado a PC por USB
```

### Paso 2: Cargar Programa

```
1. Abre Arduino IDE
2. Copia código: PROGRAMA_CONFIGURACION_APC220.ino
3. Tools → Board: Arduino Nano 33 BLE
4. Tools → Port: COM[X]
5. Ctrl+U (cargar)
```

### Paso 3: Abrir Monitor Serial

```
1. Tools → Serial Monitor
2. Velocidad: 9600 baud
3. Espera mensaje de bienvenida
```

### Paso 4: Configurar

```
Monitor Serial muestra:

╔════════════════════════════════════════╗
║  Configuración APC220                 ║
║  Arduino Nano 33 BLE Sense            ║
╚════════════════════════════════════════╝

Presiona una tecla para comenzar configuración:
  1 = Leer configuración actual
  2 = Escribir nueva configuración (434MHz, 9600bps, Pot max)
  3 = Ambas (leer, escribir, leer)

Opciones:
  Escribe 1, 2 o 3 en la caja de texto
  Presiona ENTER
```

---

## 🎯 Opción 1: Solo Leer

```
Escribe: 1
Presiona: ENTER

Resultado:
  ▲ LEYENDO CONFIGURACIÓN:
  Respuesta: PARAM 434000 3 9 3 0
  ✓ Respuesta recibida correctamente
```

**Qué significa:**
- `PARAM` = parámetros del APC220
- `434000` = 434 MHz
- `3` = 9600 bps RF
- `9` = Potencia máxima
- `3` = 9600 bps puerto serie
- `0` = Sin paridad

---

## 🎯 Opción 2: Solo Escribir

```
Escribe: 2
Presiona: ENTER

Resultado:
  ▼ ESCRIBIENDO CONFIGURACIÓN:
  Enviando: WR 434000 3 9 3 0
  ✓ Configuración enviada
  
  Parámetros escritos:
    • Frecuencia: 434 MHz
    • Velocidad RF: 9600 bps
    • Potencia: 9 (máxima)
    • Puerto serie: 9600 bps
    • Paridad: sin
```

---

## 🎯 Opción 3: Leer + Escribir + Leer (RECOMENDADO)

```
Escribe: 3
Presiona: ENTER

Resultado:
  1. Lectura INICIAL:
     ▲ LEYENDO CONFIGURACIÓN:
     PARAM 415370 2 9 3 0  (configuración anterior)
  
  2. Escritura:
     ▼ ESCRIBIENDO CONFIGURACIÓN:
     WR 434000 3 9 3 0
     ✓ Configuración enviada
  
  3. Lectura FINAL (verificación):
     ▲ LEYENDO CONFIGURACIÓN:
     PARAM 434000 3 9 3 0  (nuevos parámetros)
     ✓ Respuesta recibida correctamente
```

**Esto verifica que:**
- ✅ APC220 leía configuración anterior
- ✅ Se escribió la nueva configuración
- ✅ Se guardó correctamente

---

## ✅ Verificación de Éxito

Después de opción 3, deberías ver:

```
✓ Respuesta recibida correctamente

Parámetros leídos:
  • Frecuencia: 434000 KHz
```

**Si ves esto:** ✅ **CONFIGURACIÓN EXITOSA**

---

## 🚨 Problemas

### ❌ "NO RECIBIDA respuesta"

```
Significa: Arduino no recibe datos del APC220

VERIFICA:
  1. ¿Pines conectados?
     • D10 (RXD) ← TX del APC220
     • D11 (TXD) → RX del APC220
     • D8 (SET) → SET del APC220
     • D9 (EN) → EN del APC220
     • GND ↔ GND

  2. ¿APC220 tiene alimentación?
     • 3.3V conectado
     • LED encendido

  3. ¿Antena conectada?
     • Verificar conector en APC220

  4. ¿Board correcto?
     • Verificar: Tools → Board → Arduino Nano 33 BLE
```

### ❌ "Respuesta incompleta o confusa"

```
Significa: Se recibe algo pero no válido

Posibles causas:
  1. Velocidad incorrecta
     → Probar cambiar Serial.begin(9600) a otra velocidad
  
  2. Pines incorrectos
     → Verificar conexión D10/D11
  
  3. Cabbage (datos basura)
     → Normal en primeras pruebas
     → Reiniciar Arduino
```

---

## 📋 Configuración Final

Después de configurar, **anota estos valores:**

```
PRIMER APC220 (Emisor - CanSat):
  ✓ PARAM 434000 3 9 3 0

SEGUNDO APC220 (Receptor - Tierra):
  ✓ PARAM 434000 3 9 3 0

⚠️ DEBEN SER EXACTAMENTE IGUALES
```

---

## 🎯 Próximos Pasos

1. **Configurar segundo APC220:**
   - Desconecta primer APC220
   - Conecta segundo APC220
   - REPITE pasos 1-4 con opción 3

2. **Verificar sincronización:**
   - Ambos deben tener: `PARAM 434000 3 9 3 0`
   - Si no coinciden → Reconfigurar

3. **Cargar PROGRAMA_5:**
   - Desconecta Arduino de programa configuración
   - Conecta APC220 a Serial1 (Grove)
   - Carga `PROGRAMA_5_APC220_TELEMETRIA.ino`
   - Prueba comunicación

4. **Cargar PROGRAMA_FINAL:**
   - Todos los sensores + APC220
   - Listo para BRUNETE

---

## 📊 Tabla de Parámetros

| Parámetro | Valor | Significado |
|-----------|-------|---|
| A (Frecuencia) | 434000 | 434 MHz |
| B (Velocidad RF) | 3 | 9600 bps |
| C (Potencia) | 9 | Máxima |
| D (Puerto serie) | 3 | 9600 bps |
| E (Paridad) | 0 | Sin paridad |

**Resultado:** `WR 434000 3 9 3 0`

---

## 🔄 Ciclo Completo

```
PRIMER APC220:
  1. Conecta a Arduino
  2. Carga PROGRAMA_CONFIGURACION_APC220.ino
  3. Opción 3 (leer + escribir + leer)
  4. Verifica: PARAM 434000 3 9 3 0 ✓

SEGUNDO APC220:
  1. Desconecta primer APC220
  2. Conecta segundo APC220
  3. REPITE pasos 2-4

VERIFICACIÓN:
  Ambos muestran: PARAM 434000 3 9 3 0 ✓

LISTO:
  → Cargar PROGRAMA_5_APC220_TELEMETRIA.ino
  → Todos los sensores funcionan
  → ¡¡A BRUNETE!!
```

---

## 💡 Notas

```
✅ Este programa usa SoftwareSerial (D10/D11)
   Después puedes usar Serial1 para telemetría

✅ Puedes ejecutar el programa varias veces
   No daña el APC220

✅ Ambos APC220 deben estar configurados
   Si uno falla → No comunican

✅ Guarda foto de pantalla con PARAM final
   Para referencia futura
```

---

**¡Buena configuración!** ✅
