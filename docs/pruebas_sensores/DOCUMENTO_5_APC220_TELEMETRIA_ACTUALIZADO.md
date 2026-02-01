# 📋 DOCUMENTO 5: APC220 - TELEMETRÍA RF

## Objetivo
Integrar antena RF APC220 para transmisión de datos en tiempo real durante el vuelo.

---

## 📡 APC220 - Especificaciones

```
Protocolo: UART RF (Radio Frecuencia)
Frecuencia: 434 MHz
Rango: 300-1000 metros (línea vista)
Velocidad: Configurable (9600 baud recomendado)
Voltaje: 3.3-5V
Potencia: Configurable (0-9, recomendado 9=máximo)
```

---

## 🔌 Conexión Física

### Arduino Nano 33 BLE ← → APC220

```
Arduino Nano 33 BLE (Serial1 Grove):
  RX (Grove) ← APC220 TX
  TX (Grove) → APC220 RX
  3.3V-5V    → APC220 VCC
  GND        → GND
  
  Antena → Conectada a APC220
```

---

## ⚙️ CONFIGURACIÓN CRÍTICA DEL APC220

### ⚠️ IMPORTANTE: DOS APC220 DEBEN ESTAR EN LA MISMA ONDA

```
Emisor (CanSat):
  Frecuencia: 434 MHz
  Velocidad RF: 9600 bps
  Potencia: 9 (máximo)
  Puerto serie: 9600 bps
  
Receptor (Tierra):
  MISMOS PARÁMETROS que emisor
  
Si no coinciden → NO se comunican
```

---

## 📥 INSTALACIÓN DE DRIVERS

### Windows

**Paso 1: Descargar e instalar drivers**

```
1. Descarga: www.micro-log.com/apc/cp210x.zip
2. Descomprime
3. Ejecuta como administrador
4. Instala driver
5. Reinicia PC
```

**Verificar:**
```
Device Manager → Ports (COM & LPT)
Deberías ver: "Silicon Labs CP210x USB to UART Bridge Controller"
Anota el puerto (ej: COM3)
```

### Linux / Mac

```
El driver suele estar incluido en el SO
Verifica con: ls /dev/tty*
```

---

## 🔧 CONFIGURACIÓN DEL APC220

### Software Necesario

```
Descarga: www.micro-log.com/apc/rfmagic.rar
Descomprime la carpeta
```

### Pasos de Configuración (CRÍTICO)

**Para CADA APC220 (emisor y receptor):**

```
1. Descarga e instala drivers (paso anterior)

2. Conecta APC220 a módulo USB-UART

3. Conecta módulo USB-UART a PC

4. Abre Device Manager:
   - Busca el puerto COM
   - Si es superior a COM5:
     * Clic derecho en dispositivo
     * Properties
     * Port Settings
     * Cambia a COM1-COM5

5. Ejecuta rfmagic.exe COMO ADMINISTRADOR

6. Introduce parámetros:
   ✓ RF frequency: 434
   ✓ RF TRx rate: 9600bps (opción 3)
   ✓ RF Power: 9 (MAX)
   ✓ Series rate: 9600 bps (opción 3)

7. Verifica que aparezca puerto COM en "PC Series"

8. Click "Write w"
   → Debe mostrar: "write succeed!!"

9. Click "Read R"
   → Debe mostrar: "Read succeed!!"

10. Desconecta

11. REPITE LOS PASOS 2-10 CON EL SEGUNDO APC220
```

**⚠️ AMBOS DEBEN TENER LOS MISMOS PARÁMETROS**

---

## 📊 Parámetros de Configuración

### Frecuencia (AAAAAA)
```
Rango: 418-455 MHz
Recomendado: 434 MHz (banda ISM)
Formato: en KHz (434000 = 434 MHz)
```

### Velocidad RF (B)
```
1 = 2400 bps
2 = 4800 bps
3 = 9600 bps  ← RECOMENDADO
4 = 19200 bps
```

### Potencia (C)
```
Rango: 0-9
0 = Mínima
9 = Máxima ← RECOMENDADO
```

### Velocidad Puerto Serie (D)
```
0 = 1200 bps
1 = 2400 bps
2 = 4800 bps
3 = 9600 bps  ← RECOMENDADO
4 = 19200 bps
5 = 38400 bps
6 = 57600 bps
```

### Paridad (E)
```
0 = Sin paridad ← RECOMENDADO
1 = Paridad par
2 = Paridad impar
```

---

## 💻 PROGRAMA A CARGAR

**Archivo:** `PROGRAMA_5_APC220_TELEMETRIA.ino`

**Ubicación:** `arduino/PROGRAMA_5_APC220_TELEMETRIA.ino`

### Código Básico (Emisor CanSat)

```cpp
void setup() {
  Serial.begin(9600);      // Debug USB
  Serial1.begin(9600);     // APC220 (Grove)
  delay(2000);
  
  Serial.println("APC220 Inicializado");
}

void loop() {
  // Enviar datos por APC220
  Serial1.print("HOLA #");
  Serial1.println(contador);
  
  // Debug
  Serial.print("Enviado: HOLA #");
  Serial.println(contador);
  
  contador++;
  delay(2000);
}
```

---

