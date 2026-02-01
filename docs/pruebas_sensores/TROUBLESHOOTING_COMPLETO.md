# 🚨 TROUBLESHOOTING COMPLETO
## Problemas y Soluciones - Arduino Nano 33 BLE + CanSat

**Fecha:** Enero 2026  
**Proyecto:** CanSat Misión 2  

---

## 📋 ÍNDICE RÁPIDO

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

## 🔴 PROBLEMA 1: PUERTO COM NO APARECE

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
   ✓ Instala: "Arduino SAMD (32-bits ARM Cortex-M0+)"
   ✓ Instala: "Arduino mbed OS Nano Boards"
   
3. Reinicia Arduino IDE

4. Tools → Board Manager:
   Busca: "Arduino mbed OS Nano Boards"
   Instala versión 4.5.0 o superior
   
5. Espera a que descargue (~500MB)
```

**Si aún no funciona:**

```
Windows + Zephyr/mbed drivers:
1. Descarga: 
   https://github.com/arduino/ArduinoCore-mbed/raw/main/drivers/windows/ArduinoNano33_BLE_Mbed_OS.inf

2. Device Manager:
   - Busca dispositivo sin driver (¿ interrogación?)
   - Click derecho → Update driver
   - Selecciona archivo .inf descargado
   - Instala

3. Reinicia PC
```

#### Solución 1B: Cambiar Puerto USB

```
1. Desconecta Arduino
2. Prueba OTRO puerto USB:
   • Trasero del PC (mejor calidad)
   • Diferente puerto delantero
   • Hub USB diferente

3. Reconecta Arduino
4. Verifica en Device Manager
```

#### Solución 1C: Limpiar Cache Arduino

```
Windows:
1. Cierra Arduino IDE
2. Navega a: C:\Users\[TuUsuario]\AppData\Local\Arduino15
3. Borra carpeta "packages"
4. Reinicia Arduino IDE
5. Espera a que descargue paquetes de nuevo
```

#### Solución 1D: Verificar en Device Manager

```
Windows:
1. Presiona: Windows + X
2. Selecciona: Device Manager
3. Busca bajo "Ports (COM & LPT)":
   - "Silicon Labs CP210x" (normal)
   - "Arduino Nano 33 BLE" (si tienes driver)
   - "USB Serial Device" (genérico)

4. Si ves dispositivo con ¿:
   → Driver no instalado
   → Soluciones 1A aplica
```

### Verificación de Éxito
```
✅ Tools → Port aparece: COM3, COM4, COM5, etc.
✅ No aparece interrogación en Device Manager
✅ Arduino IDE reconoce placa
```

---

## 🔴 PROBLEMA 2: "BOARD NOT RECOGNIZED"

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
4. Espera a que descargue toolchain

⚠️ COMÚN: Seleccionar "Arduino Nano" normal
   Debe ser: "Arduino Nano 33 BLE"
```

#### Solución 2B: Resetear Bootloader

```
Procedimiento especial para Arduino Nano 33 BLE:

1. Desconecta Arduino
2. Espera 5 segundos
3. Reconecta Arduino
4. Arduino IDE detecta puerto

Si no funciona:

5. Presiona RESET en Arduino (botón pequeño)
6. RÁPIDAMENTE haz doble click
   (dentro de 1-2 segundos)
7. Arduino entra en bootloader
   (LED amarillo parpadea diferente)

8. Carga programa INMEDIATAMENTE (Ctrl+U)
```

#### Solución 2C: Verificar Procesador

```
Arduino IDE:
1. Tools → Processor
2. Selecciona: "nRF52840 (SENSE - 256KB)"
3. No debe ser: "nRF52840"

Esto es CRÍTICO para Arduino Nano 33 BLE Sense
```

#### Solución 2D: Cambiar Velocidad Upload

```
Arduino IDE:
1. Tools → Upload Speed
2. Intenta: 115200 (por defecto)
3. Si falla, prueba: 9600

Algunos Arduino falla con velocidad alta
```

### Verificación de Éxito
```
✅ Board: Arduino Nano 33 BLE
✅ Processor: nRF52840 (SENSE - 256KB)
✅ Upload Speed: 115200
✅ Port: COM[X]
```

