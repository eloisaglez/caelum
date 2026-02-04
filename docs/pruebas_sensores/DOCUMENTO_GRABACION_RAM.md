# Sistema de Grabación en RAM - CanSat

## Descripción

El Arduino Nano 33 BLE tiene problemas conocidos de compatibilidad con módulos MicroSD. Como alternativa, este sistema guarda los datos del vuelo en la memoria RAM del microcontrolador.

**Capacidad:** 500 registros (~8 minutos a 1 registro/segundo)

---

## Programas Disponibles

### 1. PROGRAMA_CANSAT_RAM_OPTIMIZADO.ino
**Uso:** Pruebas manuales

Permite grabar y exportar datos mediante comandos por el Monitor Serie.

**Comandos:**
| Comando | Función |
|---------|---------|
| `GRABAR` | Inicia grabación |
| `PARAR` | Detiene grabación |
| `LEER` | Muestra datos resumidos |
| `CSV` | Exporta datos en formato CSV |
| `ESTADO` | Muestra registros guardados |
| `BORRAR` | Borra todos los datos |

### 2. PROGRAMA_CANSAT_VUELO_AUTO.ino
**Uso:** Vuelo real

Graba automáticamente cuando detecta altitud >30m sobre el punto inicial.

**Estados del LED:**
| LED | Estado |
|-----|--------|
| Fijo | Calibrando (5 seg al encender) |
| Parpadeo lento | Esperando lanzamiento |
| Parpadeo rápido | Grabando |
| Fijo | Vuelo terminado |

---

## Uso para Pruebas (Manual)

1. Cargar `PROGRAMA_CANSAT_RAM_OPTIMIZADO.ino`
2. Abrir Monitor Serie a **9600 baud**
3. Escribir `GRABAR` → Empieza a grabar
4. Esperar el tiempo deseado
5. Escribir `PARAR` → Detiene grabación
6. Escribir `CSV` → Muestra datos en formato CSV
7. Copiar el texto y guardar como archivo `.csv`

---

## Uso para Vuelo Real (Automático)

### Antes del vuelo:
1. Cargar `PROGRAMA_CANSAT_VUELO_AUTO.ino`
2. Encender el CanSat en tierra
3. Esperar 5 segundos (calibra altitud inicial)
4. LED parpadea lento = listo para lanzamiento

### Durante el vuelo:
- El sistema detecta automáticamente cuando sube >30m
- LED parpadea rápido = grabando
- Graba 1 registro por segundo
- Para automáticamente al aterrizar o llenar memoria

### Después del vuelo:
1. Conectar el CanSat por USB
2. Abrir Monitor Serie a **9600 baud**
3. Escribir `CSV` y pulsa Enter
4. Seleccionar todo el texto CSV
5. Copiar (Ctrl+C)
6. Abrir Bloc de notas
7. Pegar (Ctrl+V)
8. Guardar como `datos_vuelo.csv`

---

## Formato de Datos CSV

### Programa de pruebas:
```csv
timestamp,temp,hum,pres,alt,co2,lat,lon,altGPS,sat,accX,accY,accZ
1000,22.50,65.00,1013.25,498,412,40.579500,-3.918400,497,8,0.05,-0.02,9.80
2000,22.45,65.10,1013.30,497,408,40.579510,-3.918390,496,8,0.03,-0.01,9.81
```

### Programa de vuelo:
```csv
timestamp,temp,presion,altitud,accX,accY,accZ
1000,22.50,1013.25,498,0.05,-0.02,9.80
2000,22.45,1013.30,497,0.03,-0.01,9.81
```

---

## Datos Guardados

| Campo | Descripción | Unidad |
|-------|-------------|--------|
| timestamp | Tiempo desde inicio | ms |
| temp | Temperatura | °C |
| hum | Humedad | % |
| pres/presion | Presión atmosférica | hPa |
| alt/altitud | Altitud calculada | m |
| co2 | CO2 equivalente | ppm |
| lat | Latitud | grados |
| lon | Longitud | grados |
| altGPS | Altitud GPS | m |
| sat | Satélites GPS | - |
| accX/Y/Z | Aceleración | g |

---

## Limitaciones

- **500 registros máximo** (~8 minutos)
- **Los datos se pierden al apagar** si no se exportan antes
- No hay respaldo físico (a diferencia de MicroSD)

---

## Análisis de Datos

Después de guardar el archivo `.csv`, puedes usar los scripts de Python:

```bash
cd analisis_post_vuelo/scripts
python analizar_mision2.py
```

O abrir directamente en Excel/Google Sheets.

---

## Solución de Problemas

| Problema | Solución |
|----------|----------|
| No aparece nada en Monitor Serie | Verificar 9600 baud, pulsar RESET |
| "No hay datos" | Ejecutar GRABAR antes de CSV |
| Memoria llena | Ejecutar BORRAR para limpiar |
| LED no parpadea | Verificar carga del programa |
| Error de compilación memoria | Usar programa optimizado (500 registros) |

---

## ¿Por qué no MicroSD?

El Arduino Nano 33 BLE (chip nRF52840) tiene problemas conocidos de compatibilidad con módulos MicroSD estándar. Esto se debe a diferencias en la implementación del bus SPI. 

La grabación en RAM es una alternativa fiable que:
- No requiere hardware adicional
- Funciona siempre
- Es suficiente para la duración del vuelo (~10 min)

---

## Notas

- El programa de vuelo automático usa el sensor de presión LPS22HB integrado
- La altitud se calcula con la fórmula barométrica estándar
- El umbral de 30m evita falsas activaciones en tierra

---

**Autor:** IES Diego Velázquez  
**Proyecto:** CanSat Misión 2  
**Fecha:** Febrero 2026
