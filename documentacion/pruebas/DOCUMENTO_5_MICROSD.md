# 📋 DOCUMENTO 5: MICROSD - GRABACIÓN LOCAL

## Objetivo
Probar la grabación de datos en tarjeta MicroSD como respaldo. En esta prueba solo se graban los **sensores integrados** del Arduino para verificar que el sistema de almacenamiento funciona.

**NOTA:** El programa final de vuelo graba todos los sensores (integrados + SCD40 + HM3301 + GPS).

---

## 💾 MicroSD - Especificaciones

```
Protocolo: SPI
Voltaje: 3.3V (⚠️ CRÍTICO - NUNCA 5V)
Capacidad: 2GB-32GB (recomendado 4-8GB)
Formato: FAT32
Archivo: TEST.CSV
```

---

## 🔌 Conexión Física

**⚠️ CRÍTICO:** MicroSD es **SOLO 3.3V**. Si usas 5V → **SE DAÑA PERMANENTEMENTE**

```
Arduino Nano 33 BLE    MicroSD (SPI)
───────────────────────────────────────
D10 (CS)           →   CS
D11 (MOSI)         →   MOSI
D12 (MISO)         →   MISO
D13 (SCK)          →   SCK
3.3V               →   VCC  (⚠️ NUNCA 5V)
GND                →   GND
```

**Verificar con multímetro:** VCC debe mostrar exactamente 3.3V

### Pinout del módulo MicroSD

```
┌─────────────────────────┐
│      MicroSD Module     │
│                         │
│  CS MOSI MISO SCK VCC GND
│   │   │    │   │   │   │
└───┼───┼────┼───┼───┼───┼─
    │   │    │   │   │   │
   D10 D11  D12 D13 3.3V GND
        Arduino Nano 33 BLE
```

---

## 🛠️ Preparación MicroSD

### Paso 1: Formatear en FAT32

```
En Windows:
1. Inserta MicroSD en lector de PC
2. Click derecho → Formatear
3. Sistema archivos: FAT32
4. Tamaño de unidad: 4096 bytes (default)
5. Click Iniciar → Sí
```

### Paso 2: Insertar en módulo

```
1. Inserta MicroSD en el módulo
2. Conecta módulo al Arduino
3. Verifica conexiones antes de encender
```

---

## 📥 Instalación Librerías

```
La librería SD viene incluida con Arduino IDE.

Si no la tienes:
Sketch → Include Library → Manage Libraries
Buscar: "SD"
Instalar: SD by Arduino
```

---

## 💻 PROGRAMA DE PRUEBA

**Archivo:** `software/pruebas/PROGRAMA_5_MICROSD.ino`

Este programa graba SOLO sensores integrados para probar el almacenamiento:
- Temperatura (HS3003)
- Humedad (HS3003)
- Presión (LPS22HB)
- Altitud (calculada)
- Aceleración (BMI270)

### Pasos:
1. Abre el programa en Arduino IDE
2. Verifica conexión física (D10-D13/GND/3.3V)
3. Tools → Board → Arduino Nano 33 BLE
4. Ctrl+U para cargar
5. Abre Monitor Serial (9600 baud)

---

## 📊 Formato del Archivo CSV

```
Archivo: TEST.CSV

Cabecera:
tiempo,temperatura,humedad,presion,altitud,accelX,accelY,accelZ

Datos ejemplo:
1000,23.50,65.2,929.5,0.0,0.02,-0.01,1.00
2000,23.45,65.1,929.5,0.1,0.01,-0.02,1.00
3000,23.48,65.0,929.4,0.2,0.00,-0.01,0.99
```

---

## ✅ Verificación

### Paso 1: Cargar programa

```
1. Abre PROGRAMA_5_MICROSD.ino
2. Tools → Board → Arduino Nano 33 BLE
3. Ctrl+U para cargar
4. Abre Monitor Serial (9600 baud)
```

### Paso 2: Verificar Monitor Serial

```
MALO:
  "MicroSD (SPI)... ERROR"

BUENO:
  "HS3003 (Temp/Hum)... OK"
  "LPS22HB (Presión)... OK"
  "IMU (Acelerómetro)... OK"
  "MicroSD (SPI)... OK"
  "Archivo creado: TEST.CSV"
  
  ║   0   ║ 23.5  ║ 65.2  ║ 930   ║  0.0  ║
  ║   1   ║ 23.5  ║ 65.1  ║ 930   ║  0.1  ║
```

### Paso 3: Verificar archivo en PC

```
1. Desconecta Arduino (espera que termine de grabar)
2. Saca MicroSD del módulo
3. Inserta en lector de PC
4. Abre TEST.CSV con Excel o Bloc de notas
5. Deberías ver los datos grabados
```

---

## 📈 Análisis de Datos

### En Excel

```
1. Abre TEST.CSV
2. Datos → Texto en columnas
3. Delimitador: Coma
4. Finalizar

Ahora puedes crear gráficas:
  • Temperatura vs Tiempo
  • Altitud vs Tiempo
  • etc.
```

---

## ⚠️ Problemas Conocidos con Nano 33 BLE

El Arduino Nano 33 BLE tiene **problemas de compatibilidad** con algunos módulos MicroSD debido a diferencias en la implementación del bus SPI.

**Si la MicroSD no funciona:**
1. Probar otro módulo MicroSD
2. Probar otra tarjeta MicroSD
3. Usar **grabación en RAM** como alternativa (ver DOCUMENTO_7)

---

## ⚠️ Checklist Antes de Prueba

```
☐ MicroSD formateada en FAT32
☐ MicroSD insertada en módulo
☐ Módulo conectado a D10/D11/D12/D13
☐ VCC conectado a 3.3V (verificado con multímetro)
☐ GND conectado
☐ Programa cargado sin errores
☐ Monitor Serial muestra "OK" en todos los sensores
☐ Archivo TEST.CSV se crea
☐ Datos visibles en PC después de desconectar
```

---

## 🚨 Troubleshooting

### Error: "MicroSD no inicializa"

```
1. Verificar voltaje con multímetro:
   VCC = 3.3V (NUNCA 5V)

2. Verificar conexiones SPI:
   CS   → D10
   MOSI → D11
   MISO → D12
   SCK  → D13

3. Formatear MicroSD en FAT32

4. Probar otra MicroSD (algunas no son compatibles)
```

### Error: "No se crea archivo"

```
1. MicroSD llena → Borrar archivos o formatear
2. MicroSD protegida → Verificar pestaña de protección
3. Formato incorrecto → Formatear FAT32
```

### Datos no se graban

```
1. Verificar que dataFile.close() se ejecuta
2. No desconectar mientras graba
3. Esperar a que termine de escribir
```

---

## 📝 Notas Importantes

```
✅ MicroSD SOLO 3.3V
   5V puede dañar el módulo y la tarjeta

✅ Esta prueba solo graba sensores integrados
   El programa final graba TODO (CO2, PM2.5, GPS, etc.)

✅ Alternativa: Grabación en RAM
   Si MicroSD no funciona, usar DOCUMENTO_7_GRABACION_RAM

✅ FAT32 obligatorio
   Otros formatos (NTFS, exFAT) no funcionan

✅ Capacidad máxima recomendada: 32GB
   Tarjetas más grandes pueden dar problemas
```

---

## 🎯 Próximo Paso

**Documento 6:** APC220 - Telemetría RF

---

**Estado:** ✅ Prueba MicroSD con sensores integrados  
**Última actualización:** Febrero 2026
