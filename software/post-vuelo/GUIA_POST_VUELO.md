# GUÍA POST-VUELO — CanSat CAELUM
**IES Diego Velázquez · Misión 2 · Detección de Firmas de Combustión**

---

## Resumen del Sistema de Datos

El CanSat guarda los datos en **tres lugares simultáneamente**:

| Fuente | Fichero | Cuándo usar |
|--------|---------|-------------|
| **MicroSD** | `datos_SD.csv` | **Siempre** — fuente principal, máxima resolución |
| **RAM backup** | `datos_RAM.csv` | Si la SD falla — fuente de emergencia |
| **Telemetría radio** | `datos_radio.csv` | **Si no se recupera el CanSat** |

> ⚠️ La RAM backup se pierde si se apaga el Arduino. La SD conserva los datos aunque la batería se agote.

> ⚠️ **`datos_radio.csv` es el seguro crítico.** Si el CanSat cae en un lugar inaccesible (tejado, árbol, agua...) los datos de la SD y la RAM se pierden para siempre. Pero `datos_radio.csv` ya está en el PC de tierra desde el momento del aterrizaje. Por eso `receptor_telemetria.py` debe estar corriendo **siempre** durante el vuelo.

---

## 1. Recuperación del CanSat

### Pasos inmediatos al encontrarlo:

1. **No apagar el Arduino** — la RAM backup sigue activa
2. Comprobar que la batería tiene carga (LED verde encendido)
3. Llevar el portátil al lugar de recuperación si es posible
4. Si la batería está muy baja, **extraer la SD card primero**

---

## 2. Extraer Datos de la SD Card (Fuente Principal)

### Material necesario:
- Lector de tarjetas MicroSD (o adaptador SD)
- Ordenador

### Pasos:

1. **Apagar el CanSat** con seguridad (esperar a que el LED se apague)
2. **Extraer la MicroSD** del módulo Adafruit
3. **Insertar** en el lector de tarjetas del ordenador
4. Buscar el archivo **`datos_SD.csv`** en la raíz de la tarjeta
5. **Copiar** `datos_SD.csv` a tu ordenador

### Verificar que el CSV es correcto:

Abrir en Excel o Google Sheets y comprobar:
- ✅ Primera fila es la cabecera con 25 columnas
- ✅ Los números tienen sentido (altitud entre 0–1100 m, CO₂ entre 400–600 ppm)
- ✅ El timestamp aumenta progresivamente
- ✅ La columna `fase` pasa por: `espera → caida_libre → apertura → descenso → tierra`

**Cabecera esperada (25 columnas):**
```
timestamp, datetime, lat, lon, alt, alt_mar, sats,
temp_hs, hum_hs, temp_scd, hum_scd, temp_lps, presion,
co2, pm1_0, pm2_5, pm10,
accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, fase
```

---

## 3. Extraer RAM Backup (Solo si la SD Falló)

Si `datos_SD.csv` no existe o está vacío, usar el backup de RAM.

### Material necesario:
- Cable USB
- Ordenador con Python instalado

### Pasos:

1. **Conectar** el CanSat al ordenador por USB (**sin apagarlo antes**)
2. Verificar en qué puerto está (Administrador de dispositivos → Puertos COM)
3. Si es distinto de COM3, editar `extraer_ram.py` y cambiar:
   ```python
   PUERTO = 'COM3'   # ← cambiar al puerto correcto
   ```
4. **Ejecutar:**
   ```bash
   python extraer_ram.py
   ```
   El script envía `CSV_RAM` automáticamente, captura la respuesta y guarda `datos_RAM.csv`:
   ```
   ✅ Conectado a COM3
   📤 Enviando comando CSV_RAM...
   📥 Recibiendo datos...
      [  10 muestras recibidas]
      [  20 muestras recibidas]
      ...
   ✅ EXTRACCIÓN COMPLETADA — 185 muestras → datos_RAM.csv
   ```
5. Para limpiar la RAM después de exportar: escribir `BORRAR_RAM` en el Monitor Serie de Arduino IDE.

> ⚠️ La RAM guarda ~350 muestras a 2 segundos/muestra (~11 min). Menos resolución que la SD (1 muestra/segundo) pero suficiente para el análisis científico.

