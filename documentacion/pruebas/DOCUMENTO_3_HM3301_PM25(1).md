# 📋 DOCUMENTO 3: SENSOR HM3301 - PARTÍCULAS PM2.5

## Objetivo
Integrar sensor HM3301 (PM1.0, PM2.5, PM10) para detectar partículas en suspensión y complementar la detección de firmas de combustión junto con el SCD40.

---

## 📡 HM3301 - Especificaciones

```
Fabricante: Seeed Studio (Grove)
Modelo: HM3301 / Grove Laser PM2.5 Sensor
Voltaje: 3.3V - 5V (compatible con ambos)
Protocolo: I2C
Dirección: 0x40
Tecnología: Láser de dispersión
Funciones: PM1.0 + PM2.5 + PM10 (µg/m³)
Rango: 0 - 1000 µg/m³
Precisión: ±10% (lectura) o ±10 µg/m³
Tiempo respuesta: ~1 segundo
```

---

## 🔬 ¿Qué mide el HM3301?

| Partícula | Tamaño | Fuentes típicas |
|-----------|--------|-----------------|
| **PM1.0** | < 1 µm | Humo fino, combustión completa |
| **PM2.5** | < 2.5 µm | Diésel, humo, combustión |
| **PM10** | < 10 µm | Polvo, polen, partículas gruesas |

**PM2.5 es el indicador clave** para detectar combustión porque:
- Penetra profundamente en los pulmones
- Se correlaciona directamente con quema de combustibles
- Estándar internacional de calidad del aire

---

## 🔌 Conexión Física

El HM3301 es compatible con 3.3V y 5V, pero usamos 3.3V por compatibilidad con el Arduino Nano 33 BLE.

```
Arduino Nano 33 BLE:

A4 (SDA)  ──→ HM3301 SDA (cable blanco Grove)
A5 (SCL)  ──→ HM3301 SCL (cable amarillo Grove)
GND       ──→ HM3301 GND (cable negro Grove)
3.3V      ──→ HM3301 VCC (cable rojo Grove)
```

### Si usas conector Grove

```
Grove Shield conectado al Arduino Nano 33 BLE
Cable Grove I2C del HM3301 → Puerto I2C del Shield

Colores estándar Grove:
  🔴 Rojo    = VCC (3.3V)
  ⚫ Negro   = GND
  ⚪ Blanco  = SDA
  🟡 Amarillo = SCL
```

### Pinout del módulo HM3301

```
┌─────────────────────────┐
│        HM3301           │
│    (Sensor láser)       │
│                         │
│  VCC  GND  SCL  SDA     │
│   │    │    │    │      │
└───┼────┼────┼────┼──────┘
    │    │    │    │
   3.3V GND  A5   A4
        Arduino Nano 33 BLE
```

---

## 📥 Instalación Librería

```
Sketch → Include Library → Manage Libraries

Buscar: "Seeed HM330X"
Instalar: Grove - Laser PM2.5 Sensor HM3301 by Seeed Studio

Reiniciar Arduino IDE
```

**Alternativa si no encuentras la librería:**
- Descargar desde: https://github.com/Seeed-Studio/Seeed_PM2_5_sensor_HM3301
- Sketch → Include Library → Add .ZIP Library

---

## ✅ Verificación Previa

Verifica que HM3301 responde en I2C (dirección 0x40):

```cpp
#include <Wire.h>

void setup() {
  Serial.begin(9600);
  delay(2000);
  Wire.begin();
  
  Serial.println("Buscando HM3301 en I2C...");
  Serial.println("Dirección esperada: 0x40");
  Serial.println();
  
  byte count = 0;
  for(byte i = 8; i < 120; i++) {
    Wire.beginTransmission(i);
    if(Wire.endTransmission() == 0) {
      Serial.print("✓ Encontrado en: 0x");
      if(i < 16) Serial.print("0");
      Serial.println(i, HEX);
      
      if(i == 0x40) {
        Serial.println("  → ¡Este es el HM3301!");
      }
      if(i == 0x62) {
        Serial.println("  → Este es el SCD40 (CO2)");
      }
      count++;
    }
  }
  
  if(count == 0) {
    Serial.println("❌ No se encontraron dispositivos I2C");
  }
}

void loop() {
  delay(10000);
}
```

