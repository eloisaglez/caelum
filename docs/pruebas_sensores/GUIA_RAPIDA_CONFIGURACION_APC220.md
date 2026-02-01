# 🔧 GUÍA RÁPIDA - CONFIGURACIÓN APC220

## Objetivo
Configurar **DOS módulos APC220** para que funcionen juntos (emisor + receptor).

---

## ⚠️ CRÍTICO: AMBOS DEBEN TENER LA MISMA CONFIGURACIÓN

```
Si no coinciden las ondas:
  ❌ NO se comunican
  ❌ Wasted time debugging

Si coinciden:
  ✅ Comunican perfectamente
  ✅ Listos para CanSat
```

---

## 🎯 CONFIGURACIÓN OBJETIVO (AMBOS)

```
Frecuencia:     434 MHz (434000 KHz)
Velocidad RF:   9600 bps
Potencia:       9 (máxima)
Puerto serie:   9600 bps
Paridad:        0 (sin paridad)

Comando: WR 434000 3 9 3 0
```

---

## 🔨 MÉTODO 1: Con rfmagic (Recomendado si tienes Windows)

### Paso 1: Instalar Drivers

```
1. Descarga: www.micro-log.com/apc/cp210x.zip
2. Descomprime
3. Ejecuta instalador
4. Reinicia PC
```

### Paso 2: Descargar Software

```
1. Descarga: www.micro-log.com/apc/rfmagic.rar
2. Descomprime carpeta
3. Guarda en Desktop
```

### Paso 3: Configurar PRIMER APC220

```
1. Conecta APC220 a módulo USB-UART
2. Conecta USB-UART a PC
3. Abre Device Manager:
   • Busca "Silicon Labs CP210x"
   • Anota puerto (ej: COM3)
   • Si COM > 5: cambiar a COM1-5

4. Ejecuta rfmagic.exe COMO ADMINISTRADOR

5. Configura parámetros:
   • RF frequency: 434
   • RF TRx rate: 9600bps
   • RF Power: 9
   • Series rate: 9600 bps
   • PC Series: [debe aparecer puerto COM]

6. Click "Write w"
   → "write succeed!!" ✓

7. Click "Read R"
   → "Read succeed!!" ✓

8. Desconecta
```

### Paso 4: Configurar SEGUNDO APC220

```
REPITE PASOS 1-8 CON OTRO APC220

⚠️ VERIFICAR QUE AMBOS MUESTREN LOS MISMOS PARÁMETROS
```

---

## 🔨 MÉTODO 2: Con Arduino (Si rfmagic no funciona)

### Hardware Necesario

```
• Arduino UNO (no Nano 33 BLE)
• Módulo APC220
• Cable USB
```

### Conexión Arduino UNO ← → APC220

```
GND  → GND
D13  → VCC
D12  → EN
D11  → RXD
D10  → TXD
D9   → AUX
D8   → SET
```

### Pasos

```
1. Conecta Arduino UNO a PC (USB)

2. Copia código: PROGRAMA_CONFIGURACION_APC220.ino

3. Carga en Arduino IDE:
   • Selecciona: Board = Arduino UNO
   • Selecciona: Port = COM[X]
   • Ctrl+U para cargar

4. Abre Monitor Serial (9600 baud)

5. Deberías ver:
   ✓ "Configuración escrita"
   ✓ "Config actual: PARAM 434000 3 9 3 0"
   ✓ "✅ CONFIGURACIÓN COMPLETADA"

6. Si todo OK:
   • Desconecta Arduino
   • Desconecta APC220
   
7. REPITE CON SEGUNDO APC220
```

---

## ✅ VERIFICACIÓN FINAL

Después de configurar AMBOS APC220:

### Método 1 (rfmagic)
```
Abre rfmagic con PRIMER APC220:
  Click "Read R" → "Read succeed!!" ✓
  Deberías ver: PARAM 434000 3 9 3 0

Conecta SEGUNDO APC220:
  Click "Read R" → "Read succeed!!" ✓
  Deberías ver: PARAM 434000 3 9 3 0

⚠️ SI ALGUNO MUESTRA DIFERENTE → Reconfigurar
```

### Método 2 (Arduino)
```
Abre Monitor Serial con PRIMER APC220:
  "Config actual: PARAM 434000 3 9 3 0" ✓

Desconecta, conecta SEGUNDO APC220:
  "Config actual: PARAM 434000 3 9 3 0" ✓

⚠️ SI ALGUNO MUESTRA DIFERENTE → Reconfigurar
```

