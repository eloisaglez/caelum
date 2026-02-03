# ÍNDICE DE DOCUMENTACIÓN

## EMPIEZA AQUÍ

**[ÍNDICE DE PRUEBAS FINAL](./INDICE_DE_PRUEBAS_FINAL.md)** - Guía paso a paso

---

## DOCUMENTOS TÉCNICOS (por orden de uso)

### 1. SENSORES INTEGRADOS
**Archivo:** `DOCUMENTO_1_SENSORES_INTEGRADOS_PLACA.md`
- Qué sensores incluye Arduino Nano 33 BLE Sense
- Cómo funcionan
- Precisión de cada uno
- **Programa asociado:** `PROGRAMA_1_SENSORES_INTEGRADOS.ino`

### 2. SENSOR SGP30 (GASES)
**Archivo:** `DOCUMENTO_2_SGP30.md`
- Qué es SGP30
- Cómo conectar (⚠️ 3.3V crítico)
- Interpretación TVOC/eCO2
- Firmas de combustión
- **Programa asociado:** `PROGRAMA_2_SGP30_GASES.ino`

### 3. GPS (POSICIÓN)
**Archivo:** `DOCUMENTO_3_SENSOR_GPS_POSICION.md`
- Cómo funciona GPS
- Cómo conectar
- Tiempos obtención señal
- **Programa asociado:** `PROGRAMA_3_GPS_POSICION.ino`

### 4. MICROSD (GRABACIÓN)
**Archivo:** `DOCUMENTO_4_MICROSD_GRABACION.md`
- Cómo funciona MicroSD (SPI)
- Cómo conectar (⚠️ 3.3V crítico)
- Formato CSV
- **Programa asociado:** `PROGRAMA_4_MICROSD_GRABACION.ino`

### 5. APC220 (TELEMETRÍA RF)
**Archivo:** `DOCUMENTO_5_APC220_TELEMETRIA.md`
- Cómo funciona APC220
- Configuración con Arduino UNO
- Conexiones (⚠️ directas, no cruzadas)
- **Programas asociados:** 
  - `PROGRAMA_APC220_CONFIGURADOR.ino`
  - `PROGRAMA_APC220_EMISOR.ino`
  - `PROGRAMA_APC220_RECEPTOR.ino`

---

## DOCUMENTOS IMPORTANTES

### Cambio de Frecuencia (Concurso)
**Archivo:** `IMPORTANTE_CAMBIO_FRECUENCIA.md`
- Recordatorio para cambiar frecuencia antes del concurso
- Pasos para reconfigurar los APC220
- Checklist pre-competición

### Temperatura (Aclaraciones)
**Archivo:** `ACLARACIONES_SENSORES_TEMPERATURA.md`
- Verdad sobre HS3003
- Comparativa sensores
- Opción DHT22

---

## TROUBLESHOOTING

**Archivo:** `TROUBLESHOOTING_COMPLETO.md`

15+ problemas comunes y soluciones:
- Arduino no se reconoce
- Puerto COM no aparece
- Sensores no responden
- GPS sin señal
- MicroSD no graba
- APC220 no comunica
- Y muchos más...

---

## PROGRAMAS ARDUINO

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

PROGRAMA_APC220_CONFIGURADOR.ino
  → Configura APC220 con Arduino UNO
  → ~10 minutos

PROGRAMA_APC220_EMISOR.ino
  → Emisor para Nano 33 BLE (usa Serial1)
  → Prueba de comunicación

PROGRAMA_APC220_RECEPTOR.ino
  → Receptor para Arduino UNO
  → Estación tierra

PROGRAMA_FINAL_CANSAT_TELEMETRIA.ino
  → TODOS los sensores + telemetría
  → LISTO PARA VUELO
```

---

## CÓMO USAR

### Opción 1: Principiante
1. Lee INDICE_DE_PRUEBAS_FINAL.md
2. Sigue documento → programa → verificar
3. Consulta TROUBLESHOOTING si falla

### Opción 2: Experimentado
1. Revisa INDICE_DE_PRUEBAS_FINAL.md
2. Carga PROGRAMA_FINAL_CANSAT_TELEMETRIA.ino
3. Consulta documentos específicos

### Opción 3: Problema
1. Abre TROUBLESHOOTING_COMPLETO.md
2. Busca tu síntoma
3. Sigue soluciones

---

## CHECKLIST DE ARCHIVOS

```
DOCUMENTOS (.md):
  ☑ INDEX.md
  ☑ INDICE_DE_PRUEBAS_FINAL.md
  ☑ DOCUMENTO_1_SENSORES_INTEGRADOS_PLACA.md
  ☑ DOCUMENTO_2_SGP30.md
  ☑ DOCUMENTO_3_SENSOR_GPS_POSICION.md
  ☑ DOCUMENTO_4_MICROSD_GRABACION.md
  ☑ DOCUMENTO_5_APC220_TELEMETRIA.md
  ☑ IMPORTANTE_CAMBIO_FRECUENCIA.md
  ☑ TROUBLESHOOTING_COMPLETO.md
  ☑ ACLARACIONES_SENSORES_TEMPERATURA.md

PROGRAMAS (.ino):
  ☑ PROGRAMA_1_SENSORES_INTEGRADOS.ino
  ☑ PROGRAMA_2_SGP30_GASES.ino
  ☑ PROGRAMA_3_GPS_POSICION.ino
  ☑ PROGRAMA_4_MICROSD_GRABACION.ino
  ☑ PROGRAMA_APC220_CONFIGURADOR.ino
  ☑ PROGRAMA_APC220_EMISOR.ino
  ☑ PROGRAMA_APC220_RECEPTOR.ino
  ☑ PROGRAMA_FINAL_CANSAT_TELEMETRIA.ino
```

---

## RECOMENDADO PARA BRUNETE

1. **Antes de viajar:**
   - Leer INDICE_DE_PRUEBAS_FINAL.md
   - Probar cada PROGRAMA_X.ino
   - Resolver problemas con TROUBLESHOOTING
   - Leer IMPORTANTE_CAMBIO_FRECUENCIA.md

2. **Día de competencia:**
   - Cambiar frecuencia APC220 según organización
   - Cargar PROGRAMA_FINAL_CANSAT_TELEMETRIA.ino
   - Verificar sensores funcionando
   - ¡A volar!

---

## AYUDA RÁPIDA

| Problema | Ver |
|----------|-----|
| Arduino no se reconoce | TROUBLESHOOTING #1 |
| Sensor no inicializa | TROUBLESHOOTING #9 |
| SGP30 no responde | TROUBLESHOOTING #12 |
| GPS sin satélites | TROUBLESHOOTING #13 |
| MicroSD no graba | TROUBLESHOOTING #14 |
| APC220 no comunica | TROUBLESHOOTING #15 |

---

**¡Listo para empezar!**

**Estado:** Documentación completa  
**Última actualización:** Febrero 2026