---

## 🔴 PROBLEMA 3: UPLOAD FALLA

### Síntomas
```
"uploading error"
"timeout error"
"ERROR: FAIL"
"Sketch too big"
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

#### Solución 3C: Reducir Tamaño Sketch

```
Si sketch es muy grande:

En Tools → Optimize for size:
  Desactiva:
    • Debugging info
    • Símbolos extra

O usa sketch más simple para pruebas
```

#### Solución 3D: Cable Defectuoso

```
Si todo arriba falla:

1. Prueba OTRO cable USB
   • Algunos cables solo cargan, no transmiten datos
   • Usa cable de marca conocida (Anker, Belkin)

2. Prueba OTRO puerto USB en PC

3. Si falla sistemáticamente:
   → Probablemente Arduino defectuoso
```

---

## 🔴 PROBLEMA 4: MONITOR SERIAL NO FUNCIONA

### Síntomas
```
Monitor Serial vacío (no hay datos)
O aparece basura/caracteres raros
O se cierra automáticamente
```

### Soluciones

#### Solución 4A: Velocidad Incorrecta

```
COMÚN: Mismatch de velocidad

Arduino código:
  Serial.begin(9600);

Arduino IDE Monitor:
  Velocidad: ¿9600? NO, ¿115200?

SOLUCIÓN:
1. Verifica velocidad en código
2. Selecciona MISMA velocidad en Monitor
3. Popular: 9600, 115200
```

#### Solución 4B: Cerrar y Abrir Monitor

```
1. Cierra Monitor Serial (X)
2. Presiona RESET en Arduino
3. Espera 1 segundo
4. Abre Tools → Serial Monitor
5. Monitor debería mostrar datos

⚠️ Monitor abierto BLOQUEA serial
    Algunos programas interfieren
```

#### Solución 4C: Reset Doble Antes

```
1. Arduino conectado
2. Presiona RESET doble
3. Rápidamente (< 2 seg): Tools → Serial Monitor
4. Aumenta probabilidad de sincronización
```

#### Solución 4D: Basura en Monitor

```
Si ves caracteres raros:

CAUSA: Velocidad incorrecta

SOLUCIONES:
1. Verifica velocidad Serial.begin()
2. Selecciona exacta velocidad en Monitor
3. Si no sabes: Prueba todas (9600, 115200, etc)

Velocidad EQUIVOCADA:
  "äöü›þ¬«œ" = baudrate malo
```

---

## 🟡 PROBLEMA 5: ARDUINO NO SE RECONECTA DESPUÉS

### Síntomas
```
Funcionó una vez, luego:
  • Puerto desaparece
  • "Device disconnected"
  • Hay que desconectar/reconectar USB
```

### Soluciones

#### Solución 5A: Código con Bucle Infinito

```
Código problemático:
  while(1) delay(1000);  // ← Bloquea

SOLUCIÓN:
  Siempre debe haber loop() funcionando
  
  void loop() {
    // algo
    delay(1000);
  }
```

#### Solución 5B: Falta delay() en setup()

```
Código:
  void setup() {
    Serial.begin(9600);
    // ← Falta: delay(2000);
  }

SOLUCIÓN:
  void setup() {
    Serial.begin(9600);
    delay(2000);  // ← Espera a estabilizar
  }
```

#### Solución 5C: Desconectar Sensores

```
Si Arduino desaparece cuando conectas sensor:

1. Desconecta Arduino
2. Desconecta TODOS los sensores
3. Reconecta solo Arduino
4. ¿Aparece puerto? SI → Sensor causa problema

CULPABLE: Sensor en voltaje incorrecto
  • SGP30 en 5V en lugar de 3.3V
  • MicroSD en 5V
  • Corto circuito

SOLUCIÓN:
  • Verificar voltaje correcto
  • Cambiar sensor defectuoso
```

---

## 🟡 PROBLEMA 6: ERROR DE COMPILACIÓN

### Síntomas
```
Botón Upload aparece gris
O muestra:
  "error: 'Serial' was not declared"
  "error: no matching function"
