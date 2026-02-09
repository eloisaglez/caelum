## 📋 DOCUMENTO 7: Sistema de Grabación en RAM

Objetivo
El Arduino Nano 33 BLE utiliza la memoria RAM como una **"Caja Negra"** de seguridad. Esto evita fallos por vibraciones en tarjetas MicroSD y asegura que los datos críticos del vuelo se conserven mientras el dispositivo esté encendido.

**Capacidad:** 400 registros (~13 minutos a 1 registro cada 2 segundos).

## 🛠️ Fase 0: Test Rápido de Diagnóstico

Antes de cargar el programa de vuelo completo, usa este código mínimo para confirmar que el hardware y la memoria funcionan correctamente.

## 🕹️ Fase 1: Comandos del Monitor Serie (9600 baud)

-   `PRUEBA`: Activa el umbral de **0.5m**. Ideal para laboratorio.
-   `CONCURSO`: Activa el umbral de **2.5m**. Para el día del lanzamiento.
-   `GRABAR`: Fuerza el inicio de la grabación de forma manual.
-   `BORRAR`: Limpia la memoria RAM y resetea la altitud máxima.
-   `CSV`: Exporta todos los datos guardados en formato de tabla para Excel.

## 🚀 Fase 2: Modos de Operación

### 1\. Test de Laboratorio (Manual/Sensible)

Diseñado para verificar el funcionamiento de los sensores y la memoria en un entorno controlado:

1.  Cargar el programa y enviar el comando `PRUEBA`.
2.  Levantar el CanSat y bajarlo rápido (mínimo 50 cm).
3.  El LED empezará a parpadear, indicando que está grabando.
4.  Enviar `CSV` para verificar la captura de datos.

### 2\. Vuelo Real (Automático)

Lógica optimizada para la misión oficial:

1.  Antes del lanzamiento, enviar el comando `CONCURSO`.
2.  El sistema esperará a detectar una caída real (descenso de >2.5m desde el punto más alto).
3.  **IMPORTANTE:** Tras el aterrizaje, ⚠️**no apagar o desconectar el CanSat de la batería**. Conéctalo al PC y usa el comando `CSV` antes de desconectar la batería.

## Formato de Datos Exportados

| Campo | Descripción | Unidad |
| --- | --- | --- |
| **ms** | Tiempo desde el encendido | milisegundos |
| **temp** | Temperatura ambiente | °C |
| **hum** | Humedad relativa | % |
| **alt** | Altitud relativa al suelo | metros |
| **accX/Y/Z** | Aceleración en los 3 ejes | g |

## Notas Técnicas

-   **Volatilidad:** Los datos se pierden si se desconecta la batería antes de hacer el volcado CSV.
-   **Optimización:** Se utiliza el tipo de dato `int16_t` para maximizar el espacio disponible en la RAM.

**Autor:** IES Diego Velázquez  
**Proyecto:** CanSat - Misión 2 (Backup RAM)  
**Fecha:** Febrero 2026


