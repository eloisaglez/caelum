# 📋 DOCUMENTO 1: PUESTA EN MARCHA ARDUINO NANO 33 BLE SENSE

## Objetivo
Verificar que Arduino Nano 33 BLE Sense funciona correctamente con sus sensores integrados.

---

## 🎯 Sensores Integrados

| Sensor | Modelo | Función | Estado |
|--------|--------|---------|--------|
| **Acelerómetro + Giroscopio** | BMI270 | Movimiento + Rotación | ✅ |
| **Magnetómetro** | BMM150 | Brújula/Orientación | ✅ |
| **Presión + Temperatura** | LPS22HB | Altitud + Temp compensación | ✅ |
| **Temperatura + Humedad** | HS3003 | Temp REAL + Humedad | ✅ |
| **Luz/Color/Proximidad** | APDS9960 | Luz ambiente | ✅ |

---

## 📥 Instalación de Librerías

En Arduino IDE:

```
Sketch → Include Library → Manage Libraries

✅ Instala:
   - Arduino_BMI270_BMM150
   - Arduino_HS300x
   - ReefwingLPS22HB
   - Arduino_APDS9960
```

**Reinicia Arduino IDE después de instalar.**

---

## ⚙️ Configuración Arduino IDE

```
Tools → Board: "Arduino Nano 33 BLE"
Tools → Port: Selecciona COM
Tools → Upload Speed: 115200
Tools → Processor: nRF52840 (SENSE - 256KB)
```

---

## 💻 CÓDIGO ASOCIADO

**Archivo:** `PROGRAMA_1_SENSORES_INTEGRADOS.ino`

### Pasos:
1. Descarga el archivo `.ino`
2. Abre en Arduino IDE
3. Verifica conexiones
4. Carga en placa (`Ctrl+U`)
5. Abre Monitor Serial (9600 baud)

---

## ✅ Verificación de Funcionamiento

Al cargar el programa, deberías ver:

```
╔════════════════════════════════════════╗
║  Arduino Nano 33 BLE - Sensores Test   ║
╚════════════════════════════════════════╝

IMU (BMI270+BMM150)... ✓ OK
HS3003 (Temp+Humedad)... ✓ OK
LPS22HB (Presión)... ✓ OK

═══════════════════════════════════════════
Sistema listo. Leyendo sensores...

N° | Temp(HS) | Humedad | Presion | Altitud | AccelZ | GyroX
───┼──────────┼─────────┼─────────┼─────────┼────────┼────────
0 | 23.5°C    | 65.2%   | 929.5 hPa | 620.1m | 1.00   | 0.2
1 | 23.5°C    | 65.1%   | 929.5 hPa | 620.0m | 1.00   | 0.1
```

---

## 📊 Datos Esperados

### Temperatura HS3003
- Rango: 0-50°C
- Precisión: ±2°C
- ⚠️ MÁS real que LPS22HB, pero tiene error ±2-3°C
- ⚠️ Influencia del calor del chip
- Típico: lee 20-25°C, realidad: ~15-20°C

### Humedad
- Rango: 0-100%
- Precisión: ±3%

### Presión
- Rango: 300-1100 hPa
- Típico: ~930 hPa (Madrid)

### Altitud (calculada)
- Precisión: ±10-20m
- Se calcula de presión

---

## ⚠️ Problemas Comunes

### No aparece puerto COM
```
✅ Solución:
  1. Instalar driver (si es necesario)
  2. Cambiar puerto USB (trasero de PC)
  3. Reiniciar Arduino IDE
```

### Sensores no responden
```
✅ Solución:
  1. Verificar Board: "Arduino Nano 33 BLE"
  2. Verificar librerías instaladas
  3. Presionar RESET doble
  4. Recargar programa
```

### Monitor Serial en blanco
```
✅ Solución:
  1. Cerrar Monitor Serial
  2. Presionar RESET doble
  3. Cargar programa
  4. Abrir Monitor Serial
  5. Presionar RESET una vez
```

---

## 🎯 Próximo Paso

**Documento 2:** Agregar sensor SCD40 (CO2)

Archivo: `PROGRAMA_2_SCD40.ino`

---

**Estado:** ✅ Arduino Nano 33 BLE funcionando  
**Última actualización:** Febrero 2026
**Versión:** Actualizada según pruebas reales
