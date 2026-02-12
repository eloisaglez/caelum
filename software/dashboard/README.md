# 🚀 Proyecto CanSat: Equipo CAELUM 🛰️

Repositorio oficial de la Estación de Tierra del **IES Diego Velázquez**. Este sistema gestiona la recepción, respaldo y visualización de telemetría para la misión CanSat 2024-2025.

---

## ⚠️ CONTROL DE CALIDAD
> [!IMPORTANT]
> Antes de realizar cualquier operación oficial, asegúrate de haber eliminado la carpeta `test-local/` y cualquier archivo de prueba temporal. El directorio raíz debe contener únicamente los scripts finales detallados a continuación.

---

## 📂 Estructura de Software

### 📡 Programas de Ejecución
* **`📡_datos_puerto_serie.py`**: El motor del proyecto. Conecta con el receptor USB, guarda los datos en tiempo real con sistema de auto-guardado (`flush`) y envía la telemetría a la nube.
* **`⏪_cargar_datos_vuelo.py`**: Utilizado para el post-análisis. Carga los datos guardados en `datos_vuelo.csv` y los reproduce en el Dashboard.
* **`⏪_cargar_datos_simulacion.py`**: Programa de testeo que carga el histórico de `vuelo_brunete_17marzo.csv` para demostraciones y simulacros.

### 📊 Archivos de Datos (CSV)
* **`datos_vuelo.csv`**: Archivo maestro de la misión (se genera automáticamente al iniciar el vuelo).
* **`vuelo_brunete_17marzo.csv`**: Base de datos histórica del ensayo previo.

### 📈 Visualización
* **`Dashboard_Caelum.html`**: Interfaz web dinámica con gráficas, mapa GPS y visualización 3D.

---

## 🛠️ Protocolo de Operación

### Escenario 1: Lanzamiento Oficial (Misión Real)
1. Conectar receptor USB y verificar puerto COM.
2. Ejecutar **`📡_datos_puerto_serie.py`**.
3. Abrir **`Dashboard_Caelum.html`**.
4. Una vez confirmado el aterrizaje, detener el programa con `Ctrl + C` para cerrar el flujo de datos de forma segura.

### Escenario 2: Simulación o Presentación al Jurado
1. Ejecutar el script de carga correspondiente (**Vuelo** o **Simulación**).
2. El sistema retransmitirá los datos almacenados al Dashboard como si estuvieran ocurriendo en vivo.

---

## 👨‍💻 Sobre el Equipo
* **Institución:** IES Diego Velázquez.
* **Misión:** Análisis de contaminantes atmosféricos (PM2.5, PM10) y gases (CO2).
* **Tecnología:** Python 3.x, Firebase Realtime Database, JavaScript (Three.js para 3D).

---
*Caelum ad astra* 🌌
