# IMPORTANTE: CAMBIO DE FRECUENCIA ANTES DEL CONCURSO

## ⚠️ RECORDATORIO

Antes del lanzamiento oficial, la organización del concurso CanSat asignará una **frecuencia específica** a cada equipo para evitar interferencias entre los distintos CanSat.

---

## QUÉ HAY QUE HACER

Cuando recibas la frecuencia asignada (por ejemplo: 434.500 MHz):

### 1. Configurar AMBOS APC220 con la nueva frecuencia

Usa el Arduino UNO con el programa `PROGRAMA_APC220_CONFIGURADOR.ino`:

```
WR 434500 3 9 3 0
```

Verifica con:
```
RD
```

Debe responder:
```
PARA 434500 3 9 3 0
```

### 2. Configurar los DOS módulos

- APC220 del CanSat (emisor)
- APC220 de la estación tierra (receptor)

**AMBOS deben tener la MISMA frecuencia**

### 3. Probar comunicación

Después de cambiar la frecuencia, haz una prueba de comunicación para verificar que todo funciona.

---

## FRECUENCIAS PERMITIDAS

El APC220 funciona en el rango **418 - 455 MHz**.

Frecuencias comunes para CanSat:
- 433.000 MHz (433000)
- 434.000 MHz (434000)
- 434.500 MHz (434500)
- 435.000 MHz (435000)

La organización asignará una frecuencia dentro de este rango.

---

## FORMATO DEL COMANDO

```
WR FFFFFF 3 9 3 0
```

Donde FFFFFF es la frecuencia en KHz:
- 433.000 MHz = 433000
- 434.500 MHz = 434500
- 435.250 MHz = 435250

---

## CHECKLIST ANTES DEL CONCURSO

```
[ ] Frecuencia asignada recibida: _______ MHz
[ ] APC220 emisor configurado: PARA _______ 3 9 3 0
[ ] APC220 receptor configurado: PARA _______ 3 9 3 0
[ ] Prueba de comunicación OK
[ ] Antenas conectadas en ambos módulos
```

---

## NOTAS

- NO cambiar la frecuencia el día del lanzamiento sin probar antes
- Llevar el Arduino UNO y cables por si hay que reconfigurar en el campo
- Anotar la frecuencia asignada en varios sitios (papel, móvil, etc.)
