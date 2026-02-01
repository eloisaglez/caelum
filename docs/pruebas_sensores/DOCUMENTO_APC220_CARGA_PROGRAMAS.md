# ⚠️ APC220 Y CARGA DE PROGRAMAS

## El Problema

**❌ NO SE PUEDE CARGAR PROGRAMA CON APC220 CONECTADO**

Si intentas cargar un programa Arduino con APC220 ya conectado a Serial1:
```
Error: "Upload failed"
Error: "Port not found"
Error: "timeout error"
```

---

## 🔴 ¿POR QUÉ OCURRE?

```
APC220 usa Serial1 (puerto serie físico)
Arduino IDE también intenta usar Serial1 para subir código
Conflicto: ambos quieren el mismo puerto
Resultado: ❌ FALLO DE CARGA
```

---

## ✅ SOLUCIÓN: ORDEN CORRECTO

### CARGA DE PROGRAMAS

**PASO 1: DESCONECTA APC220**
```
❌ Desconecta antena APC220 de Serial1
❌ Si está en Shield Grove, quítalo
```

**PASO 2: CARGA PROGRAMA**
```
✅ Conecta Arduino a USB
✅ Abre Arduino IDE
✅ Selecciona programa
✅ Ctrl+U para cargar
✅ Espera mensaje "Done uploading"
```

**PASO 3: RECONECTA APC220**
```
✅ Una vez cargado el programa
✅ Reconecta APC220 a Serial1
✅ Arduino ejecuta programa con APC220
```

---

## 📋 DIAGRAMA DE FLUJO

```
┌─────────────────────┐
│ ¿Necesitas subir?   │
│ programa nuevo?     │
└──────────┬──────────┘
           │
        ❌ SÍ
           │
    ┌──────▼──────┐
    │ DESCONECTA  │
    │ APC220      │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │ CARGA       │
    │ PROGRAMA    │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │ RECONECTA   │
    │ APC220      │
    └──────┬──────┘
           │
    ✅ LISTO
```

---

## 🚨 CASOS ESPECÍFICOS

### CASO 1: Cargar PROGRAMA_1 (solo sensores)

```
❌ APC220 está conectado a Serial1
→ DESCONECTA antes de cargar

✅ Arduino reconoce puerto COM
✅ Carga exitosa
✅ Sensores funcionan
✅ (APC220 sigue desconectado, normal)
```

### CASO 2: Cargar PROGRAMA_2 (SGP30)

```
❌ APC220 está conectado
→ DESCONECTA

✅ Carga programa
✅ Prueba SGP30
✅ Reconecta APC220 después
```

### CASO 3: Cargar PROGRAMA_FINAL (todos sensores + APC220)

```
❌ APC220 está conectado
→ DESCONECTA

✅ Carga programa final
✅ Reconecta APC220
✅ Programa ejecuta con APC220
✅ Telemetría funciona
```

---

## 🔌 CONEXIONES DURANTE CARGA

### ❌ NO HAGAS ESTO

```
Serial1 Grove:  APC220 CONECTADO
USB:            Arduino conectado a PC
Resultado:      ❌ CARGA FALLA
```

### ✅ HAZ ESTO

```
Serial1 Grove:  NADA (desconectado)
USB:            Arduino conectado a PC
Resultado:      ✅ CARGA EXITOSA
```

### ✅ DESPUÉS DE CARGAR

```
Serial1 Grove:  APC220 CONECTADO
USB:            Arduino en batería o USB
Resultado:      ✅ TODO FUNCIONA
```

---

## 📝 CHECKLIST CARGA CON APC220

```
ANTES DE CARGAR:
  ☑ APC220 DESCONECTADO de Serial1
  ☑ Arduino conectado a USB
  ☑ Puerto COM detectado
  ☑ Board: Arduino Nano 33 BLE

CARGANDO:
  ☑ Ctrl+U
  ☑ "Done uploading" aparece

DESPUÉS DE CARGAR:
  ☑ Desconecta USB (opcional)
  ☑ Reconecta APC220 a Serial1
  ☑ Arduino en batería
  ☑ Programa ejecuta
  ☑ APC220 transmite
```

---

## 💡 TRUCO: CARGA RÁPIDA

Si cargas muchos programas seguidos:

```
1. Desconecta APC220 de Serial1
2. Deja todo lo demás conectado
3. Carga PROGRAMA_1
4. Carga PROGRAMA_2
5. Carga PROGRAMA_3
6. ... etc
7. Cuando termines: Reconecta APC220
```