**Resultado esperado:** 
```
✓ Encontrado en: 0x40 → ¡Este es el HM3301!
✓ Encontrado en: 0x62 → Este es el SCD40 (CO2)
```

---

## 💻 PROGRAMA DE PRUEBA

**Archivo:** `PROGRAMA_3_HM3301_PM25.ino`

```cpp
/*
 * CanSat Misión 2 - Prueba Sensor HM3301
 * Mide: PM1.0, PM2.5, PM10 (µg/m³)
 * 
 * Conexiones:
 *   SDA → A4 (blanco Grove)
 *   SCL → A5 (amarillo Grove)
 *   VCC → 3.3V (rojo Grove)
 *   GND → GND (negro Grove)
 */

#include <Wire.h>
#include <Seeed_HM330X.h>

HM330X sensor;
uint8_t buf[30];

// Variables para promedios
float pm1_sum = 0, pm25_sum = 0, pm10_sum = 0;
int lecturas = 0;
int contador = 0;

void setup() {
  Serial.begin(9600);
  delay(2000);
  
  Serial.println("╔═══════════════════════════════════════════╗");
  Serial.println("║  CanSat Misión 2 - Sensor HM3301 (PM2.5)  ║");
  Serial.println("║  Tecnología: Láser de dispersión          ║");
  Serial.println("╚═══════════════════════════════════════════╝");
  Serial.println();
  
  // Inicializar sensor
  Serial.print("Inicializando HM3301... ");
  if (sensor.init()) {
    Serial.println("❌ ERROR");
    Serial.println("Verifica conexiones:");
    Serial.println("  SDA (blanco) → A4");
    Serial.println("  SCL (amarillo) → A5");
    Serial.println("  VCC (rojo) → 3.3V");
    Serial.println("  GND (negro) → GND");
    while(1) delay(1000);
  }
  Serial.println("✓ OK");
  
  Serial.println();
  Serial.println("⏳ Estabilizando sensor (30 segundos recomendado)...");
  Serial.println("   Los primeros valores pueden ser inexactos.");
  Serial.println();
  
  delay(5000);  // Espera mínima
  
  // Cabecera de datos
  Serial.println("╔═══════╦═════════════╦═════════════╦═════════════╦════════════════╗");
  Serial.println("║   N°  ║ PM1.0(µg/m³)║ PM2.5(µg/m³)║ PM10(µg/m³) ║    Estado      ║");
  Serial.println("╠═══════╬═════════════╬═════════════╬═════════════╬════════════════╣");
}

void loop() {
  // Leer datos del sensor
  if (sensor.read_sensor_value(buf, 29)) {
    Serial.println("║ Error al leer sensor                                       ║");
    delay(1000);
    return;
  }
  
  // Extraer valores (índices según datasheet)
  // Usamos valores "atmospheric environment" (más precisos para exterior)
  uint16_t pm1 = (buf[10] << 8) | buf[11];   // PM1.0 AE
  uint16_t pm25 = (buf[12] << 8) | buf[13];  // PM2.5 AE
  uint16_t pm10 = (buf[14] << 8) | buf[15];  // PM10 AE
  
  // Clasificar calidad del aire por PM2.5
  String estado = clasificarPM25(pm25);
  
  // Mostrar datos en formato tabla
  Serial.print("║ ");
  imprimirNumero(contador, 4);
  Serial.print(" ║     ");
  imprimirNumero(pm1, 4);
  Serial.print("    ║     ");
  imprimirNumero(pm25, 4);
  Serial.print("    ║     ");
  imprimirNumero(pm10, 4);
  Serial.print("    ║ ");
  Serial.print(estado);
  for(int i = estado.length(); i < 14; i++) Serial.print(" ");
  Serial.println(" ║");
  
  // Acumular para estadísticas
  pm1_sum += pm1;
  pm25_sum += pm25;
  pm10_sum += pm10;
  lecturas++;
  
  // Mostrar estadísticas cada 10 lecturas
  if (lecturas >= 10) {
    Serial.println("╠═══════╩═════════════╩═════════════╩═════════════╩════════════════╣");
    Serial.print("║ PROMEDIO (10 lecturas): PM1.0=");
    Serial.print(pm1_sum/lecturas, 1);
    Serial.print(" | PM2.5=");
    Serial.print(pm25_sum/lecturas, 1);
    Serial.print(" | PM10=");
    Serial.print(pm10_sum/lecturas, 1);
    for(int i = 0; i < 5; i++) Serial.print(" ");
    Serial.println("║");
    Serial.println("╠═══════╦═════════════╦═════════════╦═════════════╦════════════════╣");
    
    // Resetear acumuladores
    pm1_sum = 0;
    pm25_sum = 0;
    pm10_sum = 0;
    lecturas = 0;
  }
  
  contador++;
  delay(1000);  // HM3301 actualiza cada ~1 segundo
}

// Función auxiliar para imprimir números con padding
void imprimirNumero(int num, int ancho) {
  int digitos = 1;
  int temp = num;
  while (temp >= 10) { digitos++; temp /= 10; }
  for (int i = 0; i < ancho - digitos; i++) Serial.print(" ");
  Serial.print(num);
}

// Función para clasificar calidad del aire por PM2.5 (estándar OMS/EPA)
String clasificarPM25(uint16_t pm25) {
  if (pm25 <= 12) return "🟢 Excelente";
  if (pm25 <= 35) return "🟢 Bueno";
  if (pm25 <= 55) return "🟡 Moderado";
  if (pm25 <= 150) return "🟠 Malo";
  if (pm25 <= 250) return "🔴 Muy malo";
  return "🔴 Peligroso";
}
```

