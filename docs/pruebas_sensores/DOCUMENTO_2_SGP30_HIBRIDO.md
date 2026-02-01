# 📋 DOCUMENTO 2: SENSOR SGP30 - DETECCIÓN DE GASES

## Objetivo
Integrar sensor SGP30 (TVOC + eCO2) para detectar contaminación aérea.

---

## 📡 SGP30 - Especificaciones

```
Voltaje: 3.3V (⚠️ NUNCA 5V)
Protocolo: I2C
Dirección: 0x58
Función: TVOC (ppb) + eCO2 (ppm) + H2 (raw) + Ethanol (raw)
```

---

## 🔌 Conexión Física

**¡¡CRÍTICO!!** SGP30 es **SOLO 3.3V**. Si usas 5V → **SE DAÑA PERMANENTEMENTE**

```
Arduino Nano 33 BLE:

A4 (SDA)  ──→ SGP30 SDA
A5 (SCL)  ──→ SGP30 SCL
GND       ──→ SGP30 GND
3.3V      ──→ SGP30 VCC (⚠️ NUNCA 5V)
```

**Verifica con multímetro:** VCC debe mostrar exactamente 3.3V

---

## 📥 Instalación Librería

```
Sketch → Include Library → Manage Libraries

Busca: "Adafruit SGP30"
Instala: Adafruit SGP30 by Adafruit (última versión)

Reinicia Arduino IDE
```

---

## ✅ Verificación Previa

Antes de cargar el programa, verifica que SGP30 responde en I2C:

```cpp
#include <Wire.h>

void setup() {
  Serial.begin(9600);
  delay(2000);
  
  Serial.println("Buscando SGP30 en I2C...");
  
  byte count = 0;
  for(byte i = 8; i < 120; i++) {
    Wire.beginTransmission(i);
    if(Wire.endTransmission() == 0) {
      Serial.print("✓ Encontrado en: 0x");
      if(i < 16) Serial.print("0");
      Serial.println(i, HEX);
      count++;
    }
  }
  
  if(count == 0) {
    Serial.println("❌ No encontrado");
  }
}

void loop() {
  delay(10000);
}
```

**Resultado esperado:** `✓ Encontrado en: 0x58`

---

## 💻 CÓDIGO ASOCIADO

**Archivo:** `PROGRAMA_2_SGP30_GASES.ino`

### Pasos:
1. Descarga `PROGRAMA_2_SGP30_GASES.ino`
2. Verifica conexión física (A4/A5/GND/3.3V)
3. Carga en Arduino
4. Abre Monitor Serial (9600 baud)
5. Espera 15 segundos de calibración

---

## 📊 Interpretación de Valores

### TVOC (Compuestos Orgánicos Volátiles)

```
0-220 ppb      🟢 Aire limpio (excelente)
220-660 ppb    🟡 Buena calidad (aceptable)
660-2200 ppb   🟠 Moderada (ventilación recomendada)
2200-5500 ppb  🔴 Mala (fuente cercana)
>5500 ppb      🔴 Muy mala (peligroso)
```

### eCO2 (CO2 Equivalente)

```
400 ppm        🟢 Normal (aire exterior)
400-1000 ppm   🟡 Aceptable (interior ventilado)
>1000 ppm      🟠 Malo (necesita ventilación)
>2000 ppm      🔴 Muy malo (peligroso)
```

---

## 🔍 Firmas de Combustión Detectables

### Tráfico Vehicular 🚗
- TVOC: 300-800 ppb
- H2 raw: Elevado
- Patrón: Incremento gradual en carreteras

### Generadores Diésel 🚜
- TVOC: >1000 ppb
- eCO2: >1500 ppm
- Patrón: Picos pronunciados

### Biomasa/Fuego 🔥
- TVOC: >500 ppb
- Ethanol raw: Alto
- Patrón: Zona forestal con humo

### Zona Industrial 🏭
- TVOC: Variable/Inestable
- eCO2: Moderado-alto
- Patrón: Fluctuaciones continuas

---

## ⚠️ Checklist Antes de Vuelo

```
☐ SGP30 conectado a A4/A5
☐ Voltaje 3.3V (verificado con multímetro)
☐ GND conectado
☐ I2C scanner muestra 0x58
☐ Programa carga sin errores
☐ Valores estables después de 15 segundos
☐ TVOC y eCO2 dentro de rangos normales
☐ NO hay "❌ Error en medición"
```

---

## 🚨 Troubleshooting

### Error: "No se encontró SGP30"

```
1. Verifica conexión física:
   - A4 conectado a SDA
   - A5 conectado a SCL
   - 3.3V (NO 5V) conectado
   - GND conectado

2. Presiona RESET doble
3. Recarga programa
4. Espera 15 segundos
```

### Valores siempre 0 o raros

```
1. SGP30 necesita TIEMPO
   - Espera 30 segundos al iniciar
   - Los valores cambian lentamente

2. Verifica que esté midiendo:
   - Acerca un trapo húmedo
   - Debe cambiar TVOC
```

---

## 📝 Notas Importantes

```
✅ SGP30 DEBE estar a 3.3V
   Si lo conectas a 5V → se daña PERMANENTEMENTE

✅ Necesita "warmup"
   Los primeros 15 segundos son calibración
   No confíes en valores antes de ese tiempo

✅ TVOC + eCO2 son relativos
   Sirven para detectar CAMBIOS
   No para medir valores absolutos precisos

✅ H2 y Ethanol (raw)
   Son datos sin procesar
   Útiles para identificar TIPO de contaminación
```

---

## 🎯 Próximo Paso

**Documento 3:** Integración GPS

Archivo: `PROGRAMA_3_GPS_POSICION.ino`

---

**Estado:** ✅ SGP30 funcionando  
**Última actualización:** Enero 2026
