# 🛰️ CANSAT MISIÓN 2 - ÍNDICE MAESTRO
## Estructura Híbrida: Documentos + Programas

**Fecha:** Enero 2026  
**Proyecto:** Detección de Firmas de Combustión  
**Centro:** IES Diego Velázquez  
**Estado:** ✅ Listo para Brunete 2026

---

## 📚 CÓMO USAR ESTA DOCUMENTACIÓN

```
ESTRUCTURA HÍBRIDA:

📄 Documentos (.md)          → EXPLICACIÓN CONCEPTUAL
    ├─ Teoría
    ├─ Conexiones físicas
    ├─ Troubleshooting
    └─ ⚠️ REFERENCIA AL ARCHIVO .ino

📝 Programas (.ino)          → CÓDIGO LISTO PARA CARGAR
    ├─ Código completo
    ├─ Comentarios técnicos
    ├─ Fácil de copiar
    └─ ✅ LISTO PARA USAR
```

---

## 🗺️ MAPA DE DOCUMENTACIÓN

### ETAPA 1: SENSORES INTEGRADOS

**Documento:** `DOCUMENTO_1_SENSORES_INTEGRADOS_HIBRIDO.md`  
**Código:** `PROGRAMA_1_SENSORES_INTEGRADOS.ino`

```
✅ Temperatura HS3003 + Humedad
✅ Presión LPS22HB + Altitud
✅ Acelerómetro BMI270
✅ Giroscopio BMI270
✅ Magnetómetro BMM150
✅ Luz APDS9960 (incluido)

Tiempo: ~15 minutos
Dificultad: ⭐ Muy fácil
```

---

### ETAPA 2: SENSOR SGP30

**Documento:** `DOCUMENTO_2_SGP30_HIBRIDO.md`  
**Código:** `PROGRAMA_2_SGP30_GASES.ino`

```
✅ Medición TVOC (ppb)
✅ Medición eCO2 (ppm)
✅ Datos H2 raw (identificación)
✅ Datos Ethanol raw (identificación)

Tiempo: ~20 minutos
Dificultad: ⭐⭐ Fácil
Crítico: ⚠️ 3.3V SOLAMENTE
```

---

### ETAPA 3: GPS

**Documento:** `DOCUMENTO_3_SENSOR_GPS_POSICION.md`  
**Código:** `PROGRAMA_3_GPS_POSICION.ino`

```
✅ Latitud + Longitud
✅ Altitud GPS
✅ Número de satélites
✅ Precisión posición

Tiempo: ~30 minutos (espera GPS)
Dificultad: ⭐⭐ Fácil
Crítico: ⚠️ Necesita EXTERIOR
```

---

### ETAPA 4: MICROSD

**Documento:** `DOCUMENTO_4_MICROSD_GRABACION.md`  
**Código:** `PROGRAMA_4_MICROSD_GRABACION.ino`

```
✅ Grabación en CSV
✅ Almacenamiento local
✅ Backup automático
✅ Formato para análisis

Tiempo: ~20 minutos
Dificultad: ⭐⭐ Fácil
Crítico: ⚠️ 3.3V SOLAMENTE
```

---

### ETAPA 5: APC220 (Opcional)

**Documento:** `DOCUMENTO_5_APC220_TELEMETRIA.md`  
**Código:** `PROGRAMA_5_APC220_TELEMETRIA.ino`

```
✅ Telemetría RF
✅ Datos en tiempo real
✅ Comunicación Serial1
✅ Alcance 100-500m

Tiempo: ~25 minutos
Dificultad: ⭐⭐⭐ Moderada
Crítico: ⚠️ Necesita receptor
```

---

### ETAPA 6: FIREBASE & WEB

**Documento:** `DOCUMENTO_6_FIREBASE_WEB.md`  
**Scripts:** `enviar_a_firebase.py` + HTML

```
✅ Almacenamiento en nube
✅ Página web interactiva
✅ Mapa de calor
✅ Google Earth 3D

Tiempo: ~40 minutos
Dificultad: ⭐⭐⭐⭐ Avanzada
Crítico: ⚠️ Requiere cuenta Firebase
```

---

### PROGRAMA FINAL INTEGRADO

**Código:** `PROGRAMA_FINAL_CANSAT_MISION2.ino`

```
✅ TODOS LOS SENSORES
✅ MicroSD grabación
✅ GPS posición
✅ SGP30 gases
✅ APC220 telemetría
✅ Sensores integrados

Tiempo: Listo para vuelo
Dificultad: ⭐⭐⭐⭐⭐ Completo
Estado: ✅ FUNCIONANDO
```

---

## 📖 GUÍA DE LECTURA RECOMENDADA

### Opción A: PRINCIPIANTES (Sin experiencia Arduino)