```

### Soluciones

#### Solución 6A: Falta #include

```
ERROR:
  error: 'Serial' was not declared

SOLUCIÓN:
  Agrega al inicio:
  #include <Arduino.h>

O simplemente: Verifica que sea sketch .ino
```

#### Solución 6B: Falta Librería

```
ERROR:
  fatal error: Adafruit_SGP30.h: No such file

SOLUCIÓN:
1. Sketch → Include Library → Manage Libraries
2. Busca: "Adafruit SGP30"
3. Instala
4. Reinicia Arduino IDE
5. Recompila
```

#### Solución 6C: Conflicto de Nombres

```
ERROR:
  variable 'x' was not declared

SOLUCIÓN:
  Verifica:
    • No uses nombres de librerías como variables
    • Redeclaración de variables
    • Ámbito de variables

EJEMPLO:
  int Serial = 5;  // ❌ Serial es librería
```

---

## 🟡 PROBLEMA 7: LIBRERÍA NO ENCONTRADA

### Síntomas
```
"library not found"
"You need to install"
"Please install the following libraries"
```

### Soluciones

#### Solución 7A: Instalar Librería Manual

```
Arduino IDE:
1. Sketch → Include Library → Manage Libraries
2. Busca nombre completo de librería
   (ej: "Adafruit SGP30" no "SGP30")
3. Instala la OFICIAL (por Adafruit, Arduino, etc)
4. Espera descarga
5. Reinicia Arduino IDE
```

#### Solución 7B: Librería Alternativa

```
Si no existe librería:

Opciones:
  • Buscar librería alternativa compatible
  • Descargar manualmente desde GitHub
  • Guardar en: Documents/Arduino/libraries/

Ejemplo:
  Descargado ReefwingLPS22HB.zip
  Guardar en: .../Arduino/libraries/ReefwingLPS22HB/
```

#### Solución 7C: Verificar Arquitectura

```
Advertencia (pero compila):
  "library pretends to run on avr but may be incompatible"

CAUSA: Librería para AVR, no MBED

SOLUCIÓN:
  • Usar librería oficial de Arduino (MBED compatible)
  • O ignorar advertencia si funciona
  • Mejor: Cambiar a librería correcta
```

---

## 🔴 PROBLEMA 9: SENSOR NO INICIALIZA

### Síntomas
```
Monitor Serial muestra:
  "Sensor... ❌ ERROR"
  "Failed to initialize"
  "Sensor not found"
```

### Soluciones

#### Solución 9A: Verificar Conexión Física

```
1. Apaga Arduino
2. Verifica CADA pin:
   • SDA/RXD conectado
   • SCL/TX conectado
   • VCC conectado
   • GND conectado
   • ¿Hay soldaduras frias? Resuelda
3. Enciende Arduino nuevamente
```

#### Solución 9B: Verificar Voltaje

```
¡CRÍTICO! Muchos sensores son 3.3V:

Con multímetro:
1. Mide VCC del sensor
2. Debe ser: 3.3V exactamente
3. Si es 5V: ❌ DAÑADO el sensor

SENSORES 3.3V SOLO:
  • SGP30
  • MicroSD
  • APC220 (a veces)
```

#### Solución 9C: Verificar I2C

```
Para sensores I2C (SDA/SCL):

Programa Scanner I2C:
#include <Wire.h>

void setup() {
  Serial.begin(9600);
  delay(3000);
  
  Serial.println("Buscando dispositivos I2C...");
  
  byte count = 0;
  for(byte i = 8; i < 120; i++) {
    Wire.beginTransmission(i);
    if(Wire.endTransmission() == 0) {
      Serial.print("✓ Encontrado en: 0x");
      Serial.println(i, HEX);
      count++;
    }
  }
  
  if(count == 0) Serial.println("❌ No encontrados");
}

void loop() { delay(10000); }