---

## 🧪 PRUEBA DE COMUNICACIÓN

Una vez ambos configurados:

### Configuración

```
Emisor APC220: Conectado a Arduino CanSat + PROGRAMA_5
Receptor APC220: Conectado a segundo Arduino

Carga programa EMISOR:

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
}

void loop() {
  Serial1.println("HOLA");
  delay(2000);
}
```

Carga programa RECEPTOR:

```
void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
}

void loop() {
  if (Serial1.available()) {
    char c = Serial1.read();
    Serial.print(c);
  }
}
```

### Verificación

```
Monitor Serial RECEPTOR deberías ver:
  H
  O
  L
  A
  
Si ves esto → ✅ TODO FUNCIONA
Si no ves → Verificar configuración
```

---

## 🚨 PROBLEMAS COMUNES

### ❌ "rfmagic no reconoce APC220"

```
Solución:
  1. ¿Instalaste drivers?
     → Descargar www.micro-log.com/apc/cp210x.zip
  
  2. ¿Puerto COM correcto?
     → Device Manager: busca "Silicon Labs"
     → Si COM > 5: cambiar a COM1-5
  
  3. ¿Ejecutas rfmagic como admin?
     → Click derecho → "Run as administrator"
```

### ❌ "write succeed!! pero no lee"

```
Solución:
  1. Desconecta APC220
  2. Reconecta
  3. Vuelve a intentar "Read R"
  
  Si persiste → APC220 defectuoso
```

### ❌ "Arduino method: No se leyó configuración"

```
Solución:
  1. ¿Pines D8-D13 conectados?
     → Verificar conexiones
  
  2. ¿D13 a VCC?
     → Alimentación APC220
  
  3. ¿Monitor Serial abierto a 9600?
     → Cambiar velocidad si falla
```

### ❌ "No comunican los dos APC220"

```
Solución:
  1. ¿Misma configuración?
     → Verificar PARAM en ambos
     → Deben ser IGUALES
  
  2. ¿Antenas conectadas?
     → Verificar en ambos módulos
  
  3. ¿Distancia?
     → Probar a 10 metros
     → Sin obstáculos entre ellos
```

---

## 📋 CHECKLIST CONFIGURACIÓN

```
PRIMER APC220:
  ☐ Drivers instalados
  ☐ Conectado a PC/Arduino
  ☐ Parámetros configurados: WR 434000 3 9 3 0
  ☐ "write succeed!!" confirmado
  ☐ "Read succeed!!" confirmado
  ☐ Verificar: PARAM 434000 3 9 3 0

SEGUNDO APC220:
  ☐ Drivers instalados
  ☐ Conectado a PC/Arduino
  ☐ Parámetros configurados: WR 434000 3 9 3 0
  ☐ "write succeed!!" confirmado
  ☐ "Read succeed!!" confirmado
  ☐ Verificar: PARAM 434000 3 9 3 0

VERIFICACIÓN FINAL:
  ☐ Ambos muestran: PARAM 434000 3 9 3 0
  ☐ AMBOS tienen los MISMOS parámetros
  ☐ Antenas conectadas en ambos
  ☐ Listo para cargar PROGRAMA_5
```

---

## 🎯 DESPUÉS DE CONFIGURAR

```
1. Ambos APC220 guardados con configuración
2. ✅ Listos para CanSat
3. Carga PROGRAMA_5_APC220_TELEMETRIA.ino
4. Prueba de comunicación
5. Carga PROGRAMA_FINAL
6. ¡¡A BRUNETE!!
```

---

## 📞 RESUMEN RÁPIDO

| Paso | Método 1 (rfmagic) | Método 2 (Arduino) |
|------|---|---|
| Instalar | Drivers CP210x | Arduino IDE |
| Software | rfmagic.rar | PROGRAMA_CONFIGURACION_APC220.ino |
| Tiempo | ~30 min | ~20 min |
| Requiere | Windows + PC | Arduino UNO + USB |
| Verificación | "Read succeed!!" | Monitor Serial |
| Dificultad | ⭐⭐ | ⭐⭐⭐ |

---

**Ambos métodos son válidos. Elige según qué tengas disponible.** 🎯

**¡Buena configuración!** ✅
