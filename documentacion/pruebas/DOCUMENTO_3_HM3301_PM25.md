# 📋 DOCUMENTO 3: SENSOR HM3301 - PARTÍCULAS PM2.5

## Objetivo
Integrar sensor HM3301 para medir partículas en suspensión (PM1.0, PM2.5, PM10) mediante tecnología láser.

---

## 📡 Especificaciones

| Característica | Valor |
|----------------|-------|
| Fabricante | Seeed Studio |
| Voltaje | 3.3V - 5V |
| Protocolo | I2C |
| Dirección | 0x40 |
| Rango | 0 - 1000 µg/m³ |
| Mediciones | PM1.0, PM2.5, PM10 |
| Tiempo estabilización | ~30 segundos |

---

## 🔌 Conexión Física

```
Arduino Nano 33 BLE    HM3301 (Grove)
───────────────────────────────────────
A4 (SDA)           →   SDA (blanco)
A5 (SCL)           →   SCL (amarillo)
3.3V               →   VCC (rojo)
GND                →   GND (negro)
```

---

## 📥 Instalación Librería

```
Sketch → Include Library → Manage Libraries

Buscar: "Seeed HM330X" o "Grove Laser PM2.5"
Instalar: Grove - Laser PM2.5 Sensor HM3301
```

---

## ✅ Verificación I2C

**Programa:** `software/pruebas/I2C_scanner_HM3301.ino`

**Resultado esperado:** `✓ Encontrado en: 0x40`

---

## 💻 Programa de Prueba

**Archivo:** `software/pruebas/PROGRAMA_3_HM3301_PM25.ino`

### Pasos:
1. Abre el programa en Arduino IDE
2. Tools → Board → Arduino Nano 33 BLE
3. Ctrl+U para cargar
4. Abre Monitor Serial (9600 baud)
5. Espera ~30 segundos para estabilización

---

## ⚠️ Checklist

```
☐ HM3301 conectado a A4/A5
☐ Voltaje 3.3V conectado
☐ I2C scanner muestra 0x40
☐ Librería instalada
☐ Sensor estabilizado (~30 seg)
☐ PM2.5 aire limpio: <12 µg/m³
☐ Entrada de aire despejada
```

---

## 🚨 Troubleshooting

| Problema | Solución |
|----------|----------|
| No aparece 0x40 | Verificar cables Grove (colores), verificar voltaje |
| Valores = 0 | Normal en aire muy limpio. Probar: acercar humo de incienso |
| Valores erráticos | Esperar 30 segundos de estabilización |

---

## 📝 Notas

- Estabilización tarda **~30 segundos**
- En aire limpio: **<12 µg/m³** es normal
- Para probar: acerca humo → debe subir significativamente
- No bloquear orificios de entrada de aire

---

**Siguiente:** DOCUMENTO_4_GPS.md