---

## 🚨 PROBLEMAS Y SOLUCIONES

### ❌ "Puerto COM no aparece"

```
Causa probable: APC220 conectado
Solución:
  1. Desconecta APC220
  2. Desconecta/reconecta USB Arduino
  3. Puerto COM debería aparecer
  4. Intenta cargar de nuevo
```

### ❌ "Timeout error during upload"

```
Causa probable: APC220 interfiere
Solución:
  1. ❌ Desconecta APC220
  2. ❌ Presiona RESET doble en Arduino
  3. ✅ Intenta cargar inmediatamente (< 2 seg)
```

### ❌ "Compilation error" al cargar con APC220

```
Causa probable: Serial1 bloqueada
Solución:
  1. Desconecta APC220
  2. Espera 5 segundos
  3. Reconecta USB Arduino
  4. Carga programa
```

---

## 🎯 RECOMENDACIÓN PARA BRUNETE

### EN CASA (desarrollo)

```
1. Cargas programas (APC220 desconectado)
2. Pruebas y debuggeo
3. Reconectas APC220
4. Pruebas finales
```

### EN BRUNETE (competencia)

```
1. Carga PROGRAMA_FINAL una única vez
2. No cambies de programa
3. Reconecta APC220
4. Verifica todo funciona
5. ¡A volar!
```

---

## 📊 RESUMEN RÁPIDO

| Acción | APC220 | Estado |
|--------|--------|--------|
| **Cargar programa** | ❌ Desconectado | ✅ Funciona |
| **Ejecutar programa** | ✅ Conectado | ✅ Funciona |
| **Debuggear** | ❌ Desconectado | ✅ Funciona |
| **Telemetría** | ✅ Conectado | ✅ Funciona |

---

## ⚡ PROCEDIMIENTO CORRECTO PASO A PASO

### Para cada programa nuevo:

```
1️⃣ PREPARACIÓN
   ├─ Arduino conectado a USB
   ├─ APC220 DESCONECTADO
   └─ Arduino IDE abierto

2️⃣ SELECCIONAR PROGRAMA
   ├─ Abre archivo .ino
   ├─ Verifica Board: Arduino Nano 33 BLE
   └─ Verifica Puerto: COM[X]

3️⃣ CARGAR
   ├─ Ctrl+U (o botón Upload)
   ├─ Espera "Done uploading"
   └─ Abre Monitor Serial si quieres

4️⃣ DESPUÉS
   ├─ Desconecta USB (opcional)
   ├─ Reconecta APC220 a Serial1
   ├─ Alimenta Arduino (USB o batería)
   └─ Programa ejecuta normalmente
```

---

## 🎓 EXPLICACIÓN TÉCNICA

```
Arduino Nano 33 BLE tiene:
  • Puerto USB (para carga de código)
  • Serial1 (para comunicaciones)

Problema:
  • Cuando subes código, Arduino IDE usa puerto USB
  • Arduino IDE temporalmente comunica con bootloader
  • Si Serial1 (APC220) está activo, crea conflicto
  
Solución:
  • Desconectar Serial1 durante carga
  • Dejar USB como único puerto activo
  • Después de cargar: reconectar Serial1
```

---

## ✅ ACTUALIZAR DOCUMENTACIÓN

Esta información debería estar en:

```
📄 DOCUMENTO_5_APC220_TELEMETRIA_ACTUALIZADO.md
   → Agregar sección "Carga de programas"
   
📄 TROUBLESHOOTING_COMPLETO.md
   → Agregar Problema: "Upload falla con APC220"
   
📄 INDICE_DE_PRUEBAS_FINAL.md
   → Mencionar: "Desconecta APC220 antes de cargar"
```

---

## 🎯 RECOMENDACIÓN FINAL

```
✅ REGLA SIMPLE:
   "APC220 DESCONECTADO para cargar"
   "APC220 CONECTADO para ejecutar"

✅ ESTO EVITA:
   • Errores de carga
   • Conflictos de puertos
   • Frustración en Brunete

✅ ES RÁPIDO:
   • 10 segundos desconectar/conectar
   • Vale la pena por seguridad
```

---

**¡Buena observación!** ✅

Esta es información **CRÍTICA** que debe estar clara en todos los documentos.

**¿Quieres que actualice los documentos para incluir esto?**