```
1. Lee: DOCUMENTO_1 (conceptos básicos)
   Carga: PROGRAMA_1 (verifica que funciona)
   
2. Lee: DOCUMENTO_2 (SGP30)
   Carga: PROGRAMA_2 (entiende gases)
   
3. Lee: DOCUMENTO_3 (GPS)
   Carga: PROGRAMA_3 (obtén posición)
   
4. Lee: DOCUMENTO_4 (MicroSD)
   Carga: PROGRAMA_4 (graba datos)
   
5. Lee: ACLARACIONES (temperatura)
   Opción: Agrega DHT22 si quieres precisión
```

**Tiempo total:** ~2-3 horas  
**Resultado:** Sistema funcionando

---

### Opción B: EXPERIMENTADOS (Conoces Arduino)

```
1. Revisa DOCUMENTO_1 (verificación rápida)
   Carga PROGRAMA_1 (confirma sensores)

2. Carga PROGRAMA_2, 3, 4 secuencialmente
   Lee documentos según necesites

3. Carga PROGRAMA_FINAL_CANSAT
   Sistema listo para vuelo
```

**Tiempo total:** ~1 hora  
**Resultado:** Sistema optimizado

---

### Opción C: COMPETENCIA (Necesitas TODO ya)

```
1. Usa PROGRAMA_FINAL_CANSAT_MISION2.ino
   
2. Consulta documentos según errores

3. Sigue CHECKLIST_PRE_VUELO.md

4. ¡A volar!
```

**Tiempo total:** ~30 minutos  
**Resultado:** Listo para Brunete

---

## 🗂️ ESTRUCTURA DE CARPETAS RECOMENDADA

```
cansat-mision2/
│
├── 📚 DOCUMENTOS/
│   ├── DOCUMENTO_1_SENSORES_INTEGRADOS_HIBRIDO.md
│   ├── DOCUMENTO_2_SGP30_HIBRIDO.md
│   ├── DOCUMENTO_3_SENSOR_GPS_POSICION.md
│   ├── DOCUMENTO_4_MICROSD_GRABACION.md
│   ├── DOCUMENTO_5_APC220_TELEMETRIA.md
│   ├── DOCUMENTO_6_FIREBASE_WEB.md
│   ├── ACLARACIONES_SENSORES_TEMPERATURA.md
│   ├── CHECKLIST_PRE_VUELO.md
│   └── README_ACTUALIZADO.md
│
├── 📝 PROGRAMAS/
│   ├── PROGRAMA_1_SENSORES_INTEGRADOS.ino
│   ├── PROGRAMA_2_SGP30_GASES.ino
│   ├── PROGRAMA_3_GPS_POSICION.ino
│   ├── PROGRAMA_4_MICROSD_GRABACION.ino
│   ├── PROGRAMA_5_APC220_TELEMETRIA.ino
│   └── PROGRAMA_FINAL_CANSAT_MISION2.ino
│
├── 🐍 PYTHON/
│   ├── analizar_mision2.py
│   ├── generar_kml_mision2.py
│   ├── enviar_a_firebase.py
│   └── requirements.txt
│
├── 📊 DATOS/
│   ├── MISSION2.CSV (generado tras vuelo)
│   ├── mapa_calor_cansat.html (resultado)
│   └── firmas_combustion_3d.kml (Google Earth)
│
└── 📋 REFERENCIA/
    ├── INDICE_MAESTRO.md (este archivo)
    ├── TABLA_CONEXIONES.md
    └── TABLA_SENSORES.md
```

---

## ⚡ INICIO RÁPIDO (3 PASOS)

```
PASO 1: Descargar archivos
  ├─ Descarga DOCUMENTO_1 (.md)
  └─ Descarga PROGRAMA_1 (.ino)

PASO 2: Cargar código
  ├─ Abre PROGRAMA_1 en Arduino IDE
  ├─ Carga en placa (Ctrl+U)
  └─ Abre Monitor Serial (9600 baud)

PASO 3: Verificar
  ├─ Deberías ver: "✓ OK" en sensores
  ├─ Tabla de datos actualizándose
  └─ ¡Sistema funcionando!
```

---

## 🎯 FUNCIONES DE CADA DOCUMENTO

| Documento | Qué aprenderás | Código asociado |
|-----------|---|---|
| **1** | Sensores integrados | PROGRAMA_1.ino |
| **2** | SGP30 (gases) | PROGRAMA_2.ino |
| **3** | GPS (posición) | PROGRAMA_3.ino |
| **4** | MicroSD (datos) | PROGRAMA_4.ino |
| **5** | APC220 (telemetría) | PROGRAMA_5.ino |
| **6** | Firebase + Web | Python scripts |
| **Aclaraciones** | Temperatura exacta | DHT22 opcional |
| **README** | Resumen ejecutivo | Todos |

