# ⚙️ Configuración de Cura – Carcasa CanSat CAELUM

> Parámetros optimizados para impresión en **PLA** priorizando **resistencia mecánica** y **precisión dimensional**.  
> Probados con Ultimaker Cura (vista personalizada).

---

## 🏆 Resumen rápido

| Parámetro | Valor |
|---|---|
| Material | PLA |
| Perfil base | Super Quality – 0.12 mm |
| Altura de capa | 0.12 mm |
| Altura de capa inicial | 0.2 mm |
| Líneas de pared | 4 |
| Expansión horizontal | −0.1 mm |
| Capas superior/inferior | 8 |
| Densidad de relleno | 35% |
| Patrón de relleno | Giroide |
| Temperatura boquilla | 205 °C |
| Temperatura cama | 60 °C |
| Velocidad de impresión | 45 mm/s |
| Velocidad pared exterior | 22.5 mm/s |
| Velocidad capa inicial | 20 mm/s |
| Adherencia | Borde (Brim) – 8 mm |

---

## 📐 Calidad

| Parámetro | Valor | Motivo |
|---|---|---|
| Altura de capa | `0.12 mm` | Super Quality – mayor precisión dimensional |
| Altura de capa inicial | `0.2 mm` | Mejor adhesión a la cama |
| Ancho de línea | `0.44 mm` | Boquilla estándar 0.4 mm |

---

## 🧱 Paredes

| Parámetro | Valor | Motivo |
|---|---|---|
| Recuento de líneas de pared | `4` | Resistencia ante impacto de aterrizaje |
| Expansión horizontal | `-0.1 mm` | Compensar expansión del plástico para dimensiones exactas |
| Optimizar orden de impresión de paredes | ✅ Activado | Mejor acabado exterior |

---

## 🔝 Superior e inferior

| Parámetro | Valor | Motivo |
|---|---|---|
| Capas superiores | `8` | Cierre robusto de la carcasa |
| Capas inferiores | `8` | Base sólida ante impacto |

---

## 🔲 Relleno

| Parámetro | Valor | Motivo |
|---|---|---|
| Densidad de relleno | `35%` | Equilibrio resistencia/peso |
| Patrón de relleno | `Giroide` | Distribución isótropa de fuerzas, ideal para impactos |

---

## 🌡️ Material

| Parámetro | Valor | Motivo |
|---|---|---|
| Temperatura de impresión | `205 °C` | Mejor adhesión entre capas en PLA |
| Temperatura de la placa | `60 °C` | Adhesión óptima sin warping |

---

## 💨 Velocidad

| Parámetro | Valor | Motivo |
|---|---|---|
| Velocidad de impresión | `45 mm/s` | Precisión dimensional en paredes |
| Velocidad de pared exterior | `22.5 mm/s` | Mitad de velocidad = mejor acabado |
| Velocidad de capa inicial | `20 mm/s` | Máxima adhesión primera capa |
| Velocidad de desplazamiento | `150 mm/s` | Valor por defecto, no modificar |

---

## 🔄 Desplazamiento

| Parámetro | Valor |
|---|---|
| Habilitar la retracción | ✅ Activado |
| Distancia de retracción | `2.0 mm` |
| Velocidad de retracción | `25 mm/s` |
| Modo peinada | Sobre el relleno |
| Evitar partes impresas al desplazarse | ✅ Activado |

---

## 🧊 Refrigeración

| Parámetro | Valor |
|---|---|
| Activar refrigeración | ✅ Activado |
| Velocidad del ventilador | `100%` |
| Velocidad inicial del ventilador | `0%` (activa desde capa 4) |
| Tiempo mínimo de capa | `10 s` |

---

## 🏗️ Adherencia de la placa de impresión

| Parámetro | Valor | Motivo |
|---|---|---|
| Tipo de adherencia | `Borde` (Brim) | Sujeta la pieza sin añadir grosor bajo la carcasa |
| Ancho del borde | `8 mm` | Suficiente para piezas con paredes finas |
| Borde solo en exterior | ✅ Activado | Facilita retirada del borde |

---

## ⚠️ Notas importantes

- **No activar soportes** si el diseño está orientado correctamente.
- Hacer una **pieza de prueba pequeña** antes de imprimir la carcasa completa para validar tolerancias (especialmente agujeros para tornillos y sensores).
- Si los encajes quedan demasiado ajustados, aumentar la expansión horizontal a `−0.15 mm`.
- Si los encajes quedan holgados, reducir a `−0.05 mm`.

---

## 🛠️ Hardware de referencia

Configuración probada para la carcasa del **CanSat CAELUM** que aloja:

- Arduino Nano 33 BLE Sense Rev2
- Sensor HM-3301 (partículas)
- Sensor SCD40/41 (CO₂)
- Módulo GPS
- Módulo radio APC220
- Módulo SD card

---

*Generado para el proyecto CAELUM – IES Diego Velázquez, Torrelodones*
