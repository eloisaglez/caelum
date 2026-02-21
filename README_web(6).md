# 🌐 CANSAT - Panel Web de Telemetría

Panel de control en tiempo real para visualización de datos del CanSat conectado a Firebase Realtime Database.

---
Sistema unificado para la gestión de datos CanSat.

## 🗂️ Estructura de Firebase
- `/cansat/telemetria`: Datos en vivo del concurso.
- `/cansat/pruebas`: Testeo de sensores.
- `/cansat/replay`: Reproducción de `datos_SD.csv` (generado por limpiar_espera.py).
- `/cansat/simulacion`: Datos de `datos_simulacion.csv`.

## 📊 Diccionario de Datos Único (25 Campos)
Todos los sistemas usan estas claves exactas:
`timestamp`, `datetime`, `lat`, `lon`, `alt`, `alt_mar`, `sats`, `temp_hs`, `hum_hs`, `temp_scd`, `hum_scd`, `temp_lps`, `presion`, `co2`, `pm1_0`, `pm2_5`, `pm10`, `accel_x`, `accel_y`, `accel_z`, `gyro_x`, `gyro_y`, `gyro_z`, `fase`.

**Sensores de temperatura y humedad (validación cruzada):**
- `temp_hs` / `hum_hs` → HS300x (integrado, referencia principal)
- `temp_scd` / `hum_scd` → SCD40 (externo, validación cruzada T+HR)
- `temp_lps` → LPS22HB (integrado, tercera lectura de temperatura)

**CO₂ — trazador de estabilidad atmosférica** (no indicador de calidad del aire a esa altitud)

## 🚀 Guía de Scripts
1. **PC**: Usa `receptor_telemetria.py` para Concurso y Pruebas.
2. **Nube (Colab)**: Usa `caelum_playback.py` para Replay y Simulación.
3. **Web**: `caelum_dashboard.html` para visualizar todo.


## 🚀 Motores de Ejecución (Scripts Python)

### 1. Receptor_telemetria (PC) - `receptor_telemetria.py`
* **Funciones**: Lee el puerto serie (USB/APC220), autoinstala librerías (`requests`, `pyserial`) y limpia Firebase al iniciar.
* **Modo Concurso**: Envía a `/telemetria` y genera automáticamente el archivo `datos_radio.csv`.
* **Modo Pruebas**: Envía a `/pruebas` para verificar sensores sin guardar archivos.

### 2. Caelum Playback (Colab) - `caelum_playback.py`
* **Funciones**: Detecta automáticamente el archivo subido a Google Colab.
* **Lógica**: 
    * Si detecta `datos_SD.csv` → Modo **REPLAY** (usar limpiar_espera.py primero).
    * Si detecta `datos_simulacion.csv` → Modo **SIMULACIÓN**.

**Nota:** Las carpetas se crean automáticamente cuando el script envía el primer dato. Los scripts borran datos anteriores de su carpeta antes de empezar.

---
# 🌐 CANSAT - Panel Web de Telemetría (Misión CAELUM)

Este proyecto permite la visualización en tiempo real de la telemetría del CanSat mediante una arquitectura de doble motor (PC y Nube) conectada a Firebase Realtime Database.

## 🎨 Panel de Control (HTML)
**Características:**
- ✅ Mapa satelital ArcGIS
- ✅ CanSat 3D con orientación
- ✅ Gráficos de altitud, presión y temperatura
- ✅ Panel de partículas PM1.0, PM2.5, PM10 (perfil vertical)
- ✅ CO₂ como trazador de estabilidad atmosférica
- ✅ Validación cruzada temperatura: HS300x vs SCD40 vs LPS22HB
- ✅ Indicador de inversiones térmicas (alt↑ + temp↑ + PM2.5↑)

Incluye ahora un selector con **4 pestañas** para sincronizarse con los motores:
- ✅ **CONCURSO LIVE**: Conectado a `/telemetria`.
- ✅ **PRUEBAS SENSORES**: Conectado a `/pruebas`.
- ✅ **REPLAY VUELO**: Conectado a `/replay`.
- ✅ **SIMULACIÓN**: Conectado a `/simulacion`.

---

## 📊 Estructura de Datos Oficial (JSON)

Cada paquete enviado a Firebase sigue este formato estricto para asegurar la compatibilidad con el panel web:

```json
{
  "timestamp": 0,
  "datetime": "2026-03-17T11:30:00",
  "lat": 40.4052,
  "lon": -3.9931,
  "alt": 500.0,
  "alt_mar": 1150.0,
  "sats": 8,
  "temp_hs": 8.5,
  "hum_hs": 65.0,
  "temp_scd": 8.6,
  "hum_scd": 64.2,
  "temp_lps": 8.9,
  "presion": 950.5,
  "co2": 430,
  "pm1_0": 8.0,
  "pm2_5": 12.0,
  "pm10": 18.0,
  "accel_x": 0.1,
  "accel_y": -0.2,
  "accel_z": 9.8,
  "gyro_x": 5.0,
  "gyro_y": -3.0,
  "gyro_z": 1.0,
  "fase": "descenso"
}
```
---
## 🔧 Configuración Firebase

### URL Base
```
https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app
```

### Rutas de Datos
```
/cansat/telemetria/[timestamp]/   ← Concurso
/cansat/replay/[timestamp]/       ← Reproducción
/cansat/simulacion/[timestamp]/   ← Simulador
/cansat/pruebas/[timestamp]/      ← Pruebas
```

### Reglas de Seguridad
```json
{
  "rules": {
    "cansat": {
      ".read": true,
      ".write": true
    }
  }
}
```

---

## 🧪 Probar Localmente

```bash
# Servidor local
python -m http.server 8000

# Abrir en navegador
http://localhost:8000/caelum_dashboard.html
```

---

## 🚀 Desplegar en Firebase Hosting

```bash
# Instalar Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Inicializar
firebase init hosting

# Desplegar
firebase deploy --only hosting
```

**URL:** https://cansat-66d98.web.app

---

## 📱 Acceso Móvil (REVISAR) ‼️

Una vez desplegado:
1. Abre: `https://cansat-66d98.web.app`
2. Selecciona el modo (Directo/Replay/Simulación/Pruebas)
3. Funciona en cualquier dispositivo

---

## 🛠️ Solución de Problemas

| Problema | Solución |
|----------|----------|
| Mapa no carga | Verificar conexión a internet |
| Datos no aparecen | Verificar modo correcto seleccionado |
| Error CORS | Usar servidor HTTP, no `file://` |
| Firebase offline | Verificar URL y reglas de seguridad |


---

**Proyecto:** CanSat Misión 2 - Febrero 2026  
**Sensores:** SCD40 (CO₂ + T + HR) + HM3301 (PM2.5) + HS300x (T + HR) + LPS22HB (T + Presión)  
**Centro:** IES Diego Velázquez
