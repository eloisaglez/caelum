# GUÍA POST-VUELO - CanSat CAELUM

## Resumen

Esta guía describe los pasos a seguir después de recuperar el CanSat para extraer, analizar y visualizar los datos del vuelo.

---

## 1. Recuperación del CanSat

### ⚠️ IMPORTANTE: Actuar rápido

Los datos están en la RAM del Arduino. **Si se agota la batería, se pierden.**

**Tiempo estimado de batería:**
- Pila 9V estándar: ~2-3 horas
- LiPo 3.7V 2000mAh: ~4-5 horas

### Pasos:
1. Localizar el CanSat
2. **NO apagarlo** hasta exportar los datos
3. Llevar el portátil al lugar de recuperación si es posible

---

## 2. Exportar Datos del CanSat

### Equipamiento necesario:
- Cable USB
- Ordenador con Arduino IDE

### Pasos:

1. **Conectar** el CanSat al ordenador por USB

2. **Abrir Arduino IDE** → Herramientas → Monitor Serie

3. **Configurar** a 9600 baud

4. **Escribir** `ESTADO` y pulsar Enter
   ```
   === ESTADO ===
   Grabando: NO
   Registros: 185/500
   Altitud inicial: 620.5 m
   Altitud actual: 622.1 m
   ```

5. **Escribir** `CSV` y pulsar Enter
   ```
   === INICIO CSV ===
   
   equipo,paquete,timestamp,lat,lon,altGPS,sats,temp,hum,pres,altBaro,tvoc,eco2,h2,ethanol,accX,accY,accZ,gyrX,gyrY,gyrZ
   CAELUM,1,1000,40.579500,-3.918400,498,8,22.50,65.00,1013.25,497,412,850,13500,17200,0.05,-0.02,9.80,1.2,-0.5,0.3
   ...
   
   === FIN CSV ===
   ```

6. **Seleccionar** todo el texto CSV (desde la cabecera hasta el último dato)

7. **Copiar** (Ctrl+C)

8. **Abrir Bloc de notas** (o cualquier editor de texto)

9. **Pegar** (Ctrl+V)

10. **Guardar como** `datos_vuelo.csv`

---

## 3. Verificar Datos

Antes de analizar, verificar que el CSV es correcto:

1. **Abrir** `datos_vuelo.csv` en Excel o Google Sheets

2. **Verificar:**
   - ¿Hay cabecera con nombres de columnas?
   - ¿Los números tienen sentido?
   - ¿Hay coordenadas GPS válidas (no 0,0)?
   - ¿El timestamp aumenta correctamente?

3. **Problemas comunes:**
   - Líneas cortadas → Reconectar y exportar de nuevo
   - GPS en 0,0 → Normal si no había señal
   - TVOC en 0 → El sensor necesita calibración

---

## 4. Análisis de Datos

### Preparación:

```bash
# Instalar dependencias (solo la primera vez)
pip install pandas numpy folium matplotlib seaborn simplekml

# Ir a la carpeta de scripts
cd analisis_post_vuelo/scripts

# Copiar el CSV aquí
cp /ruta/datos_vuelo.csv .
```

### Ejecutar análisis:

```bash
# Análisis completo (mapa de calor + gráficas)
python analizar_mision2.py

# Mapa de cortinas de humo
python mapa_cortina.py

# KML para Google Earth
python generar_kml.py
```

---

## 5. Visualizar Resultados

### Mapas HTML

1. Abrir `mapa_calor_cansat.html` en el navegador
2. Hacer clic en los marcadores para ver detalles
3. Usar el control de capas (esquina superior derecha)

### Google Earth

1. Abrir Google Earth
2. Archivo → Abrir → `firmas_combustion_3d.kml`
3. Navegar en 3D para ver los cilindros

### Gráficas

- `analisis_cansat.png` contiene 4 gráficas:
  - Evolución TVOC vs tiempo
  - Correlación TVOC vs eCO2
  - Distribución de valores TVOC
  - Señales H2/Ethanol (firmas)

---

## 6. Interpretación de Resultados

### Clasificación de Calidad del Aire

| TVOC (ppb) | Calidad | Significado |
|------------|---------|-------------|
| 0-220 | 🟢 Excelente | Aire limpio, sin contaminación |
| 220-660 | 🟡 Buena | Niveles normales, zona residencial |
| 660-2200 | 🟠 Moderada | Cerca de carreteras o industrias |
| 2200-5500 | 🔴 Mala | Fuente de contaminación cercana |
| >5500 | ⛔ Muy Mala | Peligroso, fuente directa |

### Firmas de Combustión

El CanSat puede identificar **qué tipo de fuente** causó la contaminación:

| Firma | Indicadores | Causa típica |
|-------|-------------|--------------|
| 🚜 Generador Diésel | TVOC>1000, H2>13000 | Generadores eléctricos |
| 🔥 Biomasa | TVOC>500, Ethanol>18000 | Quema de vegetación, barbacoas |
| 🚗 Tráfico | TVOC 300-800, eCO2>1000 | Carreteras, aparcamientos |
| 🌿 Aire Limpio | TVOC<100 | Zonas sin actividad |
| 🏭 Industrial | Variable | Fábricas, talleres |

---

## 7. Generar Informe

Con los datos analizados, puedes generar un informe incluyendo:

1. **Resumen del vuelo**
   - Duración
   - Altitud máxima/mínima
   - Número de muestras

2. **Mapa de contaminación**
   - Captura del mapa de calor
   - Zonas identificadas

3. **Firmas detectadas**
   - Tipos de fuentes encontradas
   - Ubicación de cada una

4. **Conclusiones**
   - Calidad del aire general
   - Fuentes principales de contaminación
   - Comparación con datos esperados

---

## 8. Comandos del CanSat

| Comando | Función |
|---------|---------|
| `CSV` | Exportar datos en formato CSV |
| `ESTADO` | Ver registros guardados y estado |
| `LEER` | Mostrar datos resumidos |
| `BORRAR` | Eliminar todos los datos |
| `GRABAR` | Forzar inicio de grabación |
| `PARAR` | Detener grabación |

---

## 9. Solución de Problemas

| Problema | Solución |
|----------|----------|
| No aparece nada en Monitor Serie | Verificar 9600 baud, pulsar RESET |
| CSV incompleto | Aumentar buffer del Monitor Serie |
| GPS en 0,0 | Normal si no había señal |
| Pocos registros | Verificar umbral de altitud |
| Datos perdidos | La batería se agotó antes de exportar |

---

## 10. Checklist Post-Vuelo

```
[ ] CanSat recuperado
[ ] Conectado por USB
[ ] Monitor Serie abierto (9600 baud)
[ ] Comando ESTADO ejecutado
[ ] Comando CSV ejecutado
[ ] Datos copiados y guardados como CSV
[ ] Scripts de análisis ejecutados
[ ] Mapas generados y revisados
[ ] Informe preparado
```

---

**Equipo:** CAELUM  
**Centro:** IES Diego Velázquez  
**Proyecto:** CanSat Misión 2  
**Fecha:** Febrero 2026
