# 🛰️ CANSAT - MISIÓN 2
## Detección de Firmas de Combustión

[![Arduino](https://img.shields.io/badge/Arduino_Nano_33_BLE-00979D?style=flat&logo=Arduino)](https://www.arduino.cc/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-blue)](LICENSE)

---

## 📋 Resumen Ejecutivo

**CanSat Misión 2** es un proyecto de **monitoreo ambiental desde satélite miniatura** que detecta contaminación aérea (TVOC/eCO2) georreferenciada mediante GPS durante su descenso.

**Objetivo:** Identificar firmas de combustión (tráfico, generadores, biomasa) y crear mapas de calor interactivos.

**Duración:** ~10 minutos de vuelo | **Alcance:** Cobertura geográfica 5km² | **Precisión:** ±30m GPS

---

## 🎯 Características Principales

| Característica | Descripción |
|---|---|
| **Sensor Gas** | SGP30: TVOC + eCO2 + H2 + Ethanol |
| **Posicionamiento** | GPS: Lat/Lon/Altitud |
| **Almacenamiento** | MicroSD: Respaldo de datos |
| **Telemetría** | APC220: RF en tiempo real (opcional) |
| **Control** | Arduino Nano 33 BLE Sense Rev2 |
| **Análisis** | Python: Mapas + KML + Gráficas |

---

## 🔌 Conexiones Hardware

```
Arduino Nano 33 BLE:
├─ I2C (A4/A5) ─────→ SGP30 (TVOC/eCO2)
├─ Serial D2/D4 ────→ GPS (Posición)
├─ SPI D10-D13 ─────→ MicroSD (Datos)
├─ Serial1 Grove ───→ APC220 (Telemetría RF)
└─ Integrados:
   ├─ HS3003: Temperatura + Humedad
   ├─ LPS22HB: Presión + Altitud
   ├─ BMI270: Acelerómetro
   └─ BMM150: Magnetómetro
```

---

## 🚀 Inicio Rápido

### 1. Cargar programa Arduino

```
1. Abrir: PROGRAMA_FINAL_CANSAT_MISION2.ino
2. Tools → Board → Arduino Nano 33 BLE
3. Tools → Port → COM[X]
4. Ctrl+U para cargar
```

### 2. Instalar dependencias Python

```bash
pip install pandas numpy folium matplotlib seaborn simplekml
```

### 3. Ejecutar análisis post-vuelo

```bash
python analizar_mision2.py        # Genera mapa de calor
python generar_kml_mision2.py     # Visualización 3D Google Earth
```

---

## 📊 Clasificación de Calidad del Aire

| TVOC | Clasificación | Causa Probable |
|------|---------------|---|
| 0-220 ppb | 🟢 Excelente | Aire limpio |
| 220-660 ppb | 🟡 Buena | Zona residencial |
| 660-2200 ppb | 🟠 Moderada | Tráfico/Industrial |
| 2200-5500 ppb | 🔴 Mala | Generador/Biomasa |
| >5500 ppb | ⛔ Muy Mala | Fuente directa |

---

## 🔍 Firmas de Combustión

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

## 📁 Estructura de Archivos

```
cansat-mision2/
├── DOCUMENTO_1_ARDUINO_SENSORES_INTEGRADOS.md
├── DOCUMENTO_2_SENSOR_SGP30_GASES.md
├── DOCUMENTO_3_SENSOR_GPS_POSICION.md
├── DOCUMENTO_4_APC220_TELEMETRIA.md
├── DOCUMENTO_5_MICROSD_GRABACION.md
├── DOCUMENTO_6_PRESENTACION_DATOS_FIREBASE.md
├── ACLARACIONES_SENSORES_TEMPERATURA.md
├── PROGRAMA_FINAL_CANSAT_MISION2.ino
├── mission2.csv (datos vuelo)
├── mapa_calor_cansat.html (resultado)
├── firmas_combustion_3d.kml (Google Earth)
└── analisis_cansat.png (gráficas)
```

---

## ⚙️ Librerías Necesarias

### Arduino IDE
- `Arduino_BMI270_BMM150`
- `Arduino_HS300x`
- `ReefwingLPS22HB`
- `Adafruit_SGP30`
- `SD`

### Python
```
pandas, numpy, folium, matplotlib, seaborn, simplekml
```

---

## 🧪 Pre-Vuelo

```
☐ Arduino inicializa (todos sensores OK)
☐ SGP30 calibrado (esperar 15 seg)
☐ GPS obtiene fix (4+ satélites)
☐ MicroSD formateada (FAT32)
☐ Batería cargada (9V, 11000mAh)
☐ Estructura mecánica lista
☐ Antena GPS hacia arriba
☐ APC220 receptor en tierra (si aplica)
```

---

## 📡 Durante Vuelo

```
✅ Sistema registra cada ~2 segundos
✅ Datos se graban en MISSION2.CSV
✅ LED indica actividad
✅ GPS actualiza posición
✅ SGP30 mide contaminación
✅ No requiere intervención
```

---

## 📊 Post-Vuelo (Análisis)

### Paso 1: Extraer datos
```bash
1. Recuperar CanSat
2. Extraer MicroSD
3. Copiar MISSION2.CSV al PC
```

### Paso 2: Generar visualizaciones
```bash
python analizar_mision2.py
python generar_kml_mision2.py
```

### Paso 3: Ver resultados
```
✓ mapa_calor_cansat.html (abrir en navegador)
✓ firmas_combustion_3d.kml (importar en Google Earth)
✓ analisis_cansat.png (gráficas estadísticas)
```

---

## 🚨 Troubleshooting Rápido

| Problema | Solución |
|---|---|
| GPS sin señal | Ir a exterior, esperar 2-5 min |
| SGP30 valores raros | Esperar 15 seg calibración |
| MicroSD no graba | Formatear FAT32, verificar CS=D10 |
| Arduino no se reconoce | Instalar driver, cambiar puerto USB |
| Datos corruptos | Verificar conexiones, presionar RESET |

---

## ⚠️ Notas Importantes

```
🔴 CRÍTICO - Temperatura:
   • HS3003 mide temperatura integrada (~error ±2-3°C)
   • MEJOR: Agregar DHT22 externo para precisión
   • Ver: ACLARACIONES_SENSORES_TEMPERATURA.md

🔴 CRÍTICO - SGP30:
   • Conectar SOLO a 3.3V (no 5V)
   • Usar Grove Shield o pines A4/A5
   • Evitar breadboard en vuelo

🔴 CRÍTICO - MicroSD:
   • SOLO 3.3V en VCC
   • Formatar en FAT32
   • Insertar ANTES de vuelo
```

---

## 📚 Documentación Completa

Para información detallada, consultar:

1. **DOCUMENTO 1** → Arduino Nano 33 BLE con sensores integrados
2. **DOCUMENTO 2** → SGP30 (TVOC + eCO2)
3. **DOCUMENTO 3** → GPS (Posición + Altitud)
4. **DOCUMENTO 4** → APC220 (Telemetría RF)
5. **DOCUMENTO 5** → MicroSD (Almacenamiento)
6. **DOCUMENTO 6** → Firebase + Páginas Web
7. **ACLARACIONES** → Temperatura y sensores

---

## 🎓 Aplicaciones

✅ Competiciones CanSat (ESA/NASA)  
✅ Proyectos Bachillerato (Tecnología)  
✅ STEAM Education  
✅ Estudios ambientales locales  
✅ Aprendizaje Arduino + Python  

---

## 📊 Formato de Datos CSV

```
tiempo,lat,lon,alt_gps,alt_calc,temp,humedad,presion,tvoc,eco2,h2,ethanol,accelx,accely,accelz,gyroX,gyroY,gyroZ,brujula,satelites

0,40.462584,-3.746275,620.1,620.0,21.5,65.2,929.5,45,410,12500,18000,0.02,-0.01,1.00,0.2,0.1,-0.1,245,6
1,40.462585,-3.746276,620.2,620.1,21.5,65.1,929.5,48,412,12600,18100,0.01,-0.02,1.00,0.1,0.0,0.0,246,6
```

---

## 🔗 Referencias

- [Arduino Nano 33 BLE Sense](https://docs.arduino.cc/hardware/nano-33-ble-sense)
- [Adafruit SGP30](https://learn.adafruit.com/adafruit-sgp30-air-quality-sensor)
- [Folium Maps](https://python-visualization.github.io/folium/)
- [Google Earth KML](https://developers.google.com/kml)

---

## 📞 Contacto

**IES Diego Velázquez**  
Departamento de Tecnología  
Torrelodones, Madrid, España

---

## 🙏 Agradecimientos

- Equipo de estudiantes del IES Diego Velázquez
- Programa Erasmus+ STEMadrid Network
- ESA CanSat Initiative

---

<div align="center">

**🛰️ CanSat Misión 2 - Enero 2026**

*Sistema de Monitoreo Ambiental Georreferenciado*

*Hecho con ❤️ para educación STEAM*

</div>

---

## 📝 Historial de Cambios

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | Enero 2026 | Versión inicial completa |
| 1.1 | Enero 2026 | Resumen ejecutivo añadido |

---

**Última actualización:** Enero 2026  
**Estado:** ✅ Listo para Brunete 2026  
**Autor:** IES Diego Velázquez