¿Ve dirección? → I2C funciona
¿No ve nada? → Problema conexión
```

#### Solución 9D: Reiniciar Arduino

```
1. Desconecta USB
2. Espera 10 segundos
3. Reconecta USB
4. Carga programa nuevamente
```

---

## 🟡 PROBLEMA 10: VALORES RAROS/NaN

### Síntomas
```
Monitor Serial muestra:
  "Temperatura: nan"
  "Presión: -999.99"
  "Valor: 0.000000"
  Valores cambian aleatoriamente
```

### Soluciones

#### Solución 10A: Sensor Necesita Tiempo

```
Algunos sensores necesitan estabilización:

Problema: Leer inmediatamente después de iniciar

SOLUCIÓN:
  void setup() {
    sensor.begin();
    delay(1000);      // ← Esperar
    delay(15000);     // ← SGP30: 15 segundos
  }
```

#### Solución 10B: Inicialización Incorrecta

```
Código problemático:
  SGP30.begin();     // Sin verificación
  valor = SGP30.read();  // Lectura fallida

SOLUCIÓN:
  if (!SGP30.begin()) {
    Serial.println("ERROR");
    while(1) delay(1000);
  }
  
  // LUEGO leer valores
```

#### Solución 10C: Interferencia I2C

```
Si sensores I2C dan valores raros:

Causas:
  • Múltiples sensores I2C en mismo bus
  • Cables demasiado largos
  • Ruido electromagnético

SOLUCIONES:
  1. Cables cortos
  2. Usar resistencias pull-up (si faltan)
  3. Separar sensores espacialmente
  4. Proteger con malla de Faraday (avanzado)
```

#### Solución 10D: Potencia Insuficiente

```
Si batería está descargada:

Síntomas: Valores raros, reset aleatorio

SOLUCIONES:
  1. Cargar batería completamente
  2. Usar fuente USB mejor (más amperaje)
  3. Quitar sensores no esenciales
```

---

## 🔴 PROBLEMA 12: SGP30 NO RESPONDE

### Síntomas
```
"Failed to find SGP30 chip"
"SGP30 not found on I2C bus"
"Valores siempre 0"
```

### Soluciones

#### Solución 12A: VOLTAJE CRÍTICO

```
⚠️ SGP30 es SOLO 3.3V

Síntoma: Conectado a 5V
Resultado: ❌ DAÑADO PERMANENTEMENTE

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
  delay(15000);      // ← ESPERAR
  
  // LUEGO usar sensor
```

#### Solución 12D: Scanner I2C

```
Verifica si Arduino "ve" SGP30:

Usa programa de Solución 9C
Busca: 0x58

Si NO aparece 0x58:
  • Cables mal conectados
  • Voltaje incorrecto
  • SGP30 defectuoso
```

---

## 🟡 PROBLEMA 13: GPS SIN SEÑAL

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
⚠️ GPS SOLO funciona afuera

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
  ⏱️ 2-5 MINUTOS

Warm Start (misma ubicación):
  ⏱️ 30-60 SEGUNDOS

Hot Start (con datos cacheados):
  ⏱️ 5-15 SEGUNDOS

SOLUCIÓN: ESPERAR
```

#### Solución 13C: Antena GPS

```
Sin antena GPS:
  • NO funciona
  • 0 satélites siempre

VERIFICAR:
  • Antena conectada a módulo GPS
  • Antena apuntando al cielo
  • Antena no bloqueada
```

#### Solución 13D: Pines D2/D4

```
GPS usa SoftwareSerial:
  D2 = RX (recibe)
  D4 = TX (transmite)

VERIFICAR:
  • D2 conectado a GPS TX
  • D4 conectado a GPS RX
  • NO intercambiados
```

---

## 🟡 PROBLEMA 14: MICROSD NO GRABA

### Síntomas
```
"MicroSD ERROR"
"No se crea archivo"
"Datos no se graban"
```

### Soluciones

#### Solución 14A: VOLTAJE 3.3V

```
⚠️ MicroSD es SOLO 3.3V

Si VCC = 5V: ❌ DAÑADO

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
  4. Tamaño unidad: 4096 bytes
  5. Iniciar
  
Si falla:
  • Usar otro formateador
  • Probar otra MicroSD
```

#### Solución 14C: Pines SPI

