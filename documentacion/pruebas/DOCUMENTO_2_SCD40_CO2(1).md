# 📋 DOCUMENTO 2: SENSOR SCD40 - MEDICIÓN DE CO2 REAL

## Objetivo
Integrar sensor SCD40 (CO2 real + Temperatura + Humedad) para detectar firmas de combustión con precisión.

---

## ⚠️ ¿Por qué SCD40 y no SGP30?

| Característica | SGP30 | SCD40 |
|----------------|-------|-------|
| **Tipo de medición** | eCO2 (estimado) | CO2 real (NDIR) |
| **Tecnología** | MOX (Metal Oxide) | NDIR (Infrarrojo) |
| **Uso exterior** | ❌ No fiable | ✅ Preciso |
| **Baseline** | Necesita calibración | Auto-calibración |
| **Precisión** | ±15% (estimación) | ±(50ppm + 5%) |

**Conclusión:** El SGP30 estima CO2 a partir de VOCs, lo cual NO funciona en exteriores donde el aire está limpio. El SCD40 mide CO2 real mediante infrarrojo, ideal para detectar combustión.

---

## 📡 SCD40 - Especificaciones

```
Fabricante: Sensirion
Voltaje: 2.4V - 5.5V (usa 3.3V con Arduino Nano 33 BLE)
Protocolo: I2C
Dirección: 0x62
Funciones: CO2 (ppm) + Temperatura (°C) + Humedad (%)
Rango CO2: 400 - 5000 ppm (ampliable a 40000 ppm)
Precisión CO2: ±(50 ppm + 5% del valor)
Tiempo respuesta: 5 segundos por medición
```

---

## 🔌 Conexión Física

**RECOMENDADO:** Usar 3.3V para compatibilidad con Arduino Nano 33 BLE

```
Arduino Nano 33 BLE:

A4 (SDA)  ──→ SCD40 SDA
A5 (SCL)  ──→ SCD40 SCL
GND       ──→ SCD40 GND
3.3V      ──→ SCD40 VCC
```

**Verificar con multímetro:** VCC debe mostrar 3.3V

### Pinout del módulo SCD40

```
┌─────────────────┐
│     SCD40       │
│                 │
│  VCC  GND  SCL  SDA
│   │    │    │    │
└───┼────┼────┼────┼──
    │    │    │    │
   3.3V GND  A5   A4
        Arduino Nano 33 BLE
```

---

## 📥 Instalación Librería

```
Sketch → Include Library → Manage Libraries

Buscar: "Sensirion I2C SCD4x"
Instalar: Sensirion I2C SCD4x by Sensirion (última versión)

También instalar (dependencia):
Buscar: "Sensirion Core"
Instalar: Sensirion Core by Sensirion

Reiniciar Arduino IDE
```

---

## ✅ Verificación Previa

Antes de cargar el programa principal, verifica que SCD40 responde en I2C:

```cpp
#include <Wire.h>

void setup() {
  Serial.begin(9600);
  delay(2000);
  Wire.begin();
  
  Serial.println("Buscando SCD40 en I2C...");
  Serial.println("Dirección esperada: 0x62");
  Serial.println();
  
  byte count = 0;
  for(byte i = 8; i < 120; i++) {
    Wire.beginTransmission(i);
    if(Wire.endTransmission() == 0) {
      Serial.print("✓ Encontrado en: 0x");
      if(i < 16) Serial.print("0");
      Serial.println(i, HEX);
      
      if(i == 0x62) {
        Serial.println("  → ¡Este es el SCD40!");
      }
      count++;
    }
  }
  
  if(count == 0) {
    Serial.println("❌ No se encontraron dispositivos I2C");
    Serial.println("Verifica:");
    Serial.println("  - SDA conectado a A4");
    Serial.println("  - SCL conectado a A5");
    Serial.println("  - VCC conectado a 3.3V");
    Serial.println("  - GND conectado");
  }
}

void loop() {
  delay(10000);
}
```

**Resultado esperado:** `✓ Encontrado en: 0x62 → ¡Este es el SCD40!`

---

## 💻 PROGRAMA DE PRUEBA

**Archivo:** `PROGRAMA_2_SCD40_CO2.ino`

