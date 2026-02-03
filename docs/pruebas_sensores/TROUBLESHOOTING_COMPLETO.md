# TROUBLESHOOTING COMPLETO
## Problemas y Soluciones - Arduino Nano 33 BLE + CanSat

**Fecha:** Febrero 2026  
**Proyecto:** CanSat Misión 2  

---

## ÍNDICE RÁPIDO

```
PROBLEMAS ARDUINO:
  1. Puerto COM no aparece
  2. "Board not recognized"
  3. Upload falla
  4. Monitor Serial no funciona
  5. Arduino no se reconecta

PROBLEMAS LIBRERÍAS:
  6. Error de compilación
  7. Librería no encontrada
  8. Conflicto de versiones

PROBLEMAS SENSORES:
  9. Sensor no inicializa
  10. Valores raros/NaN
  11. No hay datos

PROBLEMAS ESPECÍFICOS:
  12. SGP30 no responde
  13. GPS sin señal
  14. MicroSD no graba
  15. APC220 no comunica
```

---

## PROBLEMA 1: PUERTO COM NO APARECE

### Síntomas
```
Arduino IDE:
  • Tools → Port: Vacío (sin puertos)
  • O solo aparece "COM1"
  • Arduino conectado pero no detectado
```

### Soluciones

#### Solución 1A: Instalar Drivers (CRÍTICO)

**Windows - Arduino Nano 33 BLE necesita driver nRF52840:**

```
1. Descarga Arduino IDE completo desde:
   https://www.arduino.cc/en/software

2. Durante instalación:
   Instala: "Arduino SAMD (32-bits ARM Cortex-M0+)"
   Instala: "Arduino mbed OS Nano Boards"
   
3. Reinicia Arduino IDE

4. Tools → Board Manager:
   Busca: "Arduino mbed OS Nano Boards"
   Instala versión 4.5.0 o superior
   
5. Espera a que descargue (~500MB)
```

#### Solución 1B: Cambiar Puerto USB

```
1. Desconecta Arduino
2. Prueba OTRO puerto USB:
   • Trasero del PC (mejor calidad)
   • Diferente puerto delantero
3. Reconecta Arduino
4. Verifica en Device Manager
```

#### Solución 1C: Verificar en Device Manager

```
Windows:
1. Presiona: Windows + X
2. Selecciona: Device Manager
3. Busca bajo "Ports (COM & LPT)":
   - "Arduino Nano 33 BLE"
   - "USB Serial Device"

4. Si ves dispositivo con ?:
   → Driver no instalado
```

### Verificación de Éxito
```
Tools → Port aparece: COM3, COM4, COM5, etc.
No aparece interrogación en Device Manager
Arduino IDE reconoce placa
```

---

## PROBLEMA 2: "BOARD NOT RECOGNIZED"

### Síntomas
```
Arduino IDE muestra:
  "An error occurred while uploading the sketch"
  "uploading error: exit status 1"
  "board not recognized"
```

### Soluciones

#### Solución 2A: Verificar Board Correcto

```
Arduino IDE:
1. Tools → Board
2. Busca: "Arduino Nano 33 BLE"
3. Click para seleccionar

COMÚN: Seleccionar "Arduino Nano" normal
Debe ser: "Arduino Nano 33 BLE"
```

#### Solución 2B: Resetear Bootloader

```
Procedimiento especial para Arduino Nano 33 BLE:

1. Desconecta Arduino
2. Espera 5 segundos
3. Reconecta Arduino

Si no funciona:

4. Presiona RESET en Arduino (botón pequeño)
5. RÁPIDAMENTE haz doble click
   (dentro de 1-2 segundos)
6. Arduino entra en bootloader
   (LED amarillo parpadea diferente)
7. Carga programa INMEDIATAMENTE (Ctrl+U)
```

---

## PROBLEMA 3: UPLOAD FALLA

### Síntomas
```
"uploading error"
"timeout error"
"ERROR: FAIL"
```

### Soluciones

#### Solución 3A: RESET Doble (Más efectivo)

```
1. Arduino conectado
2. Presiona RESET UNA VEZ
3. ESPERA 1 segundo
4. Presiona RESET OTRA VEZ (double tap)
5. LED amarillo debe parpadear diferente
6. INMEDIATAMENTE (< 2 seg): Ctrl+U
```

#### Solución 3B: Liberar Puerto COM

```
Si algo ocupa puerto:

1. Cierra Monitor Serial
2. Cierra Serial Plotter
3. Cierra otros programas usando COM
4. Reinicia Arduino IDE
5. Intenta upload nuevamente
```

#### Solución 3C: Cable Defectuoso

```
Si todo arriba falla:

1. Prueba OTRO cable USB
   • Algunos cables solo cargan, no transmiten datos
2. Prueba OTRO puerto USB en PC
```

---

## PROBLEMA 4: MONITOR SERIAL NO FUNCIONA

### Síntomas
```
Monitor Serial vacío (no hay datos)
O aparece basura/caracteres raros
```

