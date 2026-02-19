# IMPORTANTE — CONFIGURACIÓN APC220 (434 MHz)
## CANSAT CAELUM · IES Diego Velázquez

---

## El problema

El módulo APC220 viene configurado de fábrica con parámetros por defecto que pueden no coincidir entre el módulo del CanSat y el módulo del portátil de tierra. Si los dos módulos no tienen exactamente la misma configuración, **no se comunican**.

---

## Parámetros que deben coincidir en AMBOS módulos

| Parámetro | Valor configurado | Notas |
|-----------|------------------|-------|
| Frecuencia | 434.000 MHz | Dentro de la banda ISM europea |
| Velocidad RF | 9600 bps | |
| Potencia TX | 9 (máxima) | Para mayor alcance en vuelo |
| Ancho de banda | 250 KHz | |
| Serie (UART) | 9600 baud | Debe coincidir con el código Arduino |

---

## Cómo configurar el APC220

### Material necesario
- Cable USB-TTL (CH340 o similar)
- Software **rfmagic** (descarga en web de RF-Solutions)
- Dos módulos APC220 (configurar ambos igual)

### Pasos
1. Conectar el APC220 al PC via USB-TTL
2. Abrir **rfmagic**
3. Seleccionar el puerto COM correcto
4. Introducir los parámetros de la tabla anterior
5. Hacer clic en **Write** para guardar
6. Repetir con el segundo módulo
7. Verificar comunicación entre ambos

---

## Verificación de comunicación

Con ambos módulos configurados:

1. Conectar módulo 1 al Arduino (CanSat)
2. Conectar módulo 2 al portátil de tierra
3. Ejecutar `receptor_telemetria.py`
4. Verificar que llegan datos en la consola

Si no llegan datos:
- Revisar que la frecuencia es idéntica en ambos módulos
- Revisar baudrate (9600 en módulo Y en código Arduino)
- Verificar que los pines TX/RX no están invertidos
- Comprobar alimentación 3.3V del módulo

---

## Pines de conexión al Arduino Nano 33 BLE Sense Rev2

| APC220 | Arduino |
|--------|---------|
| VCC | 3.3V |
| GND | GND |
| RXD | TX (pin D1) |
| TXD | RX (pin D0) |
| SET | No conectar (modo normal) |

> El Arduino Nano 33 BLE Sense trabaja a **3.3V** — no conectar a 5V.

---

## En el portátil de tierra

```bash
python receptor_telemetria.py
```

El script guarda automáticamente los datos recibidos en `datos_radio.csv`.

---

## Normativa de frecuencias

La banda 434 MHz (433.050 – 434.790 MHz) es banda ISM libre en Europa para uso sin licencia con potencia máxima de 10 mW ERP. El APC220 cumple esta normativa.

Verificar antes del concurso que la organización no tiene restricciones adicionales sobre el uso de radiofrecuencias en el aeródromo.

---

**Última actualización:** Febrero 2026
