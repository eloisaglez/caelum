# CHECKLIST DÍA DE VUELO — CANSAT CAELUM
## IES Diego Velázquez · Misión 2 · 2026

---

## La noche antes

- [ ] Cargar batería 9V ion litio completamente
- [ ] Verificar que `CANSAT_VUELO_INTEGRADO.ino` está subido al Arduino
- [ ] Comprobar que la MicroSD está formateada (FAT32) y vacía
- [ ] Instalar MicroSD en el módulo Adafruit
- [ ] Actualizar presión de referencia en el código según AEMET (www.aemet.es)
- [ ] Cargar portátil de tierra completamente
- [ ] Verificar que `receptor_telemetria.py` funciona con el APC220
- [ ] Tener `caelum_playback.py` y `analizar_vuelo.py` listos en el portátil

---

## En el aeródromo — antes del montaje

- [ ] Verificar presión atmosférica actual (AEMET o Windy.com)
- [ ] Actualizar `seaLevelPressure` en el código si ha cambiado
- [ ] Comprobar fix GPS en exterior (puede tardar 1-2 minutos)
- [ ] Verificar comunicación APC220 entre CanSat y portátil de tierra
- [ ] Arrancar `receptor_telemetria.py` en el portátil de tierra
- [ ] Comprobar que Firebase recibe datos correctamente

---

## Montaje del CanSat

- [ ] Conectar batería 9V al TP4056
- [ ] Verificar LED verde encendido (alimentación OK)
- [ ] Comprobar que todos los sensores inicializan (Monitor Serial)
- [ ] Verificar que se crea `datos_SD.csv` en la MicroSD
- [ ] Comprobar telemetría APC220 llegando al portátil
- [ ] Cerrar carcasa del CanSat
- [ ] Verificar paracaídas correctamente plegado y conectado

---

## Lanzamiento

- [ ] `receptor_telemetria.py` corriendo en el portátil — **NO CERRAR**
- [ ] Dashboard abierto en https://cansat-66d98.web.app
- [ ] Confirmar que el CanSat está en fase `espera`
- [ ] Anotar hora de lanzamiento
- [ ] Anotar coordenadas GPS de la zona de lanzamiento

---

## Tras el aterrizaje

- [ ] Localizar el CanSat
- [ ] Anotar coordenadas GPS de aterrizaje
- [ ] Detener `receptor_telemetria.py` — guardar `datos_radio.csv`
- [ ] Extraer MicroSD — copiar `datos_SD.csv` al portátil
- [ ] Conectar Arduino por USB — ejecutar `extraer_ram.py` para obtener `datos_RAM.csv`
  - La RAM solo graba durante el DESCENSO — es normal que tenga menos registros que la SD
- [ ] Verificar que los tres ficheros tienen datos:
  - [ ] `datos_SD.csv`
  - [ ] `datos_RAM.csv`
  - [ ] `datos_radio.csv`

---

## Análisis post-vuelo

- [ ] Ejecutar `python limpiar_espera.py datos_SD_raw.csv` → genera `datos_SD.csv`
- [ ] Ejecutar `python analizar_vuelo.py datos_SD.csv`
- [ ] Revisar gráficas generadas en `analisis_vuelo/`
- [ ] Ejecutar `python generar_kml.py datos_SD.csv`
- [ ] Abrir `trayectoria_vuelo.kml` en Google Earth
- [ ] Ejecutar `caelum_playback.py` para reproducir en el dashboard

---

## ⚠️ Si no se recupera el CanSat

- `datos_radio.csv` es el único dato disponible
- Ejecutar `python analizar_vuelo.py datos_radio.csv`
- Ejecutar `python generar_kml.py datos_radio.csv`

---

**Ver también:** `IMPORTANTE_CAMBIO_FRECUENCIA.md` para configuración APC220
