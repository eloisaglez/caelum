# GUÍA RÁPIDA - CONFIGURACIÓN APC220

## Objetivo
Configurar **DOS módulos APC220** para que funcionen juntos (emisor + receptor).

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

Comando: WR 434000 3 9 3 0
```

---

## MÉTODO: Con Arduino UNO

Otros métodos como rfmagic, PuTTY o terminales serie no funcionaron 
porque no podían establecer comunicación con el módulo. 
El método con Arduino UNO como intermediario sí funciona correctamente.

### Hardware Necesario

- Arduino UNO (no sirve Nano 33 BLE, no soporta SoftwareSerial)
- Módulo APC220
- Cable USB
- Antena conectada al APC220 (importante)

### Conexión Arduino UNO ↔ APC220

```
Arduino     APC220
───────────────────
GND    →    GND
D13    →    VCC
D12    →    EN
D11    →    RXD
D10    →    TXD
D9     →    AUX
D8     →    SET
```

### Pasos

1. Conecta Arduino UNO a PC (USB)

2. Conecta APC220 a Arduino según esquema (con antena)

3. Abre Arduino IDE:
   - Selecciona: Board = Arduino UNO
   - Selecciona: Port = COM[X]

4. Carga el programa: PROGRAMA_APC220_SIMPLE.ino

5. Abre Monitor Serial (9600 baud)

6. Deberías ver:
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

7. Para cambiar la configuración, escribe en el monitor serie:
   ```
   WR 434000 3 9 3 0
   ```

8. Verifica escribiendo:
   ```
   RD
   ```
   Debe responder: `PARA 434000 3 9 3 0`

9. Desconecta APC220

10. REPITE CON SEGUNDO APC220

---

## VERIFICACIÓN FINAL

Después de configurar AMBOS APC220:

1. Conecta PRIMER APC220
2. Abre Monitor Serial, escribe `RD`
3. Debe mostrar: `PARA 434000 3 9 3 0`

4. Desconecta, conecta SEGUNDO APC220
5. Escribe `RD`
6. Debe mostrar: `PARA 434000 3 9 3 0`

**SI ALGUNO MUESTRA DIFERENTE → Reconfigurar**

---

## PRUEBA DE COMUNICACIÓN

Una vez ambos configurados:

### Emisor (conectado al CanSat)

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.println("HOLA");
  delay(2000);
}
```

### Receptor (estación tierra)

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    Serial.print(c);
  }
}
```

Si ves "HOLA" cada 2 segundos → TODO FUNCIONA

---

## PROBLEMAS COMUNES

### "Sin respuesta" o configuración no se lee

Solución:
1. ¿Antena conectada? → El módulo puede ser inestable sin antena
2. ¿Pines D8-D13 bien conectados? → Verificar conexiones
3. ¿D13 a VCC del APC220? → Es la alimentación
4. ¿Monitor Serial a 9600 baud?

### "No comunican los dos APC220"

Solución:
1. ¿Misma configuración? → Verificar PARAM en ambos, deben ser IGUALES
2. ¿Antenas conectadas en ambos?
3. ¿Distancia? → Probar a 10 metros sin obstáculos

---

## CHECKLIST CONFIGURACIÓN

```
PRIMER APC220:
  [ ] Conectado a Arduino UNO
  [ ] Antena conectada
  [ ] Configuración escrita: WR 434000 3 9 3 0
  [ ] Verificado con RD: PARA 434000 3 9 3 0

SEGUNDO APC220:
  [ ] Conectado a Arduino UNO
  [ ] Antena conectada
  [ ] Configuración escrita: WR 434000 3 9 3 0
  [ ] Verificado con RD: PARA 434000 3 9 3 0

VERIFICACIÓN FINAL:
  [ ] Ambos muestran: PARA 434000 3 9 3 0
  [ ] Prueba de comunicación OK
  [ ] Listos para CanSat
```

---

## DESPUÉS DE CONFIGURAR

1. Ambos APC220 guardados con configuración
2. Listos para CanSat
3. Carga programa de telemetría
4. Prueba de comunicación final
5. ¡A BRUNETE!