### Soluciones

#### Solución 4A: Velocidad Incorrecta

```
COMÚN: Mismatch de velocidad

Arduino código:
  Serial.begin(9600);

Arduino IDE Monitor:
  Velocidad: debe ser 9600

SOLUCIÓN:
1. Verifica velocidad en código
2. Selecciona MISMA velocidad en Monitor
```

#### Solución 4B: Basura en Monitor

```
Si ves caracteres raros:

CAUSA: Velocidad incorrecta

Velocidad EQUIVOCADA:
  "äöü›þ¬«œ" = baudrate malo

SOLUCIÓN: Prueba todas (9600, 115200, etc)
```

---

## PROBLEMA 9: SENSOR NO INICIALIZA

### Síntomas
```
"Sensor not found"
"Failed to initialize"
"ERROR al inicializar"
```

### Soluciones

#### Solución 9A: Verificar Conexiones

```
I2C (SGP30, BME280, etc):
  SDA → A4
  SCL → A5
  VCC → 3.3V (NUNCA 5V para sensores 3.3V)
  GND → GND

Verificar con multímetro:
  VCC = 3.3V exactamente
```

#### Solución 9B: Scanner I2C

```
Carga este programa para detectar sensores:

#include <Wire.h>

void setup() {
  Wire.begin();
  Serial.begin(9600);
  delay(2000);
  
  Serial.println("Escaneando I2C...");
  
  byte count = 0;
  for(byte i = 8; i < 120; i++) {
    Wire.beginTransmission(i);
    if(Wire.endTransmission() == 0) {
      Serial.print("Encontrado en: 0x");
      Serial.println(i, HEX);
      count++;
    }
  }
  
  if(count == 0) Serial.println("No encontrados");
}

void loop() { delay(10000); }

¿Ve dirección? → I2C funciona
¿No ve nada? → Problema conexión
```

---

## PROBLEMA 12: SGP30 NO RESPONDE

### Síntomas
```
"Failed to find SGP30 chip"
"SGP30 not found on I2C bus"
"Valores siempre 0"
```

### Soluciones

#### Solución 12A: VOLTAJE CRÍTICO

```
SGP30 es SOLO 3.3V

Síntoma: Conectado a 5V
Resultado: DAÑADO PERMANENTEMENTE

VERIFICAR:
1. Con multímetro: VCC SGP30 = 3.3V exactamente
2. Conectar a 3.3V de Arduino SOLO
3. NO a 5V
```

#### Solución 12B: Pines I2C

```
SGP30 usa I2C en Arduino Nano 33 BLE:
  A4 = SDA (data)
  A5 = SCL (clock)

VERIFICAR:
  • SDA → A4
  • SCL → A5
  • NO intercambiados
```

#### Solución 12C: Calibración

```
SGP30 necesita 15 segundos de calibración

CÓDIGO:
  sgp30.begin();
  delay(15000);      // ESPERAR
  
  // LUEGO usar sensor
```

---

## PROBLEMA 13: GPS SIN SEÑAL

### Síntomas
```
"0 satélites"
"No fix"
"Sin posición"
(después de 5+ minutos)
```

### Soluciones

#### Solución 13A: DEBE SER EN EXTERIOR

```
GPS SOLO funciona afuera

Síntoma: En interior siempre 0 satélites
Solución: Ir a EXTERIOR

REQUISITOS:
  • Cielo despejado
  • Sin árboles/edificios cerca
  • Antena apuntando AL CIELO
  • Esperar 2-5 MINUTOS primera vez
```

#### Solución 13B: First Fix Tarda Tiempo

```
Tiempo obtención satélites:

Cold Start (primer encendido):
  2-5 MINUTOS

Warm Start (misma ubicación):
  30-60 SEGUNDOS

SOLUCIÓN: ESPERAR
```

---

## PROBLEMA 14: MICROSD NO GRABA

### Síntomas
```
"MicroSD ERROR"
"No se crea archivo"
"Datos no se graban"
```

### Soluciones

#### Solución 14A: VOLTAJE 3.3V

```
MicroSD es SOLO 3.3V

Si VCC = 5V: DAÑADO

VERIFICAR:
  Con multímetro: VCC MicroSD = 3.3V exactamente
```

#### Solución 14B: Formatear FAT32

```
MicroSD DEBE estar en FAT32

Windows:
  1. Click derecho en MicroSD
  2. Formatear
  3. Sistema archivos: FAT32
  4. Iniciar
```

#### Solución 14C: Pines SPI

```
MicroSD usa SPI:
  D10 = CS
  D11 = MOSI
  D12 = MISO
  D13 = SCK

VERIFICAR que no estén intercambiados
```

---

## PROBLEMA 15: APC220 NO COMUNICA

### Síntomas
```
"No se reciben datos"
"APC220 configurado pero no funciona"
"Dos módulos no hablan"
```

### Soluciones

#### Solución 15A: MISMA CONFIGURACIÓN

