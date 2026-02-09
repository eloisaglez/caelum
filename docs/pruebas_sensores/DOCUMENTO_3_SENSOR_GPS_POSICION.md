# 📋 DOCUMENTO 3: INTEGRACIÓN SENSOR GPS - POSICIÓN Y ALTITUD

## Objetivo
Integrar GPS para obtener coordenadas (lat/lon), altitud y número de satélites.

---

## 📡 SENSOR GPS - ESPECIFICACIONES

```
Modelo: ATGM336H (o compatible)
Protocolo: UART (comunicación serie)
Velocidad: 9600 baud (por defecto)
Salida: Sentencias NMEA ($GPRMC, $GPGGA, etc)
Función: Latitud, Longitud, Altitud, Satélites
```
---

## 🔌 CONEXIÓN FÍSICA

### Pines Arduino Nano 33 BLE

```
GPS ATGM336H:
VCC (rojo)     → Arduino 3.3V
GND (negro)    → Arduino GND
TX (amarillo)  → Arduino D0 (RX)
RX (verde)     → Arduino D1 (TX)
```

🔌 CONEXIÓN FÍSICA Y SEGURIDAD

    ⚠️ ADVERTENCIA DE CARGA: Si el GPS está conectado a los pines D0/D1 (Serial1), 
    es posible que el programa no se cargue correctamente. Si obtienes un error de 
    "Upload failed", desconecta el pin TX del GPS (Pin D0) antes de subir el código.

    ⚠️ NOTA DE SEGURIDAD PARA LA CARGA DE CÓDIGO (IMPORTANTE)

   Protocolo recomendado si falla la carga:

       Desconectar el cable TX del GPS (el que va al pin D0 de Arduino) antes de pulsar 'Subir'.
       Una vez que el IDE confirme 'Subido con éxito', volver a conectar el cable.
       Si el error persiste o se necesita usar SoftwareSerial por comodidad, se puede desplazar 
       el GPS a los pines D5 y D6 (dejando D2/D3 exclusivos para la antena APC220).

    PLAN B (Si el error de carga persiste):

        Mover el GPS a los pines D5 y D6 usando Serial1 para evitar interferencias totales con el 
        sistema de carga de la placa.
---

## 📥 INSTALACIÓN LIBRERÍAS

```
Sketch → Include Library → Manage Libraries

No necesita librería especial
- Wire.h → Incluida por defecto
- SoftwareSerial.h → Incluida por defecto
- Usamos parseo manual de NMEA
```

---

## ✅ VERIFICACIÓN GPS

Antes de integrar, verifica que envía datos:

**Programa:** `software/pruebas/PROGRAMA_4_GPS_POSICION_PRUEBAS.ino

Si NO se ven datos → Revisar conexión TX/RX

---

## 💻 PROGRAMA PRUEBA GPS

**Archivo:** `software/pruebas/DOCUMENTO_3_SENSOR_GPS_POSICION`

## ⏱️ TIEMPO OBTENCIÓN FIX GPS

---

```
PRIMER ENCENDIDO (Cold Start):
  ⏱️ 2-5 MINUTOS en exterior
  ⏱️ Sin obstáculos (cielo abierto)
  ⏱️ Antena hacia arriba

ENCENDIMIENTO POSTERIOR (Warm Start):
  ⏱️ 30-60 segundos
  
ENCENDIMIENTO CON ÚLTIMA POSICIÓN (Hot Start):
  ⏱️ 5-15 segundos
```

---

## 📍 VERIFICACIÓN EXTERIOR

**⚠️ GPS funciona mejor en EXTERIOR**

```
✅ Funciona mejor en EXTERIOR:
   - Cielo completamente despejado
   - Sin árboles/edificios cerca
   - Antena apuntando al cielo
   - Esperar 2-5 MINUTOS la primera vez

⚠️ En interior: Difícil obtener señal (0 satélites)
```

---

## 📊 INTERPRETACIÓN DATOS

### Satélites

```
0 satélites       ❌ Sin fix (sigue buscando)
3 satélites       ⚠️ Fix débil
4-5 satélites     ✓ Fix normal
6-10 satélites    ✓✓ Fix excelente
```

### Altitud GPS

```
Altitud es MSLM (sobre nivel del mar):

Madrid centro:    ~640m
Guadarrama:       ~1200m
Nivel del mar:    ~0m
```

### Precisión

```
Altitud GPS: ±5-20 metros típicamente
Lat/Lon:     ±5-30 metros típicamente

Mejor precisión cuantos más satélites
```

---

## ⚠️ CHECKLIST ANTES DE VUELO

```
☐ GPS conectado a D2 (RX) y D4 (TX)
☐ 3.3V conectado
☐ GND conectado
☐ Programa carga sin errores
☐ GPS obtiene fix en 2-5 minutos (en exterior)
☐ Mínimo 4 satélites para datos confiables
☐ Altitud dentro de rango esperado
```

---

## 🚨 TROUBLESHOOTING

### Problema: "Sin fix GPS" después de 10 min

```
Causas:
  ❌ En INTERIOR (GPS no funciona adentro)
  ❌ Antena apuntando al suelo
  ❌ Bajo árboles/edificios
  ❌ Antena defectuosa

Solución:
  1. Ir a exterior completamente despejado
  2. Antena HACIA EL CIELO
  3. Esperar 5 minutos
  4. Mover GPS en diferentes ángulos
```

### Problema: 0 satélites siempre

```
Posibles causas:
  1. GPIO/UART no inicializado (raro)
  2. GPS defectuoso
  3. Antena no conectada

Solución:
  1. Reinicia Arduino
  2. Verifica SoftwareSerial en D2/D4
  3. Prueba con datos GPS RAW (ver verificación)
```

### Problema: Altitud incorrecta

```
GPS altitud puede variar ±20m:
  - Es normal
  - Cuantos más satélites, más precisión
  - No confíes en altitud con <4 satélites
```

---

## 📝 NOTAS IMPORTANTES

```
✅ GPS NECESITA TIEMPO
   Primera búsqueda: 2-5 minutos
   Planifica esto en competencia

✅ GPS es LENTO
   Actualiza posición cada 1 segundo
   No es ideal para datos en tiempo real

✅ GPS es PESADO
   Usa bastante corriente (>100mA)
   Verifica que batería aguante

✅ GPS + Altitud barométrica
   Combinar GPS alt + LPS22HB da mejor precisión
   GPS: posición
   LPS22HB: altitud continua
```

---

## 🚀 SIGUIENTE PASO

Una vez que GPS funcione correctamente, pasar al **Documento 4: Integración APC220**

---

**Fecha:** Enero 2026  
**Proyecto:** CanSat Misión 2  
**Estado:** ✅ Completado