## ✅ VERIFICACIÓN - PRUEBA DE COMUNICACIÓN

### Prueba 1: Verificar que transmite

```
1. Carga PROGRAMA_5 en Arduino CanSat
2. Abre Monitor Serial (9600 baud)
3. Deberías ver:
   "Enviado: HOLA #0"
   "Enviado: HOLA #1"
   "Enviado: HOLA #2"
```

### Prueba 2: Verificar recepción (CON SEGUNDO ARDUINO)

```
1. Conecta segundo Arduino + APC220 receptor
2. Carga programa receptor:

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
}

void loop() {
  if (Serial1.available() > 0) {
    char dato = Serial1.read();
    Serial.print(dato);
  }
}

3. Abre Monitor Serial en receptor
4. Deberías recibir caracteres:
   "H O L A # 0"
   "H O L A # 1"
```

---

## 📡 PRUEBA DE ALCANCE

```
Procedimiento:
1. Emisor: Arduino + APC220 con PROGRAMA_5
2. Receptor: Segundo Arduino + APC220
3. Distancia inicial: 10 metros (línea vista)
4. Aleja paulatinamente
5. Anota última distancia con recepción

Resultado Esperado:
  • 100m línea vista:  ✅ Perfectamente
  • 300m línea vista:  ✅ Bueno
  • 500m línea vista:  ⚠️ Débil
  • >1000m:           ❌ Falla

Factores que afectan:
  • Obstáculos (edificios, árboles)
  • Interferencia RF (Wi-Fi, microondas)
  • Posición antenas
  • Humedad ambiente
```

---

## 🚨 TROUBLESHOOTING

### Problema: "No se comunican dos APC220"

```
Causas:
  1. ❌ Parámetros diferentes
     Solución: Verificar que ambos tengan IGUALES

  2. ❌ Driver no instalado
     Solución: Descargar e instalar cp210x.zip

  3. ❌ Puertos COM > 5
     Solución: Cambiar a COM1-COM5

  4. ❌ APC220 defectuoso
     Solución: Probar con otro APC220

Verificación:
  • Usa rfmagic en AMBOS
  • Click "Read R" → debe mostrar "Read succeed!!"
  • Si falla → APC defectuoso
```

### Problema: "Recibo basura en lugar de datos"

```
Causas:
  1. ❌ Velocidad diferente
     Solución: Verificar 9600 bps en AMBOS

  2. ❌ Paridad no sincronizada
     Solución: Poner ambos en paridad 0 (sin paridad)

  3. ❌ Interferencia RF
     Solución: Alejar de Wi-Fi, microondas, teléfonos
```

### Problema: "Alcance muy corto (<50m)"

```
Causas:
  1. ❌ Potencia baja
     Solución: Poner en 9 (máximo)

  2. ❌ Antenas deficientes
     Solución: Verificar que antenas estén bien conectadas

  3. ❌ Interferencia
     Solución: Cambiar localización (mejor en campo abierto)

  4. ❌ Obstáculos
     Solución: Necesita línea vista entre antenas
```

---

## 📝 CONFIGURACIÓN RECOMENDADA FINAL

```
Para tu CanSat Misión 2:

EMISOR (CanSat en el aire):
  WR 434000 3 9 3 0
  • Frecuencia: 434000 KHz (434 MHz)
  • Velocidad RF: 9600 bps
  • Potencia: 9 (máximo)
  • Puerto serie: 9600 bps
  • Paridad: 0 (sin)

RECEPTOR (En tierra):
  WR 434000 3 9 3 0
  • EXACTAMENTE IGUAL que emisor
```

---

## 📋 CHECKLIST PRE-VUELO APC220

```
☐ APC220 emisor configurado con rfmagic
☐ APC220 receptor configurado con rfmagic
☐ AMBOS tienen los MISMOS parámetros
☐ rfmagic muestra "Read succeed!!" en ambos
☐ Driver CP210x instalado
☐ Antenas conectadas en ambos APC220
☐ PROGRAMA_5 cargado en Arduino CanSat
☐ Receptor cargado con programa receptor
☐ Comunicación verificada a 10m
☐ Alcance verificado (100m+ en línea vista)
☐ Batería cargada en CanSat
☐ Batería cargada en receptor portátil
```

---

## 🎯 PRÓXIMO PASO

Una vez que APC220 funciona correctamente:
- ✅ Cargar **PROGRAMA_FINAL_CANSAT_MISION2.ino**
- ✅ TODOS los sensores + APC220 funcionan juntos
- ✅ Listo para **BRUNETE 2026**

---

## 📞 AYUDA RÁPIDA

```
¿No funciona?

1. ¿Instalaste drivers? 
   → Descarga www.micro-log.com/apc/cp210x.zip

2. ¿Ambos APC220 configurados en rfmagic?
   → Parámetros deben ser IGUALES

3. ¿"Read succeed!!" en rfmagic?
   → Si NO → APC220 defectuoso

4. ¿Comunicación en 10m?
   → Si NO → Verificar conexiones TX/RX
   
5. ¿Basura en lugar de datos?
   → Cambiar velocidad a 9600 bps exactamente
```

---

**Estado:** ✅ Documento APC220 actualizado con configuración  
**Última actualización:** Enero 2026