> ⚠️ Conectar el Arduino por USB puede hacer reset — el script espera 3 segundos automáticamente antes de enviar el comando.

---

## 4. Análisis de Datos

### Instalación de dependencias (solo la primera vez):

```bash
pip install pandas numpy folium matplotlib
```

### Preparar el entorno:

```bash
# Copiar el CSV a la carpeta del script
cp datos_SD.csv software/post_vuelo/python/

# Ir a la carpeta
cd software/post_vuelo/python/
```

### Ejecutar el análisis:

```bash
python analizar_vuelo.py <fichero.csv>
```

El script genera automáticamente la carpeta `analisis_vuelo/` con:

```
analisis_vuelo/
├── graf_1_perfil_vertical.png      → Perfiles PM + CO₂ + temperatura por altitud
├── graf_2_inversiones_termicas.png → Detección de capas e inversiones
├── graf_3_validacion_cruzada.png   → Comparativa de los 3 sensores de temperatura
├── graf_4_mision_primaria.png      → Altitud, presión, velocidad, trayectoria GPS
├── mapa_vuelo.html                 → Mapa interactivo con trayectoria y PM2.5
└── informe_vuelo.txt               → Resumen estadístico completo
```

---

## 4b. Visualizar Trayectoria en Google Earth (KML)

Si el CanSat tenía fix GPS, puedes ver la trayectoria en 3D sobre el terreno real.

### Ejecutar:

```bash
python generar_kml.py <fichero.csv>
```

Genera `analisis_vuelo/trayectoria_vuelo.kml`

### Abrir en Google Earth:

1. Abrir **Google Earth** (descarga gratuita en earth.google.com)
2. **Archivo → Abrir** → seleccionar `trayectoria_vuelo.kml`
3. La trayectoria aparece sobre el terreno con altitud real en 3D
4. Hacer clic en cualquier punto para ver altitud, PM2.5, CO₂ y temperatura

La trayectoria está **coloreada por PM2.5**:
- 🟢 Verde → aire limpio
- 🟡 Amarillo → zona urbana normal
- 🟠 Naranja → moderada
- 🔴 Rojo → mala / muy mala

> ⚠️ Si el CSV no tiene coordenadas GPS válidas (lat/lon = 0) el KML no se genera.

---

## 5. Reproducir el Vuelo en el Panel Web

Para ver los datos en el dashboard en tiempo real (modo replay):

1. Subir `datos_SD.csv` a Google Colab
2. Ejecutar `caelum_playback.py`
3. Abrir el dashboard: https://cansat-66d98.web.app
4. Seleccionar **REPLAY VUELO**

```bash
# En Colab o local
python caelum_playback.py
```

---

## 6. Interpretación de Resultados

### CO₂ — Confirmación de sensor y atmósfera

A ~1000 m de altitud el CO₂ atmosférico es siempre **~420 ppm** (fondo atmosférico global, troposfera bien mezclada). Las fuentes de combustión del suelo no son detectables a esa altura.

| Lectura CO₂ | Interpretación |
|-------------|----------------|
| ~420 ppm constante durante todo el vuelo | ✅ Sensor funcionando — atmósfera normal |
| Variación > 30 ppm entre altitudes | ⚠️ Posible ruido de sensor (precisión SCD40 = ±10 ppm) |

> El valor principal del SCD40 en este proyecto es su **temperatura y humedad** para la validación cruzada con HS300x y LPS22HB, no el CO₂.

---

### PM2.5 — Perfil vertical e inversiones térmicas

| PM2.5 (µg/m³) | Calidad OMS | Causa probable |
|---------------|-------------|----------------|
| 0–12 | 🟢 Excelente | Aire limpio |
| 12–35 | 🟢 Buena | Zona urbana normal |
| 35–55 | 🟡 Moderada | Tráfico moderado |
| 55–150 | 🟠 Mala | Tráfico intenso, industria |
| >150 | 🔴 Muy Mala | Humo, incendio cercano |

**Patrón de inversión térmica** (buscar en `graf_2_inversiones_termicas.png`):
```
Altitud ↑ + Temperatura ↑ (en vez de bajar) + PM2.5 ↑
              ↓
  Capa de partículas atrapadas
              ↓
  Al bajar la temperatura nocturna, la capa desciende a nivel del suelo
              ↓
  Riesgo real: alertas AQI, ataques de asma en Madrid
```

