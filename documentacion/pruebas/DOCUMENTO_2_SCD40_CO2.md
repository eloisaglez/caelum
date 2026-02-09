# 📋 DOCUMENTO 2: SENSOR SCD40 - MEDICIÓN DE CO2

## Objetivo
Integrar sensor SCD40 para medir CO2 real mediante tecnología NDIR.

---

## 📡 Especificaciones

| Característica | Valor |
|----------------|-------|
| Fabricante | Sensirion |
| Voltaje | 2.4V - 5.5V (usar 3.3V) |
| Protocolo | I2C |
| Dirección | 0x62 |
| Rango CO2 | 400 - 5000 ppm |
| Precisión | ±(50 ppm + 5%) |
| Tiempo respuesta | 5 segundos |
| Bonus | También mide Temperatura y Humedad |

---

## 🔌 Conexión Física

```
Arduino Nano 33 BLE    SCD40
───────────────────────────────
A4 (SDA)           →   SDA
A5 (SCL)           →   SCL
3.3V               →   VCC
GND                →   GND
```

---

## 📥 Instalación Librería

```
Sketch → Include Library → Manage Libraries

Buscar: "Sensirion I2C SCD4x"
Instalar: Sensirion I2C SCD4x by Sensirion

También instalar:
Buscar: "Sensirion Core"
Instalar: Sensirion Core by Sensirion
```

---

## ✅ Verificación I2C

**Programa:** `software/pruebas/PROGRAMA_I2C_SCANNER.ino`

**Resultado esperado:** `✓ Encontrado en: 0x62`

---

## 💻 Programa de Prueba

**Archivo:** `software/pruebas/PROGRAMA_2_SCD40_CO2.ino`

### Pasos:
1. Abre el programa en Arduino IDE
2. Tools → Board → Arduino Nano 33 BLE
3. Ctrl+U para cargar
4. Abre Monitor Serial (9600 baud)
5. Espera 5 segundos para primera lectura

---

## ⚠️ Checklist

```
☐ SCD40 conectado a A4/A5
☐ Voltaje 3.3V verificado
☐ I2C scanner muestra 0x62
☐ Librería instalada
☐ Primera lectura tras 5 segundos
☐ CO2 exterior: ~400-450 ppm (normal)
```

---

## 🚨 Troubleshooting

| Problema | Solución |
|----------|----------|
| No aparece 0x62 | Verificar cables A4/A5, verificar 3.3V |
| CO2 = 0 | Esperar 5 segundos, verificar startPeriodicMeasurement() |
| CO2 siempre ~400 ppm | Normal en exterior. Probar: respirar cerca del sensor |

---

## 📝 Notas

- Primera medición tarda **5 segundos**
- En exterior limpio: **400-450 ppm** es normal
- Para probar: respira cerca → debe subir a 800-1500 ppm

---

**Siguiente:** DOCUMENTO_3_HM3301_PM25.md
