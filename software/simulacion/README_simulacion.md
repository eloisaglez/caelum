# Simuladores Pre-Vuelo — CanSat CAELUM

Estos simuladores generan datos de vuelo sintéticos para dos propósitos:

1. **Validar `analizar_vuelo.py`** — comprobar que el análisis detecta correctamente inversiones térmicas y perfiles de PM2.5 antes del vuelo real
2. **Probar el dashboard** — `caelum_playback.py` detecta `datos_simulacion.csv` automáticamente y lo envía a Firebase `/simulacion` para visualizar en el panel web

---

## Simuladores disponibles

| Archivo | Escenario | Resultado esperado en `analizar_vuelo.py` |
|---------|-----------|-------------------------------------------|
| `simulador_inversion_termica.py` | PM2.5 alto en capa 200–350 m, gradiente térmico invertido | Detecta inversión térmica ✓ |
| `simulador_sin_contaminacion.py` | PM2.5 bajo y uniforme, gradiente normal | No detecta ninguna inversión ✓ |

---

## Uso

### 1. Generar datos simulados

```bash
# Escenario con inversión térmica
python simulador_inversion_termica.py

# Escenario sin contaminación
python simulador_sin_contaminacion.py
```

Ambos generan `datos_simulacion.csv` en la carpeta actual.

### 2. Analizar los datos simulados

```bash
python ../post_vuelo/analizar_vuelo.py datos_simulacion.csv
```

Verifica que las gráficas muestran el escenario correcto.

### 3. Visualizar en el dashboard

```bash
# Copiar datos_simulacion.csv a la carpeta del playback
python ../vuelo/panel_web/caelum_playback.py
```

Abre https://cansat-66d98.web.app y selecciona **SIMULACIÓN**.

---

## Notas

- CO₂ es ~420 ppm constante en ambos simuladores — refleja el comportamiento real a ~1000 m
- La única diferencia entre los dos escenarios es el perfil de PM2.5 y la temperatura
- Los datos de GPS son sintéticos basados en coordenadas de Brunete (Madrid)
