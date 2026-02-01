# 📋 DOCUMENTO 1: PUESTA EN MARCHA ARDUINO NANO 33 BLE SENSE

## Objetivo
Verificar que Arduino Nano 33 BLE Sense funciona correctamente con sus sensores integrados.

---

## 🎯 SENSORES INTEGRADOS EN ARDUINO NANO 33 BLE SENSE REV2

| Sensor | Modelo | Función | Conexión |
|--------|--------|---------|----------|
| **Acelerómetro + Giroscopio** | BMI270 | Movimiento + Rotación | I2C (integrado) |
| **Magnetómetro** | BMM150 | Brújula/Orientación | I2C (integrado) |
| **Presión + Temperatura** | LPS22HB | Altitud + Temperatura compensación | I2C (integrado) |
| **Temperatura + Humedad** | HS3003 | Datos ambientales REALES | I2C (integrado) |
| **Luz/Color/Proximidad** | APDS9960 | Luz ambiente | I2C (integrado) |

---

## 📥 INSTALACIÓN DE LIBRERÍAS

En Arduino IDE:

```
Sketch → Include Library → Manage Libraries

Instala:
  ✅ Arduino_BMI270_BMM150
  ✅ ReefwingLPS22HB
  ✅ Arduino_HS300x
  ✅ Arduino_APDS9960
```

**IMPORTANTE:** Reinicia Arduino IDE después de instalar librerías.

---

## ⚙️ CONFIGURACIÓN ARDUINO IDE

```
Tools → Board: "Arduino Nano 33 BLE"
Tools → Port: Selecciona puerto COM
Tools → Upload Speed: 115200
Tools → Processor: nRF52840 (SENSE - 256KB)
```

---

## 💻 PROGRAMA DE PRUEBA - SENSORES INTEGRADOS

```cpp
/*
 * Arduino Nano 33 BLE Sense - Prueba Sensores Integrados
 * Temperatura (HS3003) + Humedad + Presión + IMU
 */

#include <Arduino_BMI270_BMM150.h>
#include <ReefwingLPS22HB.h>
#include <Arduino_HS300x.h>

ReefwingLPS22HB pressureSensor;

// Variables
float temp_hs = 0, humedad = 0;
float temp_lps = 0, presion = 0;
float accelX = 0, accelY = 0, accelZ = 0;

void setup() {
  Serial.begin(9600);
  delay(2000);
  
  Serial.println();
  Serial.println("╔════════════════════════════════════════╗");
  Serial.println("║  Arduino Nano 33 BLE - Sensores       ║");
  Serial.println("║  Integrados (HS3003 + LPS22HB + IMU)  ║");
  Serial.println("╚════════════════════════════════════════╝");
  Serial.println();
  
  // Inicializar HS3003 (Temperatura + Humedad)
  Serial.print("HS3003 (Temp+Humedad)... ");
  if (!HS300x.begin()) {
    Serial.println("❌ ERROR");
  } else {
    Serial.println("✓ OK");
  }
  
  // Inicializar LPS22HB (Presión)
  Serial.print("LPS22HB (Presión)... ");
  pressureSensor.begin();
  if (pressureSensor.connected()) {
    Serial.println("✓ OK");
  } else {
    Serial.println("❌ ERROR");
  }
  
  // Inicializar IMU (Acelerómetro + Giroscopio)
  Serial.print("IMU (BMI270+BMM150)... ");
  if (!IMU.begin()) {
    Serial.println("❌ ERROR");
  } else {
    Serial.println("✓ OK");
  }
  
  Serial.println();
  Serial.println("═══════════════════════════════════════════");
  Serial.println("Sistema listo. Leyendo sensores...");
  Serial.println();
}

void loop() {
  // Leer HS3003 (Temperatura REAL + Humedad)
  temp_hs = HS300x.readTemperature();
  humedad = HS300x.readHumidity();
  
  // Leer LPS22HB (Presión)
  presion = pressureSensor.readPressure() / 100.0;  // Convertir a hPa
  
  // Leer IMU
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(accelX, accelY, accelZ);
  }
  
  // Mostrar datos
  Serial.print("Temp HS3003: ");
  Serial.print(temp_hs, 1);
  Serial.print("°C | Humedad: ");
  Serial.print(humedad, 1);
  Serial.print("% | Presión: ");
  Serial.print(presion, 1);
  Serial.print(" hPa | AccelZ: ");
  Serial.println(accelZ, 2);
  
  delay(2000);
}
```

---

## ✅ CHECKLIST FUNCIONAMIENTO

```
Al cargar el programa deberías ver:

✓ Mensaje inicial en Serial Monitor
✓ Confirmación "✓ OK" para HS3003
✓ Confirmación "✓ OK" para LPS22HB
✓ Confirmación "✓ OK" para IMU
✓ Lecturas de sensores cada 2 segundos:
  - Temperatura HS3003: ~20-25°C (REAL, no compensada)
  - Humedad: ~40-70%
  - Presión: ~930 hPa (según altitud)
  - Aceleración Z: ~1.0 m/s² (gravedad en reposo)
```

---

## ⚠️ TROUBLESHOOTING

### Problema: No aparece Serial Monitor

```
Solución:
  1. Tools → Port → Selecciona puerto COM
  2. Si no aparece puerto:
     - Desconecta USB
     - Espera 5 segundos
     - Reconecta USB
  3. Reinicia Arduino IDE
```

### Problema: Sensor muestra ❌ ERROR

```
Solución:
  1. Verifica que librerías estén instaladas
  2. Reinicia Arduino IDE
  3. Recarga el programa
```

### Problema: Valores raros (NaN o 0)

```
Solución:
  1. Espera 5 segundos después de cargar
  2. Los sensores necesitan tiempo de estabilización
  3. Verifica que no haya interferencia I2C
```

---

## 📊 NOTAS IMPORTANTES

```
✅ Temperatura HS3003:
   - Es la temperatura ambiente REAL
   - NO es temperatura compensada
   - Válida para CanSat Misión 2

✅ Presión LPS22HB:
   - Precisa para altitud
   - A nivel del mar: ~1013 hPa
   - En Madrid (600m): ~930 hPa

✅ IMU:
   - Acelerómetro: ±4g de rango
   - En reposo Z = 1.0 m/s² (gravedad)
   - Útil para detectar impactos/caída
```

---

## 🚀 SIGUIENTE PASO

Una vez confirmado que todo funciona correctamente, pasar al **Documento 2: Integración SGP30**

---

**Fecha:** Enero 2026  
**Proyecto:** CanSat Misión 2  
**Estado:** ✅ Completado