---

## 🚀 PRÓXIMOS PASOS

```
☐ Paso 1: Leer DOCUMENTO_1
☐ Paso 2: Cargar PROGRAMA_1
☐ Paso 3: Verificar sensores
☐ Paso 4: Seguir con DOCUMENTO_2
☐ Paso 5: ... completar según documentos
☐ Paso 6: Cargar PROGRAMA_FINAL
☐ Paso 7: Pre-vuelo checklist
☐ Paso 8: ¡A BRUNETE! 🚀
```

---

## 💡 CONSEJOS

```
✅ Comienza simple (PROGRAMA_1)
✅ Entiende cada etapa antes de avanzar
✅ Usa archivos .ino separados (copiar-pegar fácil)
✅ Consulta documentos para ENTENDER
✅ Verifica conexiones ANTES de cargar código
✅ Usa multímetro (3.3V es CRÍTICO)
✅ Mantén documentación durante desarrollo
✅ Guarda una copia de tu MISSION2.CSV
```

---

## 📞 ¿Dudas?

```
Problema               → Mira en Documento
─────────────────────────────────────────
Sensores no detectan  → DOCUMENTO_1
SGP30 falla          → DOCUMENTO_2 + ACLARACIONES
GPS sin señal        → DOCUMENTO_3
MicroSD no graba     → DOCUMENTO_4
APC220 no comunica   → DOCUMENTO_5
Análisis de datos    → DOCUMENTO_6
Temperatura confusa  → ACLARACIONES
¿Todo junto?         → PROGRAMA_FINAL + README
```

---

## 🎓 APRENDIZAJE ESPERADO

```
Después de completar esta documentación:

✅ Entiendes Arduino Nano 33 BLE
✅ Sabes usar I2C, Serial, SPI
✅ Puedes integrar múltiples sensores
✅ Sabes analizar datos ambientales
✅ Puedes crear visualizaciones
✅ Eres capaz de debugguear problemas
✅ Comprendes CanSat completamente
```

---

## 📊 MATRIZ DE DIFICULTAD

| Concepto | Dificultad | Documentar | Programa |
|----------|-----------|-----------|----------|
| Sensores integrados | ⭐ Fácil | Doc 1 | Prog 1 |
| I2C (SGP30) | ⭐⭐ | Doc 2 | Prog 2 |
| Serial (GPS) | ⭐⭐ | Doc 3 | Prog 3 |
| SPI (MicroSD) | ⭐⭐⭐ | Doc 4 | Prog 4 |
| RF (APC220) | ⭐⭐⭐ | Doc 5 | Prog 5 |
| Firebase | ⭐⭐⭐⭐ | Doc 6 | Python |
| Todo integrado | ⭐⭐⭐⭐⭐ | README | Final |

---

## ✅ CHECKLIST COMPLETITUD

```
DOCUMENTOS:
  ☐ DOCUMENTO_1_SENSORES_INTEGRADOS_HIBRIDO.md
  ☐ DOCUMENTO_2_SGP30_HIBRIDO.md
  ☐ DOCUMENTO_3_SENSOR_GPS_POSICION.md
  ☐ DOCUMENTO_4_MICROSD_GRABACION.md
  ☐ DOCUMENTO_5_APC220_TELEMETRIA.md
  ☐ DOCUMENTO_6_FIREBASE_WEB.md
  ☐ ACLARACIONES_SENSORES_TEMPERATURA.md
  ☐ README_ACTUALIZADO.md
  ☐ INDICE_MAESTRO.md (este archivo)

PROGRAMAS:
  ☐ PROGRAMA_1_SENSORES_INTEGRADOS.ino
  ☐ PROGRAMA_2_SGP30_GASES.ino
  ☐ PROGRAMA_3_GPS_POSICION.ino
  ☐ PROGRAMA_4_MICROSD_GRABACION.ino
  ☐ PROGRAMA_5_APC220_TELEMETRIA.ino
  ☐ PROGRAMA_FINAL_CANSAT_MISION2.ino

SCRIPTS PYTHON:
  ☐ analizar_mision2.py
  ☐ generar_kml_mision2.py
  ☐ enviar_a_firebase.py
  ☐ requirements.txt

ARCHIVOS REFERENCIA:
  ☐ CHECKLIST_PRE_VUELO.md
  ☐ TABLA_CONEXIONES.md
  ☐ TABLA_SENSORES.md
```

---

**¡Listo para Brunete 2026!** 🚀

**Estado:** ✅ Documentación completa y híbrida  
**Última actualización:** Enero 2026  
**Autor:** IES Diego Velázquez