```cpp
/*
 * CanSat Misión 2 - Prueba Sensor SCD40
 * Mide: CO2 real (ppm) + Temperatura (°C) + Humedad (%)
 * 
 * Conexiones:
 *   SDA → A4
 *   SCL → A5
 *   VCC → 3.3V
 *   GND → GND
 */

#include <Wire.h>
#include <SensirionI2CScd4x.h>

SensirionI2CScd4x scd4x;

// Variables
uint16_t co2 = 0;
float temperatura = 0.0;
float humedad = 0.0;
int contador = 0;

void setup() {
  Serial.begin(9600);
  delay(2000);
  
  Serial.println("╔═══════════════════════════════════════════╗");
  Serial.println("║  CanSat Misión 2 - Sensor SCD40 (CO2)     ║");
  Serial.println("║  Tecnología: NDIR (CO2 real)              ║");
  Serial.println("╚═══════════════════════════════════════════╝");
  Serial.println();
  
  // Inicializar I2C
  Wire.begin();
  
  // Inicializar SCD40
  Serial.print("Inicializando SCD40... ");
  scd4x.begin(Wire);
  
  // Detener mediciones previas (por si acaso)
  uint16_t error = scd4x.stopPeriodicMeasurement();
  if (error) {
    Serial.println("Aviso: No había medición activa");
  }
  
  // Iniciar mediciones periódicas
  error = scd4x.startPeriodicMeasurement();
  if (error) {
    Serial.println("❌ ERROR al iniciar mediciones");
    Serial.println("Verifica conexiones:");
    Serial.println("  SDA → A4");
    Serial.println("  SCL → A5");
    Serial.println("  VCC → 3.3V");
    Serial.println("  GND → GND");
    while(1) delay(1000);
  }
  
  Serial.println("✓ OK");
  Serial.println();
  Serial.println("⏳ Esperando primera medición (5 segundos)...");
  Serial.println();
  delay(5000);
  
  // Cabecera de datos
  Serial.println("╔═══════╦═══════════╦═══════════╦═══════════╦════════════════╗");
  Serial.println("║   N°  ║  CO2(ppm) ║  Temp(°C) ║  Hum(%)   ║    Estado      ║");
  Serial.println("╠═══════╬═══════════╬═══════════╬═══════════╬════════════════╣");
}

void loop() {
  uint16_t error;
  bool dataReady = false;
  
  // Verificar si hay datos disponibles
  error = scd4x.getDataReadyFlag(dataReady);
  
  if (error) {
    Serial.println("║ Error al verificar datos                              ║");
    delay(1000);
    return;
  }
  
  if (!dataReady) {
    delay(100);
    return;
  }
  
  // Leer mediciones
  error = scd4x.readMeasurement(co2, temperatura, humedad);
  
  if (error) {
    Serial.println("║ Error al leer mediciones                              ║");
    delay(1000);
    return;
  }
  
  // Determinar estado de calidad del aire
  String estado = clasificarCO2(co2);
  
  // Mostrar datos en formato tabla
  Serial.print("║ ");
  if(contador < 10) Serial.print(" ");
  if(contador < 100) Serial.print(" ");
  if(contador < 1000) Serial.print(" ");
  Serial.print(contador);
  Serial.print(" ║   ");
  
  // CO2
  if(co2 < 10) Serial.print(" ");
  if(co2 < 100) Serial.print(" ");
  if(co2 < 1000) Serial.print(" ");
  Serial.print(co2);
  Serial.print("   ║   ");
  
  // Temperatura
  if(temperatura < 10) Serial.print(" ");
  Serial.print(temperatura, 1);
  Serial.print("   ║   ");
  
  // Humedad
  if(humedad < 10) Serial.print(" ");
  Serial.print(humedad, 1);
  Serial.print("   ║ ");
  
  // Estado
  Serial.print(estado);
  // Rellenar espacios para alinear
  for(int i = estado.length(); i < 14; i++) Serial.print(" ");
  Serial.println(" ║");
  
  contador++;
  delay(5000);  // SCD40 actualiza cada 5 segundos
}

// Función para clasificar calidad del aire por CO2
String clasificarCO2(uint16_t ppm) {
  if (ppm < 450) return "🟢 Excelente";
  if (ppm < 600) return "🟢 Bueno";
  if (ppm < 1000) return "🟡 Moderado";
  if (ppm < 1500) return "🟠 Malo";
  if (ppm < 2500) return "🔴 Muy malo";
  return "🔴 Peligroso";
}
```

---

## 📊 Interpretación de Valores

### CO2 - Dióxido de Carbono (medición real NDIR)

| CO2 (ppm) | Calidad | Situación típica |
|-----------|---------|------------------|
| 400-450 | 🟢 Excelente | Aire exterior limpio (baseline atmosférico) |
| 450-600 | 🟢 Bueno | Zona urbana con vegetación |
| 600-1000 | 🟡 Moderado | Tráfico moderado, interior ventilado |
| 1000-1500 | 🟠 Malo | Tráfico intenso, mala ventilación |
| 1500-2500 | 🔴 Muy malo | Combustión activa cercana |
| >2500 | 🔴 Peligroso | Fuente directa de combustión |

### Temperatura y Humedad (bonus del SCD40)

El SCD40 también mide temperatura y humedad, útiles para:
- Compensar mediciones de otros sensores
- Datos ambientales adicionales
- Verificar funcionamiento del sensor

---

## 🔥 Firmas de Combustión Detectables

### Tráfico Vehicular 🚗
- CO2: 450-600 ppm
- Patrón: Incremento gradual cerca de carreteras
- Correlación: Alto con PM2.5 del HM3301