---

## 📊 Interpretación de Valores

### PM2.5 - Partículas Finas (estándar OMS/EPA)

| PM2.5 (µg/m³) | Calidad | Situación típica |
|---------------|---------|------------------|
| 0-12 | 🟢 Excelente | Aire muy limpio (estándar OMS) |
| 12-35 | 🟢 Bueno | Zona urbana normal |
| 35-55 | 🟡 Moderado | Tráfico moderado |
| 55-150 | 🟠 Malo para sensibles | Tráfico intenso, industria |
| 150-250 | 🔴 Muy malo | Humo, incendio cercano |
| >250 | 🔴 Peligroso | Fuente directa de combustión |

### Relación entre PM1.0, PM2.5 y PM10

```
PM1.0 alto + PM2.5 alto + PM10 bajo   → Humo fino (combustión eficiente)
PM1.0 alto + PM2.5 alto + PM10 alto   → Combustión + polvo
PM1.0 bajo + PM2.5 bajo + PM10 alto   → Solo polvo (sin combustión)
PM1.0 bajo + PM2.5 bajo + PM10 bajo   → Aire limpio ✓
```

---

## 🔥 Firmas de Combustión Detectables

### Tráfico Vehicular 🚗
- PM2.5: 30-80 µg/m³
- Patrón: Incremento gradual en carreteras
- PM1.0/PM2.5 ratio: ~0.7-0.8

### Generadores Diésel 🚜
- PM2.5: >100 µg/m³
- Patrón: Picos pronunciados
- PM1.0/PM2.5 ratio: ~0.6-0.7

### Biomasa/Fuego 🔥
- PM2.5: >150 µg/m³
- Patrón: Muy elevado con fluctuaciones
- PM1.0/PM2.5 ratio: ~0.8-0.9 (humo fino)

### Zona Industrial 🏭
- PM2.5: 40-120 µg/m³
- Patrón: Fluctuaciones continuas
- PM10 también elevado

### Polvo (sin combustión) 🌫️
- PM2.5: 20-50 µg/m³
- PM10: >100 µg/m³
- PM1.0/PM2.5 ratio: bajo (<0.5)

---

## 🎯 Interpretación Combinada CO2 + PM2.5

**CLAVE PARA CANSAT:** La combinación de SCD40 (CO2) + HM3301 (PM2.5) permite identificar el TIPO de fuente:

| CO2 | PM2.5 | Interpretación |
|-----|-------|----------------|
| Alto (>600) | Alto (>55) | 🔥 Combustión activa |
| Alto (>600) | Bajo (<35) | 😤 Respiración/fermentación |
| Bajo (<500) | Alto (>55) | 🌫️ Polvo sin combustión |
| Bajo (<450) | Bajo (<12) | ✅ Aire limpio |

### Tabla de Fuentes Específicas

| Fuente | CO2 (ppm) | PM2.5 (µg/m³) | Firma |
|--------|-----------|---------------|-------|
| Aire limpio | 400-450 | 0-12 | Baseline |
| Tráfico ligero | 450-550 | 20-50 | ↑ gradual ambos |
| Tráfico intenso | 550-700 | 50-100 | ↑↑ ambos |
| Generador diésel | 600-900 | 100-200 | Picos PM2.5 |
| Incendio forestal | 700-1500 | 150-500 | ↑↑↑ ambos |
| Obra/construcción | 420-480 | 50-150 | Solo PM alto |

---

## ⚠️ Checklist Antes de Vuelo

```
☐ HM3301 conectado a A4 (SDA) y A5 (SCL)
☐ Voltaje 3.3V (o 5V) conectado
☐ GND conectado
☐ I2C scanner muestra 0x40
☐ Librería Seeed_HM330X instalada
☐ Programa carga sin errores
☐ Sensor estabilizado (~30 segundos)
☐ PM2.5 en aire limpio: <12 µg/m³
☐ Valores coherentes y estables
☐ Entrada de aire del sensor despejada
```

---

## 🚨 Troubleshooting

### Error: "No se encontró HM3301" / No aparece 0x40

```
1. Verificar conexión física:
   - SDA (blanco) → A4
   - SCL (amarillo) → A5
   - VCC (rojo) → 3.3V
   - GND (negro) → GND

2. Si usas Grove Shield:
   - Cable en puerto I2C correcto
   - Shield bien encajado

3. Ejecutar I2C Scanner
4. Presiona RESET doble
5. Recarga programa
```

### Valores siempre 0

```
1. Sensor necesita ~30 segundos de estabilización
2. Verificar que aire puede entrar al sensor
3. No tapar orificios del sensor
```

### Valores muy altos constantemente (>200)

```
1. ¿Hay humo o polvo cerca?
2. ¿Sensor sucio internamente?
3. Verificar que no hay cortocircuito
4. Probar en exterior con aire limpio
```

### Valores erráticos/inestables

```
1. Normal los primeros 30 segundos
2. Verificar alimentación estable
3. Alejarse de fuentes de vibración
4. El láser puede ser sensible a golpes
```

---

## 📝 Notas Importantes

```
✅ Tiempo de estabilización
   El HM3301 necesita ~30 segundos para lecturas precisas
   Los primeros valores pueden ser inexactos

✅ Usar valores "Atmospheric Environment"
   El sensor da dos tipos de valores:
   - Standard Particle (CF=1): para calibración
   - Atmospheric Environment (AE): para mediciones reales
   Usamos AE (índices 10-15 del buffer)

✅ No tapar orificios
   El sensor necesita flujo de aire constante
   No cubrir la entrada ni salida de aire

✅ Combinar con SCD40
   PM2.5 + CO2 = identificación precisa de fuentes
   Ver sección "Interpretación Combinada"

✅ Limpieza
   El láser puede ensuciarse con el tiempo
   En ambientes muy polvorientos, limpiar periódicamente
```

---

## 🔗 Referencias

- Datasheet HM3301: https://wiki.seeedstudio.com/Grove-Laser_PM2.5_Sensor-HM3301/
- Librería Arduino: https://github.com/Seeed-Studio/Seeed_PM2_5_sensor_HM3301
- Estándares PM2.5 OMS: https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health
- Índice AQI EPA: https://www.airnow.gov/aqi/aqi-basics/

---

## 🎯 Próximo Paso

**Documento 4:** GPS ATGM336H - Posicionamiento

Archivo: `DOCUMENTO_4_SENSOR_GPS_POSICION.md`

---

**Estado:** ✅ HM3301 - Sensor PM2.5 láser  
**Última actualización:** Febrero 2026
