# ÍNDICE DE PRUEBAS FINALES — CANSAT CAELUM
## IES Diego Velázquez · Misión 2 · 2026

---

## Sensores integrados (Arduino Nano 33 BLE Sense Rev2)

| Prueba | Sensor | Resultado | Notas |
|--------|--------|-----------|-------|
| Inicialización BMI270 | Acelerómetro + Giroscopio | ✅ OK | Sin problemas |
| Inicialización BMM150 | Magnetómetro | ✅ OK | Sin problemas |
| Inicialización LPS22HB | Presión + Temperatura | ✅ OK | Sin problemas |
| Inicialización HS300x | Humedad + Temperatura | ✅ OK | Funciona correctamente |
| Inicialización APDS9960 | Luz + Proximidad | ✅ OK | Sin problemas |
| HTS221 | Humedad | ❌ No presente | Versión Lite sin HTS221 |

---

## Sensores externos

| Prueba | Sensor | Resultado | Notas |
|--------|--------|-----------|-------|
| Inicialización SCD40 | CO₂ + T + HR | ✅ OK | I2C, compensación de presión activa |
| Lecturas CO₂ SCD40 | CO₂ | ✅ OK | ~420 ppm en reposo |
| Inicialización HM3301 | PM1.0, PM2.5, PM10 | ✅ OK | I2C |
| Lecturas partículas HM3301 | PM2.5 | ✅ OK | Valores coherentes |
| GPS ATGM336H | Fix GPS | ✅ OK | UART, fix en exterior |

---

## Almacenamiento

| Prueba | Componente | Resultado | Notas |
|--------|-----------|-----------|-------|
| MicroSD inicialización | Adafruit MicroSD breakout | ✅ OK | SdFat — necesario para MBED |
| Escritura CSV | datos_SD_raw.csv | ✅ OK | 27 columnas, 1 muestra/segundo, datos crudos |
| Backup RAM | Buffer interno | ✅ OK | Solo durante DESCENSO, cada 2 segundos |
| Extracción RAM | extraer_ram.py | ✅ OK | Via serial tras aterrizaje |

---

## Comunicación

| Prueba | Componente | Resultado | Notas |
|--------|-----------|-----------|-------|
| APC220 — configuración | Módulo RF 434 MHz | ⚠️ Pendiente | Ver IMPORTANTE_CAMBIO_FRECUENCIA.md |
| APC220 — envío telemetría | receptor_telemetria.py | ⚠️ Pendiente | Requiere fix frecuencia |
| USB Serial | Monitor Arduino IDE | ✅ OK | 9600 baud |

---

## Sistema completo

| Prueba | Descripción | Resultado | Notas |
|--------|-------------|-----------|-------|
| Detección de fases | espera → caida_libre → apertura → descenso → tierra | ✅ OK | Requiere 3 muestras consecutivas accel < 50mG para salir de espera |
| Programa completo | CANSAT_VUELO_INTEGRADO.ino | ✅ OK | Todos los sensores funcionando |
| Alimentación 9V | Batería + TP4056 | ✅ OK | Regulado a 3.3V |
| Simulador datos | simulador_inversion_termica.py | ✅ OK | Genera datos_simulacion.csv |
| Análisis post-vuelo | analizar_vuelo.py | ✅ OK | 4 gráficas + mapa + informe |
| KML Google Earth | generar_kml.py | ✅ OK | Trayectoria 3D con cortina PM2.5 |
| Dashboard Firebase | caelum_dashboard.html | ✅ OK | https://cansat-66d98.web.app |
| Playback datos | caelum_playback.py | ✅ OK | Detecta SD / radio / simulacion |

---

## Problemas resueltos

| Problema | Solución |
|---------|---------|
| HTS221 no inicializa | Versión Lite sin sensor — eliminado del código |
| Puerto COM no detectado | Instalar driver CH340 + Arduino Mbed OS Nano Boards |
| Librería SD incompatible | Usar SdFat en vez de SD estándar (MBED) |
| Firebase acumula datos espera | receptor_telemetria.py filtra fases activas |
| Firebase error 400 al limpiar | limpiar_firebase.py con batch deletion |

---

**Última actualización:** Febrero 2026