### Generadores Diésel 🚜
- CO2: 600-1000 ppm
- Patrón: Picos pronunciados localizados
- Correlación: Muy alto con PM2.5

### Biomasa/Fuego 🔥
- CO2: 800-1500+ ppm
- Patrón: Elevación sostenida con humo
- Correlación: Extremadamente alto con PM2.5

### Zona Industrial 🏭
- CO2: 500-800 ppm
- Patrón: Fluctuaciones continuas
- Correlación: Variable con PM2.5

---

## 🎯 Interpretación Combinada CO2 + PM2.5

**IMPORTANTE:** Para detectar firmas de combustión, combina SCD40 con HM3301:

```
CO2 ALTO + PM2.5 ALTO   → Combustión activa (fuego, motor encendido)
CO2 ALTO + PM2.5 BAJO   → Respiración/Fermentación (raro en exterior)
CO2 BAJO + PM2.5 ALTO   → Polvo sin combustión (obra, viento)
CO2 BAJO + PM2.5 BAJO   → Aire limpio ✓
```

---

## ⚡ Compensación de Presión (Opcional)

Para mayor precisión, puedes compensar con la presión del LPS22HB:

```cpp
// Después de leer presión del LPS22HB (en hPa)
float presion = lps22hb.readPressure();  // ej: 929.5 hPa

// Compensar SCD40 (mejora precisión ~1-2%)
scd4x.setAmbientPressure((uint16_t)presion);
```

---

## ⚠️ Checklist Antes de Vuelo

```
☐ SCD40 conectado a A4 (SDA) y A5 (SCL)
☐ Voltaje 3.3V verificado con multímetro
☐ GND conectado
☐ I2C scanner muestra 0x62
☐ Librería Sensirion I2C SCD4x instalada
☐ Programa carga sin errores
☐ Primera lectura después de 5 segundos
☐ CO2 en exterior: 400-450 ppm (baseline normal)
☐ Temperatura coherente con ambiente
☐ Humedad coherente con ambiente
```

---

## 🚨 Troubleshooting

### Error: "No se encontró SCD40" / No aparece 0x62

```
1. Verificar conexión física:
   - A4 conectado a SDA
   - A5 conectado a SCL
   - 3.3V conectado a VCC
   - GND conectado a GND

2. Verificar voltaje con multímetro:
   - VCC del SCD40 = 3.3V

3. Ejecutar I2C Scanner:
   - Si no aparece 0x62, problema de conexión
   - Si aparece otra dirección, sensor diferente

4. Presiona RESET doble en Arduino
5. Recarga programa
```

### CO2 siempre muestra 0 o valores negativos

```
1. Esperar 5 segundos después de iniciar
   - SCD40 necesita tiempo para primera medición

2. Verificar que se llamó a startPeriodicMeasurement()

3. Verificar dataReady antes de leer
```

### CO2 siempre ~400 ppm (no cambia)

```
ESTO ES NORMAL EN EXTERIOR
- 400 ppm es el baseline atmosférico
- El CO2 en aire limpio exterior es ~415-420 ppm actualmente

Para probar que funciona:
- Respira cerca del sensor (debe subir a 800-1500 ppm)
- Acerca una vela encendida (con cuidado, debe subir)
```

### Valores de CO2 muy altos constantemente (>2000 ppm)

```
1. ¿Estás en interior cerrado?
   - Normal en habitaciones sin ventilación

2. ¿Hay fuente de combustión cerca?
   - Cocina, calefacción, vehículos

3. Verificar que no haya cortocircuito
```

---

## 📝 Notas Importantes

```
✅ SCD40 mide CO2 REAL
   A diferencia del SGP30, usa tecnología NDIR
   Funciona correctamente en exterior

✅ Primera medición tarda 5 segundos
   No confíes en lecturas antes de ese tiempo

✅ Auto-calibración
   El SCD40 se auto-calibra asumiendo exposición
   a aire limpio (~400 ppm) al menos 1 hora/semana

✅ Compensación de presión opcional
   Mejora precisión en altitud (CanSat bajando)
   Usa presión del LPS22HB

✅ Combinar con HM3301
   CO2 + PM2.5 = detección precisa de combustión
   Ver documento 3 para HM3301
```

---

## 🔗 Referencias

- Datasheet SCD40: https://sensirion.com/products/catalog/SCD40/
- Librería Arduino: https://github.com/Sensirion/arduino-i2c-scd4x
- Niveles CO2 atmosférico: https://www.co2.earth/

---

## 🎯 Próximo Paso

**Documento 3:** Sensor HM3301 - Partículas PM2.5

Archivo: `DOCUMENTO_3_HM3301_PM25.md`

---

**Estado:** ✅ SCD40 - Sensor CO2 real NDIR  
**Última actualización:** Febrero 2026