```
MicroSD usa SPI:
  D10 = CS (chip select)
  D11 = MOSI
  D12 = MISO
  D13 = SCK

VERIFICAR:
  • D10 → CS
  • D11 → MOSI
  • D12 → MISO
  • D13 → SCK
  • NO intercambiados
```

#### Solución 14D: Espacio en Disco

```
Si MicroSD llena:
  → No graba

SOLUCIONES:
  1. Borrar archivos antiguos
  2. Usar MicroSD nueva
  3. Formatear
```

---

## 🔴 PROBLEMA 15: APC220 NO COMUNICA

### Síntomas
```
"No se reciben datos"
"APC220 configurado pero no funciona"
"Dos módulos no hablan"
```

### Soluciones

#### Solución 15A: MISMA CONFIGURACIÓN

```
⚠️ CRÍTICO: Ambos APC220 deben estar en MISMA ONDA

Si uno está: 434 MHz
Y otro está: 437 MHz
Resultado: ❌ NO COMUNICAN

VERIFICAR:
  Ambos deben mostrar: PARAM 434000 3 9 3 0
  (Exactamente igual)
```

#### Solución 15B: Verificar Configuración

```
Usa PROGRAMA_CONFIGURACION_APC220.ino:

1. Carga en Arduino
2. Selecciona opción 1 (Leer)
3. Verifica que muestra: PARAM 434000 3 9 3 0
4. Si diferente → Reconfigurar con opción 2
```

#### Solución 15C: Antenas Conectadas

```
Si no comunican:

VERIFICAR:
  • Antena emisor: conectada y firmemente
  • Antena receptor: conectada y firmemente
  • ¿Ambas apuntando misma dirección?

Sin antena: NO funciona
```

#### Solución 15D: Distancia y Línea Vista

```
APC220 necesita línea vista:

Problema: Edificios/árboles entre antenas
Solución: Alejar a campo abierto

Pruebas:
  • 10m línea vista: ✅ Debe funcionar
  • Si no funciona: problema configuración
```

---

## 📋 CHECKLIST DE VERIFICACIÓN

Antes de reportar problema, verificar:

```
HARDWARE:
  ☐ ¿Todos los cables conectados?
  ☐ ¿Voltajes correctos (3.3V/GND)?
  ☐ ¿Con multímetro?: VCC = esperado
  ☐ ¿Soldaduras frías? Resuelda
  ☐ ¿Arduino reconocido en Device Manager?

SOFTWARE:
  ☐ ¿Board correcto?: Arduino Nano 33 BLE
  ☐ ¿Processor correcto?: nRF52840 (SENSE - 256KB)
  ☐ ☐ ¿Librerías instaladas?
  ☐ ¿Serial.begin(9600) en código?
  ☐ ¿Velocidad Monitor Serial = código?

SENSORES:
  ☐ ¿delay() suficiente en setup()?
  ☐ ¿I2C scanner encuentra sensor?
  ☐ ¿Voltaje correcto medido?
  ☐ ¿Sensor necesita calibración? Esperar.

ANTES DE DESESPERAR:
  ☐ ¿Probé RESET doble?
  ☐ ¿Desconecté/reconecté USB?
  ☐ ¿Cambié puerto USB?
  ☐ ¿Reinicié PC?
```

---

## 🆘 SI NADA FUNCIONA

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

4. Cambiar sensor
   • Prueba con otro sensor igual
   • Identifica si es sensor defectuoso

5. Contacta soporte
   • Arduino forums: https://forum.arduino.cc
   • GitHub issues del proyecto
```

---

## 📞 RECURSOS

```
Arduino Official:
  https://www.arduino.cc/en/Guide/ArduinoNano33BLE

Foros Arduino:
  https://forum.arduino.cc/c/using-arduino/arduino-programming-language

GitHub Arduino mbed:
  https://github.com/arduino/ArduinoCore-mbed/issues

StackOverflow:
  Tag: arduino-nano-33-ble
```

---

**¡No te desesperes, todos estos problemas son solubles!** 💪

**Estado:** ✅ Troubleshooting completo  
**Última actualización:** Enero 2026
**Versión:** Actualizado según feedback real
