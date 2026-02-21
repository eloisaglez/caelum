# CHECKLIST GITHUB — CANSAT CAELUM
## IES Diego Velázquez · Misión 2

---

## Estructura del repositorio

```
cansat-caelum/
│
├── README.md
├── requirements.txt
│
├── software/
│   ├── pruebas/                        # Programas de prueba de sensores
│   ├── vuelo/                          # Programa principal + panel web
│   │   ├── CANSAT_VUELO_INTEGRADO.ino
│   │   └── panel_web/
│   │       ├── caelum_dashboard.html
│   │       ├── caelum_playback.py
│   │       ├── receptor_telemetria.py
│   │       └── limpiar_firebase.py
│   ├── post_vuelo/                     # Análisis post-vuelo
│   │   ├── analizar_vuelo.py
│   │   ├── generar_kml.py
│   │   ├── extraer_ram.py
│   │   ├── GUIA_POST_VUELO.md
│   │   ├── GUIA_RAPIDA_POST_VUELO.txt
│   │   └── README_post_vuelo.md
│   └── simulacion/                     # Simuladores pre-vuelo
│       ├── simulador_inversion_termica.py
│       ├── simulador_sin_contaminacion.py
│       └── README_simulacion.md
│
├── documentation/
│   └── ...
│
└── data/                               # Datos de vuelo (no subir CSVs reales)
    └── .gitkeep
```

---

## Archivos a verificar antes de subir

### Arduino
- [ ] `CANSAT_VUELO_INTEGRADO.ino` — código principal del CanSat
- [ ] Librerías necesarias documentadas en README

### Python — Vuelo
- [ ] `caelum_playback.py` — reproduce CSV en Firebase
- [ ] `receptor_telemetria.py` — recibe telemetría APC220
- [ ] `extraer_ram.py` — extrae backup RAM por serial
- [ ] `limpiar_firebase.py` — limpia datos de Firebase

### Python — Post-vuelo
- [ ] `analizar_vuelo.py` — análisis completo post-vuelo
- [ ] `generar_kml.py` — trayectoria 3D para Google Earth

### Python — Simulación
- [ ] `simulador_inversion_termica.py`
- [ ] `simulador_sin_contaminacion.py`

### Panel web
- [ ] `caelum_dashboard.html` — desplegado en Firebase Hosting

### Documentación
- [ ] `README.md` — actualizado
- [ ] `requirements.txt` — actualizado
- [ ] `README_post_vuelo.md`
- [ ] `README_simulacion.md`
- [ ] `GUIA_POST_VUELO.md`
- [ ] `GUIA_RAPIDA_POST_VUELO.txt`

---

## .gitignore recomendado

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo

# Datos de vuelo (no subir datos reales al repositorio)
data/*.csv
!data/.gitkeep
analisis_vuelo/

# Sistema
.DS_Store
Thumbs.db

# IDEs
.vscode/
.idea/

# Firebase
.firebase/
firebase-debug.log
```

---

## Instalación para quien clone el repositorio

```bash
git clone https://github.com/tu-usuario/cansat-caelum.git
cd cansat-caelum
pip install -r requirements.txt
```

### Probar con simulador
```bash
cd software/simulacion
python simulador_inversion_termica.py
cd ../post_vuelo
python analizar_vuelo.py ../simulacion/datos_simulacion.csv
python generar_kml.py ../simulacion/datos_simulacion.csv
```

---

## Panel web

Desplegado en Firebase Hosting:
**https://cansat-66d98.web.app**

Para desplegar cambios:
```bash
firebase deploy --only hosting
```
