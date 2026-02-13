# 🌐 CANSAT - Panel Web de Telemetría

Panel de control en tiempo real para visualización de datos del CanSat conectado a Firebase Realtime Database.

---

## 🗂️ Estructura de Datos en Firebase

El sistema organiza la información en cuatro ramas principales dentro de `cansat/`:

* **telemetria**: Datos en directo durante el concurso.
* **pruebas**: Testeo de sensores en tiempo real sin almacenamiento local.
* **replay**: Reproducción de vuelos grabados (`caelum_datos_vuelo.csv`).
* **simulacion**: Datos de vuelos históricos o simulados (`vuelo_brunete_17marzo.csv`).


## 🚀 Motores de Ejecución (Scripts Python)

### 1. Motor Local (PC) - `receptor_telemetria.py`
* **Funciones**: Lee el puerto serie (USB/APC220), autoinstala librerías (`requests`, `pyserial`) y limpia Firebase al iniciar.
* **Modo Concurso**: Envía a `/telemetria` y genera automáticamente el archivo `caelum_datos_vuelo.csv`.
* **Modo Pruebas**: Envía a `/pruebas` para verificar sensores sin guardar archivos.

### 2. Motor Nube (Colab) - `replay_nube.py`
* **Funciones**: Detecta automáticamente el archivo subido a Google Colab.
* **Lógica**: 
    * Si detecta `caelum_datos_vuelo.csv` → Modo **REPLAY**.
    * Si detecta `vuelo_brunete_17marzo.csv` → Modo **SIMULACIÓN**.

**Nota:** Las carpetas se crean automáticamente cuando el script envía el primer dato. Los scripts borran datos anteriores de su carpeta antes de empezar.

---
## 🎨 Panel de Control (HTML)

El panel `caelum_dashboard.html` incluye ahora un selector con **4 pestañas** para sincronizarse con los motores:
- ✅ **CONCURSO LIVE**: Conectado a `/telemetria`.
- ✅ **PRUEBAS SENSORES**: Conectado a `/pruebas`.
- ✅ **REPLAY VUELO**: Conectado a `/replay`.
- ✅ **SIMULACIÓN**: Conectado a `/simulacion`.

---

## 📊 Sensores y Telemetría

### Hardware Utilizado
* **Arduino Nano 33 BLE**: Presión (LPS22HB), Temperatura (HS3003), Acelerómetro y Giroscopio.
* **GPS ATGM336H**: Posicionamiento global (Latitud, Longitud).
* **SCD40**: Medición de CO2 (ppm).
* **HM3301**: Sensores de partículas (PM2.5 y PM10).

**Características:**
- ✅ Mapa satelital ArcGIS
- ✅ CanSat 3D con orientación
- ✅ Gráficos de altitud, presión y temperatura
- ✅ Panel de calidad del aire (CO2 + PM2.5)
- ✅ Indicador de firmas de combustión
- ✅ Selector de modo: Directo / Replay / Simulación / Pruebas

---
# 🌐 CANSAT - Panel Web de Telemetría (Misión CAELUM)

Este proyecto permite la visualización en tiempo real de la telemetría del CanSat mediante una arquitectura de doble motor (PC y Nube) conectada a Firebase Realtime Database.

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
  "temp": 8.5,
  "hum": 65,
  "presion": 950.5,
  "co2": 450,
  "pm1_0": 8,
  "pm2_5": 12,
  "pm10": 18,
  "accel_x": 0.1,
  "accel_y": -0.2,
  "accel_z": 9.8,
  "gyro_x": 5.0,
  "gyro_y": -3.0,
  "gyro_z": 1.0,
  "fase": "descenso"
}

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

## 📊 Sensores Visualizados

### Sensores Integrados (Arduino Nano 33 BLE)
| Sensor | Datos |
|--------|-------|
| LPS22HB | Presión, Altitud |
| HS3003 | Temperatura, Humedad |
| BMI270 | Acelerómetro (X,Y,Z) |
| BMM150 | Giroscopio (X,Y,Z) |

### Sensores Externos
| Sensor | Datos |
|--------|-------|
| GPS ATGM336H | Latitud, Longitud, Altitud, Satélites |
| SCD40 | CO2 (ppm) |
| HM3301 | PM1.0, PM2.5, PM10 (µg/m³) |

---

## 🧪 Probar Localmente

```bash
# Servidor local
python -m http.server 8000

# Abrir en navegador
http://localhost:8000/cansat_firebase.html
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

## 📱 Acceso Móvil

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


---

**Proyecto:** CanSat Misión 2 - Febrero 2026  
**Sensores:** SCD40 (CO2) + HM3301 (PM2.5)  
**Centro:** IES Diego Velázquez
