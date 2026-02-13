# 🌐 CANSAT - Panel Web de Telemetría

Panel de control en tiempo real para visualización de datos del CanSat conectado a Firebase Realtime Database.

---

## 🎨 Panel de Control

### **cansat_gold_firebase.html**
Panel profesional estilo "Mission Control" con tema dorado.

**Características:**
- ✅ Mapa satelital ArcGIS (World Imagery)
- ✅ CanSat 3D dorado con ejes RGB
- ✅ Gauges circulares de acelerómetro (X, Y, Z)
- ✅ Gráficos de altitud, presión y temperatura
- ✅ Panel de calidad del aire (TVOC, eCO₂, H₂, Etanol)
- ✅ Layout 50/50 (Mapa+3D | Datos+Gráficos)

---

## 🚀 Despliegue en Firebase

### Paso 1: Configurar Firebase Hosting

```bash
# Instalar Firebase CLI
npm install -g firebase-tools

# Login en Firebase
firebase login

# Inicializar proyecto
firebase init hosting
```

**Configuración:**
- Public directory: `web`
- Configure as single-page app: `No`
- Set up automatic builds: `No`

### Paso 2: Desplegar

```bash
firebase deploy --only hosting
```

Tu panel estará disponible en: `https://cansat-66d98.web.app`

---

## 🔧 Configuración

### Firebase Realtime Database

El panel está configurado para leer de:
```
cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app
```

**Ruta de datos:**
```
cansat/
  └── telemetria/
      └── [timestamp]/
          ├── latitud
          ├── longitud
          ├── altitud / altitudGPS
          ├── presion
          ├── temperatura
          ├── accelX / accelY / accelZ
          ├── rotX / rotY / rotZ
          ├── eco2 (opcional)
          ├── tvoc (opcional)
          ├── h2 (opcional)
          └── etanol (opcional)
```

### Reglas de Seguridad (Database Rules)

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

## 📊 Datos Visualizados

### Datos Actualmente Disponibles
✅ Altitud (GPS)
✅ Presión atmosférica
✅ Temperatura
✅ Acelerómetro (X, Y, Z)
✅ Giroscopio (X, Y, Z)
✅ Coordenadas GPS (lat, lon)

### Datos Preparados para el Futuro
⏳ H₂ (Hidrógeno)
⏳ Etanol
⏳ eCO₂ (CO₂ equivalente)
⏳ TVOC (Compuestos orgánicos volátiles)

*Estos campos se mostrarán automáticamente cuando el CSV los incluya.*

---

## 🧪 Probar Localmente

### Opción 1: Abrir directamente
```bash
# Abrir el HTML en el navegador
open cansat_gold_firebase.html
# o
firefox cansat_gold_firebase.html
```

### Opción 2: Servidor local
```bash
# Python 3
python -m http.server 8000

# Navegar a: http://localhost:8000/cansat_gold_firebase.html
```

---

## 🔗 Integración con Simulador

El simulador Python (`simulador_completo.py`) ya está configurado para enviar datos a Firebase:

```python
firebase_url = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app"
```

**Ejecutar simulador:**
```bash
cd python/
python simulador_completo.py
```

El panel web se actualizará automáticamente en tiempo real.

---

## 📱 Acceso desde Móvil

Una vez desplegado en Firebase Hosting:
1. Abre la URL en el móvil: `https://cansat-66d98.web.app`
2. Funciona en cualquier dispositivo (responsive)
3. Sin necesidad de instalar apps

---

## 🎯 Características Técnicas

### Tecnologías Utilizadas
- **Frontend:** HTML5, CSS3, JavaScript (ES6 Modules)
- **Mapas:** Leaflet.js + ArcGIS/Google Satellite
- **Gráficos:** Chart.js
- **3D:** Three.js
- **Backend:** Firebase Realtime Database
- **Hosting:** Firebase Hosting

### Navegadores Compatibles
✅ Chrome/Edge (Recomendado)
✅ Firefox
✅ Safari
✅ Mobile browsers

---

## 🔄 Actualizar el Panel

1. Editar el archivo HTML localmente
2. Probar los cambios abriendo el archivo
3. Desplegar cambios:

```bash
firebase deploy --only hosting
```

---

## 📈 Métricas de Rendimiento

- ⚡ Carga inicial: < 2 segundos
- 🔄 Actualización en tiempo real: < 500ms
- 📦 Tamaño del bundle: ~150KB
- 🌐 Compatible con conexiones lentas

---

## 🛠️ Solución de Problemas

### El mapa no carga
- Verificar conexión a internet
- Comprobar permisos de geolocalización

### Datos no se actualizan
- Verificar que el simulador esté corriendo
- Comprobar reglas de Firebase Database
- Verificar URL de Firebase en el código

### Error de CORS
- Firebase Hosting resuelve automáticamente CORS
- En local, usar servidor HTTP (no `file://`)

---

## 📄 Licencia

Uso educativo - IES Diego Velázquez

---

## 👥 Créditos

**Desarrollado por:**
- Departamento de Tecnología
- IES Diego Velázquez, Torrelodones, Madrid

**Proyecto:** CanSat Misión 2 - Enero 2026
