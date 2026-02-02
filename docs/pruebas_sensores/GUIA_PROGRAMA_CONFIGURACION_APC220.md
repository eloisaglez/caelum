# GUÍA: Programa de Configuración APC220

## Archivo
**`PROGRAMA_APC220_SIMPLE.ino`**

---

## Objetivo

Configurar módulo APC220 usando Arduino UNO como intermediario.

**Nota:** Otros métodos como rfmagic, PuTTY o terminales serie no funcionaron 
porque no podían establecer comunicación con el módulo. Este método con 
Arduino sí funciona correctamente.

**Importante:** Usar Arduino UNO. El Arduino Nano 33 BLE no soporta 
la librería SoftwareSerial (usa procesador ARM en lugar de AVR).

---

## Conexión Física

```
Arduino UNO     APC220
─────────────────────────
GND        →    GND
D13        →    VCC
D12        →    EN
D11        →    RXD
D10        →    TXD
D9         →    AUX
D8         →    SET
```

**Importante:** Conectar siempre la antena antes de encender el módulo.
Sin antena el módulo puede comportarse de forma inestable.

---

## Cómo Usar

### Paso 1: Conectar Hardware

1. Conecta APC220 a Arduino según esquema
2. Conecta antena al APC220
3. Conecta Arduino a PC por USB

### Paso 2: Cargar Programa

1. Abre Arduino IDE
2. Abre: PROGRAMA_APC220_SIMPLE.ino
3. Tools → Board: Arduino UNO
4. Tools → Port: COM[X]
5. Ctrl+U (cargar)

### Paso 3: Abrir Monitor Serial

1. Tools → Serial Monitor
2. Velocidad: 9600 baud
3. Verás:

```
========================================
  APC220 - CONFIGURADOR
========================================

Comandos:
  RD                   -> Leer config
  WR 434000 3 9 3 0    -> Escribir config

========================================

Configuracion actual:
PARA 434000 3 9 3 0
```

### Paso 4: Usar Comandos

**Leer configuración actual:**
```
RD
```
Respuesta: `PARA 434000 3 9 3 0`

**Escribir nueva configuración:**
```
WR 434000 3 9 3 0
```
Respuesta: `OK`

---

## Formato del Comando WR

```
WR FFFFFF V P S C
```

| Parámetro | Valores | Descripción |
|-----------|---------|-------------|
| FFFFFF | 418000-455000 | Frecuencia en KHz |
| V | 1-4 | Velocidad RF: 1=2400, 2=4800, 3=9600, 4=19200 bps |
| P | 0-9 | Potencia: 0=mínima, 9=máxima |
| S | 0-6 | Puerto serie: 0=1200, 1=2400, 2=4800, 3=9600, 4=19200, 5=38400, 6=57600 bps |
| C | 0-2 | Paridad: 0=ninguna, 1=par, 2=impar |

**Configuración recomendada para CanSat:**
```
WR 434000 3 9 3 0
```
- Frecuencia: 434 MHz
- Velocidad RF: 9600 bps
- Potencia: máxima
- Puerto serie: 9600 bps
- Sin paridad

---

## Verificación de Éxito

Después de escribir la configuración:

1. Escribe `RD` en el monitor serie
2. Debe responder: `PARA 434000 3 9 3 0`

Si ves esto → CONFIGURACIÓN EXITOSA

---

## Problemas

### "Sin respuesta" al inicio

Verifica:
1. ¿Antena conectada? → Módulo inestable sin antena
2. ¿Pines correctos? → Revisar conexiones D8-D13
3. ¿Arduino UNO? → Nano 33 BLE no funciona con SoftwareSerial
4. ¿Monitor a 9600 baud?

### Respuesta con caracteres extraños

Posibles causas:
1. Velocidad incorrecta → Verificar 9600 baud
2. Conexiones flojas → Revisar cables
3. Reiniciar Arduino y volver a probar

---

## Configuración de Dos Módulos

Para que dos APC220 se comuniquen, AMBOS deben tener la misma configuración:

### Primer APC220
1. Conecta a Arduino
2. Carga programa
3. Escribe: `WR 434000 3 9 3 0`
4. Verifica: `RD` → `PARA 434000 3 9 3 0`
5. Desconecta

### Segundo APC220
1. Conecta a Arduino
2. Escribe: `WR 434000 3 9 3 0`
3. Verifica: `RD` → `PARA 434000 3 9 3 0`
4. Desconecta

### Verificación
Ambos deben mostrar exactamente: `PARA 434000 3 9 3 0`

---

## Próximos Pasos

1. Configurar ambos APC220 con mismos parámetros
2. Verificar que ambos respondan igual a `RD`
3. Cargar programa de telemetría en el CanSat
4. Probar comunicación entre emisor y receptor
5. ¡Listo para el lanzamiento!

---

## Notas

- Puedes ejecutar el programa varias veces, no daña el APC220
- La configuración se guarda en memoria del módulo (no se pierde al apagar)
- Guarda foto de pantalla con la configuración final para referencia
