# GUÍA RÁPIDA - CONFIGURACIÓN Y USO APC220

## Objetivo
Configurar y usar **DOS módulos APC220** para telemetría del CanSat (emisor + receptor).

---

## CRÍTICO: AMBOS DEBEN TENER LA MISMA CONFIGURACIÓN

Si no coinciden → NO se comunican  
Si coinciden → Listos para CanSat

---

## CONFIGURACIÓN OBJETIVO (AMBOS)

```
Frecuencia:     434 MHz (434000 KHz)
Velocidad RF:   9600 bps
Potencia:       9 (máxima)
Puerto serie:   9600 bps
Paridad:        0 (sin paridad)

Comando: WR 434000 3 9 3 0 # (Frecuencia ejemplo - Cambiar por la del concurso)
```

---

## PARTE 1: CONFIGURAR LOS APC220

### Método: Arduino UNO como configurador

Otros métodos (rfmagic, PuTTY, terminales serie) no funcionaron porque no podían establecer comunicación con el módulo. Ver https://beetlecraft.blogspot.com/2015/10/tutorial-apc220.html para resolver con rfmagic

### Hardware necesario
- Arduino UNO
- Módulo APC220
- Antena conectada al APC220

### Conexión Arduino UNO ↔ APC220

```
Arduino UNO     APC220
───────────────────────
GND        →    GND
D13        →    VCC
D12        →    EN
D11        →    RXD
D10        →    TXD
D8         →    SET
```

### Pasos

1. Conecta el APC220 al Arduino UNO según el esquema
2. Conecta la antena al APC220
3. Carga el programa: `PROGRAMA_APC220_CONFIGURADOR.ino`
4. Abre Monitor Serie a 9600 baud
5. Verás la configuración actual
6. Para escribir nueva configuración: `WR 434000 3 9 3 0`
7. Para verificar: `RD`
8. Debe responder: `PARA 434000 3 9 3 0`
9. **REPITE con el segundo APC220**

---

## PARTE 2: CONEXIÓN PARA TELEMETRÍA

### IMPORTANTE: Conexiones DIRECTAS (no cruzadas)

La etiqueta TXD/RXD del APC220 indica **dónde conectar el pin del micro**, no la función del módulo. Por eso van directos:
- TX del micro → TXD del APC220
- RX del micro → RXD del APC220

---

### Emisor: Arduino Nano 33 BLE Sense + APC220

```
Nano 33 BLE     APC220
───────────────────────
Pin 0 (RX)  →   RXD
Pin 1 (TX)  →   TXD
3.3V        →   VCC
GND         →   GND
```

**NOTA:** El pin EN puede dejarse sin conectar, funciona igualmente.  
Compatible con conector Grove (4 pines: VCC, GND, TX, RX).

Programa: `PROGRAMA_APC220_EMISOR.ino`

---

### Receptor Opción A: Arduino UNO + APC220

```
Arduino UNO     APC220
───────────────────────
GND        →    GND
D13        →    VCC
D12        →    EN
D11        →    RXD
D10        →    TXD
D8         →    SET
```

Programa: `PROGRAMA_APC220_RECEPTOR.ino`

---

### Receptor Opción B: USB-TTL + APC220

```
USB-TTL     APC220
───────────────────
TX      →   TXD
RX      →   RXD
3.3V    →   VCC
GND     →   GND
```

Abrir monitor serie del puerto USB-TTL a 9600 baud.

---

## VERIFICACIÓN

1. Carga `PROGRAMA_APC220_EMISOR.ino` en el Nano 33 BLE
2. Carga `PROGRAMA_APC220_RECEPTOR.ino` en el Arduino UNO (o usa USB-TTL)
3. Abre monitor serie del receptor
4. Deberías ver "HOLA" cada 2 segundos

---

## PROBLEMAS COMUNES

### No hay comunicación

1. ¿Misma configuración en ambos APC220? → Verificar con `RD`
2. ¿Antenas conectadas?
3. ¿Conexiones directas (no cruzadas)?
4. ¿Pines correctos?

### Error al configurar

1. ¿Antena conectada? → Módulo inestable sin antena
2. ¿Arduino UNO? → Nano 33 BLE no sirve para configurar (no soporta SoftwareSerial)

---

## CHECKLIST

```
(Frecuencia ejemplo - Cambiar por la del concurso)
CONFIGURACIÓN:
[ ] APC220 #1 configurado: PARA 434000 3 9 3 0 
[ ] APC220 #2 configurado: PARA 434000 3 9 3 0

EMISOR (Nano 33 BLE):
[ ] Pin 0 → RXD
[ ] Pin 1 → TXD
[ ] 3.3V → VCC
[ ] GND → GND
[ ] Antena conectada

RECEPTOR:
[ ] Conexión correcta
[ ] Antena conectada
[ ] Monitor serie a 9600 baud

PRUEBA:
[ ] Receptor muestra "HOLA" cada 2 segundos
[ ] Listo para integrar sensores
```