```
CRÍTICO: Ambos APC220 deben estar en MISMA ONDA

Si uno está: 434 MHz
Y otro está: 437 MHz
Resultado: NO COMUNICAN

VERIFICAR:
  Ambos deben mostrar: PARA 434000 3 9 3 0
  (Exactamente igual)
```

#### Solución 15B: Usar Arduino UNO para Configurar

```
Otros métodos (rfmagic, PuTTY) no funcionaron.
Usar Arduino UNO como configurador.

Programa: PROGRAMA_APC220_CONFIGURADOR.ino

Conexión Arduino UNO ↔ APC220:
  GND  → GND
  D13  → VCC
  D12  → EN
  D11  → RXD
  D10  → TXD
  D8   → SET

Comandos:
  RD                  → Leer configuración
  WR 434000 3 9 3 0   → Escribir configuración
```

#### Solución 15C: CONEXIONES DIRECTAS (no cruzadas)

```
IMPORTANTE: La etiqueta TXD/RXD del APC220 indica
dónde conectar el pin del micro, NO la función.

CORRECTO (conexiones directas):
  TX del micro → TXD del APC220
  RX del micro → RXD del APC220

INCORRECTO (cruzadas):
  TX del micro → RXD del APC220  ← NO
```

#### Solución 15D: Pin EN

```
Con Arduino UNO:
  → El programa controla EN (pin D12 a HIGH)

Con USB-TTL o Nano 33 BLE:
  → Conectar EN a VCC (3.3V)
  → O dejarlo sin conectar (a veces funciona)

Si EN está al aire y no funciona:
  → Puentear EN a VCC
```

#### Solución 15E: Nano 33 BLE usa Serial1

```
Arduino Nano 33 BLE NO soporta SoftwareSerial
(usa procesador ARM, no AVR)

SOLUCIÓN: Usar Serial1 en pines 0 y 1

Conexión Nano 33 BLE ↔ APC220:
  Pin 0 (RX) → RXD del APC220
  Pin 1 (TX) → TXD del APC220
  3.3V       → VCC
  GND        → GND

Código:
  Serial1.begin(9600);  // NO SoftwareSerial
  Serial1.println("HOLA");
```

#### Solución 15F: Antenas Conectadas

```
Si no comunican:

VERIFICAR:
  • Antena emisor: conectada
  • Antena receptor: conectada
  
Sin antena el módulo puede ser inestable.
```

#### Solución 15G: Prueba de Comunicación

```
1. Configurar ambos APC220 con Arduino UNO:
   WR 434000 3 9 3 0

2. Cargar en Nano 33 BLE (emisor):
   PROGRAMA_APC220_EMISOR.ino

3. Cargar en Arduino UNO (receptor):
   PROGRAMA_APC220_RECEPTOR.ino

4. Abrir Monitor Serial del receptor:
   Debe mostrar "HOLA" cada 2 segundos

Si no funciona:
  → Verificar conexiones directas
  → Verificar misma configuración
  → Verificar antenas
```

---

## CHECKLIST DE VERIFICACIÓN

Antes de reportar problema, verificar:

```
HARDWARE:
  [ ] ¿Todos los cables conectados?
  [ ] ¿Voltajes correctos (3.3V/GND)?
  [ ] ¿Con multímetro?: VCC = esperado
  [ ] ¿Arduino reconocido en Device Manager?

SOFTWARE:
  [ ] ¿Board correcto?: Arduino Nano 33 BLE
  [ ] ¿Librerías instaladas?
  [ ] ¿Serial.begin(9600) en código?
  [ ] ¿Velocidad Monitor Serial = código?

SENSORES:
  [ ] ¿delay() suficiente en setup()?
  [ ] ¿I2C scanner encuentra sensor?
  [ ] ¿Voltaje correcto medido?

APC220:
  [ ] ¿Configurado con Arduino UNO?
  [ ] ¿Ambos con misma configuración?
  [ ] ¿Conexiones directas (no cruzadas)?
  [ ] ¿Nano 33 BLE usa Serial1?

ANTES DE DESESPERAR:
  [ ] ¿Probé RESET doble?
  [ ] ¿Desconecté/reconecté USB?
  [ ] ¿Cambié puerto USB?
  [ ] ¿Reinicié PC?
```

---

## SI NADA FUNCIONA

Sigue este orden:

```
1. Reinicia PC
   (resuelve 30% de problemas)

2. Reinstala Arduino IDE desde cero
   • Desinstala completamente
   • Borra carpeta Arduino15
   • Descarga e instala nuevo

3. Cambiar Arduino
   • Prueba en otro Arduino (si tienes)
   • Identifica si es placa defectuosa

4. Cambiar sensor/módulo
   • Prueba con otro igual
   • Identifica si es defectuoso

5. Contacta soporte
   • Arduino forums: https://forum.arduino.cc
```

---

**¡No te desesperes, todos estos problemas son solubles!**

**Estado:** Troubleshooting completo  
**Última actualización:** Febrero 2026
