# 🛰️ CANSAT - MISIÓN 2
## Detección de Firmas de Combustión y Mapas de Calor Georreferenciados

[![Arduino](https://img.shields.io/badge/Arduino-00979D?style=flat&logo=Arduino&logoColor=white)](https://www.arduino.cc/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-blue)](LICENSE)

---

## 📋 Índice

- [Descripción](#-descripción)
- [Objetivos](#-objetivos)
- [Hardware](#-hardware)
- [Software](#-software)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Resultados](#-resultados)
- [Contribuir](#-contribuir)

---

## 🎯 Descripción

La **Misión 2** del proyecto CanSat se centra en el **monitoreo ambiental georreferenciado** mediante la detección de compuestos volátiles orgánicos totales (TVOC) y CO₂ equivalente (eCO2) durante el descenso del satélite.

A diferencia de la Misión 1 (que miraba hacia arriba), esta misión **mira hacia el suelo** para identificar qué actividades humanas afectan la calidad del aire:

- 🚗 **Tráfico vehicular** en carreteras
- 🏭 **Generadores eléctricos** de diésel
- 🔥 **Combustión de biomasa**
- 🌿 **Zonas de aire limpio**

---

## 🎯 Objetivos

### Científicos

- ✅ Medición continua de TVOC/eCO2 durante el descenso
- ✅ Georreferenciación de cada medición (GPS)
- ✅ Identificación de "firmas de combustión" características
- ✅ Detección de fuentes de contaminación

### Técnicos

- ✅ Integración SGP30 + GPS + SD en Arduino
- ✅ Calibración automática del sensor
- ✅ Mapas de calor interactivos (Folium)
- ✅ Visualización 3D en Google Earth (KML)
- ✅ Análisis estadístico con gráficas

---

## 🔧 Hardware

### Lista de Componentes

| Componente | Modelo | Función | Conexión |
|------------|--------|---------|----------|
| Microcontrolador | Arduino Nano | Procesamiento central | USB |
| Sensor de gas | Adafruit SGP30 | Medición TVOC/eCO2 | I2C: SDA=A4, SCL=A5 |
| GPS | NEO-6M/7M/8M | Geolocalización | UART: TX=D3, RX=D4 |
| Almacenamiento | microSD Module | Registro de datos | SPI: CS=D10 |
| Indicador | LED | Estado del sistema | Digital D8 |
| Batería | LiPo 3.7V 1000mAh | Alimentación | Regulador 5V |

### Esquema de Conexiones

```
Arduino Nano
├── A4 (SDA) ──────── SGP30 SDA
├── A5 (SCL) ──────── SGP30 SCL
├── D3 (TX) ───────── GPS RX
├── D4 (RX) ───────── GPS TX
├── D10 (CS) ──────── SD CS
├── D11 (MOSI) ────── SD MOSI
├── D12 (MISO) ────── SD MISO
├── D13 (SCK) ─────── SD SCK
└── D8 ───────────── LED
```

---

## 💻 Software

### Arduino

**Archivo:** `cansat_mission2.ino`

**Librerías necesarias:**
```cpp
#include <Adafruit_SGP30.h>   // Control del sensor
#include <TinyGPS++.h>          // Parsing GPS
#include <SD.h>                 // Tarjeta SD
#include <SoftwareSerial.h>     // Serial por software
```

**Instalación de librerías:**
1. Abrir Arduino IDE
2. Ir a `Herramientas > Administrar bibliotecas`
3. Buscar e instalar:
   - `Adafruit SGP30`
   - `TinyGPSPlus`
   - `SD` (incluida por defecto)

### Python

**Scripts disponibles:**

| Script | Función | Salida |
|--------|---------|--------|
| `analizar_mision2.py` | Análisis estadístico + mapa de calor | `mapa_calor_cansat.html` + `analisis_cansat.png` |
| `generar_kml_mision2.py` | Visualización 3D Google Earth | `firmas_combustion_3d.kml` |
| `generar_datos_ejemplo.py` | Generación de datos de prueba | `mission2.csv` |

**Instalación de dependencias:**
```bash
pip install pandas numpy folium matplotlib seaborn simplekml
```

---

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone https://github.com/tu-usuario/cansat-mision2.git
cd cansat-mision2
```

### 2. Cargar código en Arduino

1. Abrir `cansat_mission2.ino` en Arduino IDE
2. Conectar Arduino Nano vía USB
3. Seleccionar placa: `Herramientas > Placa > Arduino Nano`
4. Seleccionar procesador: `ATmega328P (Old Bootloader)` si es necesario
5. Seleccionar puerto COM correcto
6. Hacer clic en **Subir** ⬆️

### 3. Instalar dependencias Python

```bash
pip install -r requirements.txt
```

---

## 📖 Uso

### Pre-Vuelo

1. **Encender el sistema**
   - Conectar batería al Arduino
   - Esperar **15 segundos** para calibración del SGP30
   - LED debe parpadear indicando sistema listo

2. **Verificar GPS**
   - Abrir Monitor Serial (115200 baud)
   - Esperar señal GPS (mínimo 4 satélites)
   - Confirmación: "GPS: OK"

3. **Insertar tarjeta SD**
   - Formateada en FAT32
   - Mínimo 1GB de espacio

### Durante el Vuelo

- ✅ El sistema registra automáticamente cada **5 segundos**
- ✅ Datos se guardan en `mission2.csv`
- ✅ LED parpadea en cada medición
- ✅ No requiere intervención

### Post-Vuelo

1. **Recuperar CanSat**
2. **Extraer tarjeta SD**
3. **Copiar `mission2.csv` al ordenador**
4. **Ejecutar análisis:**

```bash
# Generar mapa de calor y gráficas
python analizar_mision2.py

# Generar visualización 3D para Google Earth
python generar_kml_mision2.py
```

---

## 📊 Resultados

### Mapa de Calor Interactivo

![Mapa de Calor](docs/ejemplo_mapa_calor.png)

**Archivo:** `mapa_calor_cansat.html`

- 🟢 **Verde:** Aire limpio (TVOC < 220 ppb)
- 🟡 **Amarillo:** Calidad moderada (220-660 ppb)
- 🔴 **Rojo:** Alta contaminación (> 2200 ppb)

### Visualización 3D en Google Earth

![Google Earth](docs/ejemplo_google_earth.png)

**Archivo:** `firmas_combustion_3d.kml`

- Cilindros verticales proporcionales a TVOC
- Colores según nivel de contaminación
- Información detallada en cada punto

### Gráficas de Análisis

![Análisis](docs/analisis_cansat.png)

**Archivo:** `analisis_cansat.png`

- Evolución temporal de TVOC
- Correlación TVOC vs eCO2
- Distribución de valores
- Señales raw (H2 y Ethanol)

---

## 🎨 Clasificación de Calidad del Aire

| Rango TVOC | Clasificación | Color | Impacto |
|------------|---------------|-------|---------|
| 0 - 220 ppb | 🟢 Excelente | Verde | Aire limpio |
| 220 - 660 ppb | 🟡 Buena | Amarillo | Aceptable |
| 660 - 2200 ppb | 🟠 Moderada | Naranja | Ventilación recomendada |
| 2200 - 5500 ppb | 🔴 Mala | Rojo | Fuente cercana |
| > 5500 ppb | ⛔ Muy Mala | Rojo oscuro | Peligroso |

---

## 🔍 Firmas de Combustión Detectables

### 1. Tráfico Vehicular 🚗
- TVOC: 300-800 ppb
- eCO2: Elevado (> 1000 ppm)
- Patrón: Incremento gradual

### 2. Generadores Diésel 🚜
- TVOC: > 1000 ppb
- H2 raw: Alto (> 13000)
- Patrón: Picos pronunciados

### 3. Combustión Biomasa 🔥
- TVOC: > 500 ppb
- Ethanol raw: Alto (> 18000)
- Patrón: Incremento sostenido

### 4. Zona Industrial 🏭
- TVOC: Variable
- eCO2: Moderado-alto
- Patrón: Fluctuaciones

---

## 📁 Estructura del Proyecto

```
cansat-mision2/
│
├── README.md
├── requirements.txt
│
├── arduino/
│   └── cansat_mission2.ino
│
├── python/
│   ├── analizar_mision2.py
│   ├── generar_kml_mision2.py
│   └── generar_datos_ejemplo.py
│
├── docs/
│   ├── Documentacion_CanSat_Mision2.docx
│   ├── esquema_conexiones.png
│   └── manual_usuario.pdf
│
└── data/
    └── mission2.csv (generado tras el vuelo)
```

---

## 🛠️ Solución de Problemas

### GPS no obtiene señal
- ✅ Asegurarse de estar **al aire libre**
- ✅ Esperar 2-3 minutos para adquisición inicial
- ✅ Verificar antena cerámica conectada

### SGP30 devuelve valores anómalos
- ✅ Esperar **15 segundos** tras encender
- ✅ Evitar tocar el sensor con los dedos
- ✅ Verificar conexiones I2C

### SD no graba datos
- ✅ Formatear en **FAT32**
- ✅ Verificar conexiones SPI
- ✅ Comprobar que CS = D10

---

## 🎓 Aplicaciones Educativas

Este proyecto es ideal para:

- ✅ **Competiciones CanSat** (ESA, NASA)
- ✅ **Proyectos de Bachillerato** (Tecnología Industrial)
- ✅ **STEAM** (Ciencia, Tecnología, Ingeniería, Arte, Matemáticas)
- ✅ **Estudios ambientales** locales
- ✅ **Aprendizaje de programación** (Arduino + Python)

---

## 📚 Referencias

- [Adafruit SGP30 Datasheet](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-sgp30-gas-tvoc-eco2-mox-sensor.pdf)
- [TinyGPS++ Documentation](http://arduiniana.org/libraries/tinygpsplus/)
- [Folium Documentation](https://python-visualization.github.io/folium/)
- [Google Earth KML Reference](https://developers.google.com/kml/documentation)

---

## 👥 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto es de uso **educativo** y está disponible bajo licencia MIT.

---

## 📧 Contacto

**IES Diego Velázquez**  
Departamento de Tecnología  
Torrelodones, Madrid, España

---

## ⭐ Agradecimientos

- Equipo de estudiantes del IES Diego Velázquez
- Departamento de Tecnología
- Programa Erasmus+ STEMadrid Network

---

<div align="center">

**🛰️ CanSat Misión 2 - Enero 2026**

*Hecho con ❤️ para la educación STEM*

</div>
