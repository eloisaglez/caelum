# Proyecto Caelum — Guía de Configuración Firebase

*Caelum - Del latín: Cielo, Firmamento*  
*IES Diego Velázquez — Torrelodones, Madrid*  
*Enero 2026*

---

> ⚠️ **NOTA — Documento de referencia histórica**
>
> Este documento describe la arquitectura inicial del proyecto (enero 2026), basada en Arduino Uno + GPS independiente. El sistema actual usa Arduino Nano 33 BLE Sense Rev2 con sensores SCD40, HM3301, LPS22HB, HS300x y GPS integrado.
>
> **Válido como referencia SOLO para la configuración de Firebase (Paso 1).**
> Para la documentación técnica completa del sistema actual, consultar `PRUEBAS_PROBLEMAS_SOLUCIONES_Arduino_Nano_33_BLE_Sense.md`

---

## Índice

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Paso 1: Configuración de Firebase](#paso-1-configuración-de-firebase)
3. [Paso 2: Script Python](#paso-2-script-python)
4. [Paso 3: Panel Web](#paso-3-panel-web)
5. [Pendiente al Finalizar el Proyecto](#pendiente-al-finalizar-el-proyecto)

---

## Arquitectura del Sistema

```
CanSat (Arduino + sensores + APC220)
        ↓  radio 434 MHz
Estación tierra (PC + APC220)
        ↓  USB serie
receptor_telemetria.py
        ↓  HTTPS
Firebase Realtime Database
        ↓  WebSocket
cansat_dashboard.html  (navegador)
```

---

## Paso 1: Configuración de Firebase

### 1.1 Crear proyecto Firebase

1. Ir a: https://console.firebase.google.com/
2. Clic en **Agregar proyecto**
3. Nombre del proyecto: `caelum` (o el que prefieras)
4. Desactivar Google Analytics (no es necesario)
5. Clic en **Crear proyecto**

### 1.2 Crear Realtime Database

1. En el menú lateral: **Realtime Database**
2. Clic en **Crear base de datos**
3. Ubicación: `europe-west1` (más cercana a España)
4. Modo: **Comenzar en modo de prueba** (temporal para desarrollo)

### 1.3 Obtener credenciales para Python

1. Ir a: **Configuración del proyecto** (⚙️) → **Cuentas de servicio**
2. Clic en **Generar nueva clave privada**
3. Se descarga `serviceAccountKey.json` → guardarlo en la carpeta del proyecto
4. ⚠️ **No subir este archivo a GitHub** — añadirlo al `.gitignore`

### 1.4 Obtener configuración Web (para el dashboard)

1. Ir a: **Configuración del proyecto** → **General**
2. En **Tus aplicaciones** → Web (ícono `</>`) → **Registrar app**
3. Nombre: `Panel Caelum`
4. Copiar el bloque `firebaseConfig` — se necesita para el dashboard HTML

```js
// Ejemplo de firebaseConfig (sustituir con los datos reales)
const firebaseConfig = {
    apiKey: "TU_API_KEY",
    databaseURL: "https://TU_PROYECTO-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "TU_PROYECTO",
    appId: "TU_APP_ID"
};
```

> ⚠️ No subir este bloque a GitHub si el repositorio es público.
> Ver sección [Pendiente al Finalizar el Proyecto](#pendiente-al-finalizar-el-proyecto).

---

## Paso 2: Script Python

### Instalación de librerías

```bash
pip install pyserial firebase-admin requests
```

### Configuración necesaria

- Colocar `serviceAccountKey.json` en la misma carpeta que el script
- En `receptor_telemetria.py`: cambiar la URL de Firebase por la del proyecto
- En `receptor_telemetria.py`: cambiar el puerto serie por el correcto (`COM5` en Windows, `/dev/cu.usbmodem...` en Mac)

### Ejecución

```bash
python receptor_telemetria.py
```

El script lee los datos del puerto serie (APC220) y los sube a Firebase en tiempo real. Solo envía datos de fases activas (`caida_libre`, `apertura`, `descenso`, `tierra`) — no envía la fase `espera` para no saturar la base de datos.

---

## Paso 3: Panel Web

El dashboard `cansat_dashboard.html` se abre directamente en el navegador (no necesita servidor).

### Configurar Firebase en el dashboard

Buscar en el HTML el bloque `firebaseConfig` y sustituir con los datos del proyecto:

```js
const firebaseConfig = {
    apiKey: "TU_API_KEY",
    databaseURL: "https://TU_PROYECTO-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "TU_PROYECTO",
    appId: "TU_APP_ID"
};
```

### Modos de operación

| Modo | Descripción |
|------|-------------|
| 📡 LIVE | Telemetría en tiempo real desde el APC220 |
| ✈️ SIMULACIÓN | Reproduce datos de simulación desde Firebase |

### Uso durante el vuelo

1. Ejecutar `receptor_telemetria.py` en el PC de tierra
2. Abrir `cansat_dashboard.html` en el navegador
3. Seleccionar modo **📡 LIVE**
4. Los datos aparecen en tiempo real conforme llegan por radio

---

## Pendiente al Finalizar el Proyecto

### Restringir escritura en Firebase

Una vez terminada la competición, cambiar las reglas de Firebase para que solo sea posible leer datos públicamente pero no escribir sin autenticación.

**Pasos:**
1. Ir a [Firebase Console](https://console.firebase.google.com/) → proyecto `cansat-66d98`
2. **Realtime Database** → **Reglas**
3. Sustituir las reglas actuales por:

```json
{
  "rules": {
    ".read": true,
    ".write": false
  }
}
```

4. Clic en **Publicar**

Con esto el dashboard sigue funcionando (lectura pública) pero nadie puede escribir en la base de datos sin credenciales de administrador.

---

*Última actualización: Abril 2026*  
*Documentación técnica completa: `PRUEBAS_PROBLEMAS_SOLUCIONES_Arduino_Nano_33_BLE_Sense.md`*
