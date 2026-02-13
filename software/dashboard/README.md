# 🌐 CANSAT - Panel Web de Telemetría

Panel de control en tiempo real para visualización de datos del CanSat conectado a Firebase Realtime Database.

---
Sistema unificado para la gestión de datos CanSat.

## 🗂️ Estructura de Firebase
- `/cansat/telemetria`: Datos en vivo del concurso.
- `/cansat/pruebas`: Testeo de sensores.
- `/cansat/replay`: Reproducción de `caelum_datos_vuelo.csv`.
- `/cansat/simulacion`: Datos de `vuelo_brunete_17marzo.csv`.

## 📊 Diccionario de Datos Único (21 Campos)
Todos los sistemas usan estas claves exactas:
`timestamp`, `datetime`, `lat`, `lon`, `alt`, `alt_mar`, `sats`, `temp`, `hum`, `presion`, `co2`, `pm1_0`, `pm2_5`, `pm10`, `accel_x`, `accel_y`, `accel_z`, `gyro_x`, `gyro_y`, `gyro_z`, `fase`.

## 🚀 Guía de Scripts
1. **PC**: Usa `receptor_telemetria.py` para Concurso y Pruebas.
2. **Nube (Colab)**: Usa `replay_nube.py` para Replay y Simulación.
3. **Web**: `caelum_dashboard.html` para visualizar todo.


## 🚀 Motores de Ejecución (Scripts Python)

### 1. Receptor_telemetria (PC) - `receptor_telemetria.py`
* **Funciones**: Lee el puerto serie (USB/APC220), autoinstala librerías (`requests`, `pyserial`) y limpia Firebase al iniciar.
* **Modo Concurso**: Envía a `/telemetria` y genera automáticamente el archivo `caelum_datos_vuelo.csv`.
* **Modo Pruebas**: Envía a `/pruebas` para verificar sensores sin guardar archivos.

### 2. Replay_nube (Colab) - `replay_nube.py`
* **Funciones**: Detecta automáticamente el archivo subido a Google Colab.
* **Lógica**: 
    * Si detecta `caelum_datos_vuelo.csv` → Modo **REPLAY**.
    * Si detecta `vuelo_brunete_17marzo.csv` → Modo **SIMULACIÓN**.

**Nota:** Las carpetas se crean automáticamente cuando el script envía el primer dato. Los scripts borran datos anteriores de su carpeta antes de empezar.

---
# 🌐 CANSAT - Panel Web de Telemetría (Misión CAELUM)

Este proyecto permite la visualización en tiempo real de la telemetría del CanSat mediante una arquitectura de doble motor (PC y Nube) conectada a Firebase Realtime Database.

## 🎨 Panel de Control (HTML)
**Características:**
- ✅ Mapa satelital ArcGIS
- ✅ CanSat 3D con orientación
- ✅ Gráficos de altitud, presión y temperatura
- ✅ Panel de calidad del aire (CO2 + PM2.5)
- ✅ Indicador de firmas de combustión

Incluye ahora un selector con **4 pestañas** para sincronizarse con los motores:
- ✅ **CONCURSO LIVE**: Conectado a `/telemetria`.
- ✅ **PRUEBAS SENSORES**: Conectado a `/pruebas`.
- ✅ **REPLAY VUELO**: Conectado a `/replay`.
- ✅ **SIMULACIÓN**: Conectado a `/simulacion`.

---

#**🔧 Solución de Problemas **
**Problema**                  **Solución**
Error 'ModuleNotFoundError'	El script de PC instala automáticamente requests y pyserial. Solo asegúrate de tener conexión a internet al ejecutarlo por primera vez.
No se ven datos en el panel	Asegurarse de que el modo seleccionado en el selector del HTML coincide con el modo ejecutado en Python.
Puerto serie no encontrado	   Verificar el nombre del puerto (COM3, COM4, etc.) en el administrador de dispositivos y actualízalo en motor_pc.py.

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

**Proyecto:** CanSat Misión 2 - Febrero 2026  
**Sensores:** SCD40 (CO2) + HM3301 (PM2.5)  
**Centro:** IES Diego Velázquez
