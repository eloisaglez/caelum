# 📖 ÍNDICE DE DOCUMENTACIÓN

## 🚀 EMPIEZA AQUÍ

👉 **[ÍNDICE DE PRUEBAS FINAL](./INDICE_DE_PRUEBAS_FINAL.md)** - Guía paso a paso

---

## 📚 DOCUMENTOS TÉCNICOS (por orden de uso)

### 1️⃣ SENSORES INTEGRADOS
**Archivo:** `DOCUMENTO_1_SENSORES_INTEGRADOS_HIBRIDO.md`
- Qué sensores incluye Arduino
- Cómo funcionan
- Precisión de cada uno
- **Programa asociado:** `PROGRAMA_1_SENSORES_INTEGRADOS.ino`

### 2️⃣ SENSOR SGP30 (GASES)
**Archivo:** `DOCUMENTO_2_SGP30_HIBRIDO.md`
- Qué es SGP30
- Cómo conectar (⚠️ 3.3V crítico)
- Interpretación TVOC/eCO2
- Firmas de combustión
- **Programa asociado:** `PROGRAMA_2_SGP30_GASES.ino`

### 3️⃣ GPS (POSICIÓN)
**Archivo:** `DOCUMENTO_3_SENSOR_GPS_POSICION.md`
- Cómo funciona GPS
- Cómo conectar (SoftwareSerial)
- Tiempos obtención señal
- **Programa asociado:** `PROGRAMA_3_GPS_POSICION.ino`

### 4️⃣ MICROSD (GRABACIÓN)
**Archivo:** `DOCUMENTO_4_MICROSD_GRABACION.md`
- Cómo funciona MicroSD (SPI)
- Cómo conectar (⚠️ 3.3V crítico)
- Formato CSV
- **Programa asociado:** `PROGRAMA_4_MICROSD_GRABACION.ino`

### 5️⃣ APC220 (TELEMETRÍA RF)
**Archivo:** `DOCUMENTO_5_APC220_TELEMETRIA_ACTUALIZADO.md`
- Cómo funciona APC220
- Configuración crítica
- Cómo conectar
- **Programa asociado:** `PROGRAMA_CONFIGURACION_APC220.ino` y `PROGRAMA_FINAL_CANSAT_MISION2.ino`

---

## 🔧 GUÍAS ESPECIALIZADAS

### Configuración APC220
**Opción A - rápida:** `GUIA_RAPIDA_CONFIGURACION_APC220.md`
**Opción B - Arduino:** `GUIA_PROGRAMA_CONFIGURACION_APC220.md`

### Temperatura (Aclaraciones)
**Archivo:** `ACLARACIONES_SENSORES_TEMPERATURA.md`
- Verdad sobre HS3003
- Comparativa sensores
- Opción DHT22

---

## 🚨 TROUBLESHOOTING

**Archivo:** `TROUBLESHOOTING_COMPLETO.md`

15+ problemas comunes y soluciones:
- Arduino no se reconoce
- Puerto COM no aparece
- Sensores no responden
- GPS sin señal
- MicroSD no graba
- Y muchos más...

---

## 🚀 PROGRAMAS ARDUINO

```
PROGRAMA_1_SENSORES_INTEGRADOS.ino
  → Prueba sensores integrados
  → ~20 minutos

PROGRAMA_2_SGP30_GASES.ino
  → Prueba SGP30
  → ~30 minutos

PROGRAMA_3_GPS_POSICION.ino
  → Prueba GPS
  → ~30 minutos (esperando señal)

PROGRAMA_4_MICROSD_GRABACION.ino
  → Prueba MicroSD
  → ~20 minutos

PROGRAMA_CONFIGURACION_APC220.ino
  → Configura APC220 desde Arduino
  → ~10 minutos

PROGRAMA_FINAL_CANSAT_MISION2.ino
  → TODOS los sensores integrados
  → LISTO PARA VUELO
```

---

## 📋 CÓMO USAR

### Opción 1: Principiante
1. Lee ÍNDICE_DE_PRUEBAS_FINAL.md
2. Sigue documento → programa → verificar
3. Consulta TROUBLESHOOTING si falla

### Opción 2: Experimentado
1. Revisa ÍNDICE_DE_PRUEBAS_FINAL.md
2. Carga PROGRAMA_FINAL_CANSAT_MISION2.ino
3. Consulta documentos específicos

### Opción 3: Problema
1. Abre TROUBLESHOOTING_COMPLETO.md
2. Busca tu síntoma
3. Sigue soluciones

---

## ✅ CHECKLIST DE ARCHIVOS

```
DOCUMENTOS (.md):
  ☑ INDICE_DE_PRUEBAS_FINAL.md
  ☑ DOCUMENTO_1_SENSORES_INTEGRADOS_HIBRIDO.md
  ☑ DOCUMENTO_2_SGP30_HIBRIDO.md
  ☑ DOCUMENTO_3_SENSOR_GPS_POSICION.md
  ☑ DOCUMENTO_4_MICROSD_GRABACION.md
  ☑ DOCUMENTO_5_APC220_TELEMETRIA_ACTUALIZADO.md
  ☑ GUIA_RAPIDA_CONFIGURACION_APC220.md
  ☑ GUIA_PROGRAMA_CONFIGURACION_APC220.md
  ☑ TROUBLESHOOTING_COMPLETO.md
  ☑ ACLARACIONES_SENSORES_TEMPERATURA.md

PROGRAMAS (.ino):
  ☑ PROGRAMA_1_SENSORES_INTEGRADOS.ino
  ☑ PROGRAMA_2_SGP30_GASES.ino
  ☑ PROGRAMA_3_GPS_POSICION.ino
  ☑ PROGRAMA_4_MICROSD_GRABACION.ino
  ☑ PROGRAMA_CONFIGURACION_APC220.ino
  ☑ PROGRAMA_FINAL_CANSAT_MISION2.ino
```

---

## 🎯 RECOMENDADO PARA BRUNETE

1. **Antes de viajar:**
   - Leer ÍNDICE_DE_PRUEBAS_FINAL.md
   - Probar cada PROGRAMA_X.ino
   - Resolver problemas en TROUBLESHOOTING

2. **Día de competencia:**
   - Cargar PROGRAMA_FINAL_CANSAT_MISION2.ino
   - Verificar sensores funcionando
   - ¡A volar!

---

## 📞 AYUDA RÁPIDA

| Problema | Ver |
|----------|-----|
| Arduino no se reconoce | TROUBLESHOOTING #1 |
| Sensor no inicializa | TROUBLESHOOTING #9 |
| SGP30 no responde | TROUBLESHOOTING #12 |
| GPS sin satélites | TROUBLESHOOTING #13 |
| MicroSD no graba | TROUBLESHOOTING #14 |
| APC220 no comunica | TROUBLESHOOTING #15 |

---

**¡Listo para empezar!** 🚀

**Estado:** ✅ Documentación completa  
**Última actualización:** Enero 2026