---

### Validación cruzada de temperatura (graf_3)

Tres sensores miden temperatura de forma independiente:

| Sensor | Variable | Comportamiento esperado |
|--------|----------|------------------------|
| HS300x | `temp_hs` | Referencia principal |
| SCD40 | `temp_scd` | Diferencia < 1 °C respecto a HS300x |
| LPS22HB | `temp_lps` | Puede leer +0.3–0.5 °C más por calor del procesador |

- **ΔT < 2 °C** entre HS300x y SCD40 → sensores funcionando correctamente
- **ΔT > 3 °C** → posible fallo de sensor o gradiente térmico real en el CanSat

---

### Firmas de combustión

A la altitud de vuelo (~1000 m) el CO₂ es siempre ~420 ppm constante — no indica combustión directamente. Lo relevante es si **varía con la altitud**, combinado con el PM2.5:

```
CO₂ CONSTANTE + PM2.5 BAJO en todo el perfil    → Aire limpio ✓
CO₂ CONSTANTE + PM2.5 ALTO en capas bajas       → Polvo o tráfico sin inversión
CO₂ VARIABLE  + PM2.5 ALTO en una capa concreta → Inversión térmica atrapando gases y partículas
CO₂ VARIABLE  + PM2.5 BAJO                      → Capas diferenciadas sin fuente local
```

---

## 7. Solución de Problemas

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| `datos_SD.csv` no existe | SD no se inicializó | Usar RAM backup (`CSV_RAM`) |
| CSV con menos de 25 columnas | Versión antigua del firmware | Verificar que subiste `CANSAT_VUELO_INTEGRADO.ino` actualizado |
| CO₂ = 0 en todas las filas | SCD40 no respondió | Normal si el sensor tardó en calentarse. Las primeras 5s son 0 |
| GPS lat/lon = 0 | Sin fix GPS | Normal si el vuelo fue sin cielo despejado. Las gráficas funcionan sin GPS |
| `temp_lps` siempre ~0.5°C más alta | Calor del procesador | Normal y esperado — no es un error |
| ΔT > 3°C entre HS300x y SCD40 | Fallo de sensor o condensación | Revisar conexiones I2C del SCD40 |
| PM2.5 = 0 durante todo el vuelo | HM3301 no respondió | Verificar conexión I2C (0x40) y alimentación 3.3V |
| `analizar_vuelo.py` da error | Columnas incorrectas | Verificar cabecera del CSV con Excel |

---

## 8. Comandos del CanSat (Monitor Serie a 115200 baud)

| Comando | Función |
|---------|---------|
| `CSV_RAM` | Exporta todos los datos guardados en RAM en formato CSV |
| `BORRAR_RAM` | Limpia la memoria RAM (hacer DESPUÉS de exportar) |

> La SD card se gestiona automáticamente — no necesita comandos.

---

## 9. Checklist Post-Vuelo

```
[ ] CanSat localizado y recuperado
[ ] Batería comprobada (LED verde)
[ ] Arduino NO apagado hasta exportar RAM si es necesario
[ ] SD card extraída
[ ] datos_SD.csv copiado al ordenador
[ ] datos_SD.csv verificado en Excel (25 columnas, datos coherentes)
[ ] Si SD vacía: RAM exportada con CSV_RAM y guardada
[ ] Script analizar_vuelo.py ejecutado correctamente
[ ] graf_1_perfil_vertical.png revisada (¿hay capas de PM2.5?)
[ ] graf_2_inversiones_termicas.png revisada (¿hay inversión térmica?)
[ ] graf_3_validacion_cruzada.png revisada (ΔT < 2°C entre sensores)
[ ] mapa_vuelo.html abierto y trayectoria verificada
[ ] informe_vuelo.txt leído y guardado
[ ] Datos subidos a Firebase con caelum_playback.py (opcional)
[ ] Dashboard verificado en https://cansat-66d98.web.app
```

---

**Equipo:** CAELUM
**Centro:** IES Diego Velázquez
**Proyecto:** CanSat Misión 2 — Detección de Firmas de Combustión
**Fecha:** Febrero 2026
