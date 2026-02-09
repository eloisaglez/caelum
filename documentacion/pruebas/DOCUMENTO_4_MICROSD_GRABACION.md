# CanSat Misión 2 - Documento 5
## Grabación en MicroSD - Almacenamiento Local

**Fecha:** Enero 2026  
**Proyecto:** CanSat - Detección de Firmas de Combustión  

---

## 📋 Objetivo

Grabar todos los datos de sensores en tarjeta MicroSD como respaldo (si APC220 falla).

---

## 💾 MicroSD - Especificaciones

```
Protocolo: SPI
Voltaje: 3.3V (crítico)
Capacidad: 2GB-32GB (recomendado 4-8GB)
Velocidad: Class 10+ (recomendado)
Archivo: MISSION2.CSV (formato CSV)
```

---

## 🔌 Conexión Física

**¡¡CRÍTICO!!** MicroSD es **SOLO 3.3V**. Si usas 5V → **SE DAÑA PERMANENTEMENTE**

```
Arduino Nano 33 BLE ← → Módulo MicroSD SPI

D10 (CS)   → MicroSD CS (Chip Select)
D11 (MOSI) → MicroSD MOSI (Master Out Slave In)
D12 (MISO) → MicroSD MISO (Master In Slave Out)
D13 (SCK)  → MicroSD SCK (Serial Clock)
GND        → GND
3.3V       → VCC (⚠️ NUNCA 5V)
```

**Verificar con multímetro:** VCC debe mostrar exactamente 3.3V

---

## 🛠️ Preparación MicroSD

### Paso 1: Formato

```
En Windows:
1. Inserta MicroSD en lector
2. Click derecho → Formatear
3. Sistema archivos: FAT32
4. Tamaño de unidad: 4096 bytes
5. Etiqueta: CANSAT
6. Click Iniciar → SÍ
```

### Paso 2: Crear carpeta (opcional)

```
Crear carpeta "DATOS" en MicroSD
Almacenaremos MISSION2.CSV aquí
```

---

## 📥 Instalación Librerías

```
Arduino IDE:

Sketch → Include Library → Manage Libraries

✅ Busca e instala:
   - SD (por Arduino - incluida por defecto)
```

---

## 💻 Programa: Grabar Sensores integrados en la placa en MicroSD

**Programa:** `software/pruebas/PROGRAMA_4_MICROSD_GRABACION.ino` 

---

## 📊 Estructura del Archivo CSV

```
Archivo: MISSION2.CSV

Cabecera:
nº,Temp(HS),Humedad,Presion,Altitud,AccelZ,GyroX

Datos:
0,23.5,65.2,929.5,620.1,1.00,0.2
1,23.5,65.1,929.5,620.0,1.00,0.1

```
---

## ✅ Verificación

### Paso 1: Cargar programa

```
1. Copia código arriba
2. Arduino IDE → Nuevo
3. Pega
4. RESET doble
5. Ctrl+U
```

### Paso 2: Verificar Monitor Serial

```
Deberías ver:
✓ MicroSD (SPI) OK
✓ LPS22HB OK
✓ HS3003 OK
✓ IMU OK
✓ Grabado: 0 | T:23.5°C...
✓ Grabado: 1 | T:23.5°C...
```

### Paso 3: Leer archivo

```
1. Presiona Ctrl+C después de 30 segundos
2. Saca MicroSD del Arduino
3. Inserta en lector en PC
4. Abre MISSION2.CSV en Excel/notepad
5. Deberías ver datos en formato CSV
```

## ⚠️ Checklist Antes de Vuelo

```
☐ MicroSD insertada en módulo
☐ Módulo conectado D10/D11/D12/D13
☐ 3.3V verificado con multímetro
☐ Programa carga sin errores
☐ Monitor Serial muestra "Grabado: 0..."
☐ MicroSD formateada en FAT32
☐ Archivo MISSION2.CSV se crea correctamente
☐ Datos coherentes después de 1 minuto
```

---

## 🚨 Troubleshooting

### Error: "MicroSD no inicializa"

```
Causas:
  1. Voltaje incorrecto (5V en lugar de 3.3V)
  2. Cable CS (D10) no conectado
  3. MicroSD no formateada

Soluciones:
  1. Verificar 3.3V con multímetro
  2. Verificar D10 conectado
  3. Formatear en FAT32
```

### Archivo no se crea

```
Causas:
  1. MicroSD no detectada
  2. Tarjeta no tiene espacio
  3. Permiso de escritura denegado

Soluciones:
  1. Verificar inicialización
  2. Formatear MicroSD
  3. Probar otra MicroSD
```

### Datos no se graban

```
Causas:
  1. dataFile.close() no ejecutado
  2. Búfer no flushed
  3. MicroSD llena

Soluciones:
  1. Verificar cerrar archivo
  2. Reducir frecuencia de grabación
  3. Usar MicroSD más grande
```

---

## 🎯 Próximo Paso

**Documento 6:** Presentación de datos y conexión con Firebase

---

**Estado:** ✅ MicroSD funcionando con grabación CSV  
**Última actualización:** Enero 2026
