# 🌐 CANSAT - Panel Web de Telemetría

Panel de control en tiempo real para visualización de datos del CanSat conectado a Firebase Realtime Database.

---

## 🗂️ Estructura Firebase

```
cansat/
├── telemetria/    ← Día del concurso (datos en directo)
├── replay/        ← Reproducir vuelos grabados
├── simulacion/    ← Datos del simulador Python
└── pruebas/       ← Probar sensores reales
```

| Carpeta | Script Python | Cuándo usar |
|---------|---------------|-------------|
| **telemetria** | `receptor_telemetria.py` | 🔴 Día del concurso |
| **replay** | `reproductor_replay.py` | ⏪ Revisar vuelos después |
| **simulacion** | `simulador_firebase.py` | 🧪 Probar panel sin hardware |
| **pruebas** | `enviar_pruebas.py` | 🔧 Probar sensores antes del concurso |

**Nota:** Las carpetas se crean automáticamente cuando el script envía el primer dato. Los scripts borran datos anteriores de su carpeta antes de empezar.

---

## 🎨 Panel de Control

### **cansat_firebase.html**

**Características:**
- ✅ Mapa satelital ArcGIS
- ✅ CanSat 3D con orientación
- ✅ Gráficos de altitud, presión y temperatura
- ✅ Panel de calidad del aire (CO2 + PM2.5)
- ✅ Indicador de firmas de combustión
- ✅ Selector de modo: Directo / Replay / Simulación / Pruebas

---

## 🚀 Uso Rápido

### Probar sin hardware (simulación)
```bash
python simulador_firebase.py
# Panel web → Modo: Simulación
```

### Probar sensores reales
```bash
python enviar_pruebas.py
# Panel web → Modo: Pruebas
```

### Día del concurso
```bash
python receptor_telemetria.py
# Panel web → Modo: Directo
# Guarda CSV automáticamente
```

### Revisar vuelo después
```bash
python reproductor_replay.py caelum_datos_vuelo.csv
# Panel web → Modo: Replay
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

### Estructura de Datos
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

## 📁 Scripts Python

| Script | Función |
|--------|---------|
| `receptor_telemetria.py` | Recibe del APC220, guarda caelum_datos_vuelo.csv, envía a /telemetria/ |
| `reproductor_replay.py` | Reproduce CSV a /replay/ |
| `simulador_firebase.py` | Genera datos simulados a /simulacion/ |
| `enviar_pruebas.py` | Recibe del COM, envía a /pruebas/ (sin guardar CSV) |

---

**Proyecto:** CanSat Misión 2 - Febrero 2026  
**Sensores:** SCD40 (CO2) + HM3301 (PM2.5)  
**Centro:** IES Diego Velázquez
