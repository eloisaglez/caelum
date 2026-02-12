# 🚀 Proyecto CanSat: Equipo CAELUM 🛰️

Bienvenido al repositorio oficial de la Estación de Tierra del **Equipo CAELUM** (IES Diego Velázquez). Este sistema permite la recepción, procesado, almacenamiento y visualización en tiempo real de la telemetría de nuestro CanSat.

---

## 📂 Estructura del Proyecto

El sistema está organizado en una estructura plana para facilitar su ejecución durante la misión:

* 📈 **`Dashboard_Caelum.html`**: Panel de control visual con gráficos en tiempo real, mapa GPS y modelo 3D.
* 📡 **`caelum_ground_station.py`**: Script de Python (Thonny) que gestiona la entrada de datos por puerto serie y su subida a Firebase.
* ⏪ **`caelum_playback.py`**: Simulador para reproducir vuelos pasados a partir de archivos CSV.
* 💾 **`mision_caelum_full_backup.csv`**: Archivo local de seguridad donde se registran todos los datos recibidos.

---

## 🛠️ Protocolo de Lanzamiento

Siga estos pasos rigurosamente para asegurar la integridad de los datos durante el vuelo:

### 1. Preparación de Hardware
* Conectar el receptor de radio (USB) al ordenador.
* Identificar el puerto asignado (ej. `COM3` en Windows o `/dev/ttyUSB0` en Linux).

### 2. Inicio de la Estación de Tierra (Backend)
1. Abrir `📡_caelum_ground_station.py` en **Thonny**.
2. Verificar que la variable `PUERTO_SERIAL` coincide con el puerto detectado.
3. Ejecutar el script (`F5`).
4. Confirmar que la consola muestra: `✅ Recepción activa`.

### 3. Visualización (Frontend)
1. Abrir `📈_Dashboard_Caelum.html` en un navegador (preferiblemente Chrome o Edge).
2. Presionar `F11` para entrar en modo pantalla completa.

---

## 📊 Protocolo de Datos (Telemetría)

El sistema procesa **15 parámetros** críticos:
1. Altitud | 2. Temperatura | 3. Presión | 4. CO2 | 5. Latitud | 6. Longitud | 7. PM2.5 | 8. PM10 | 9-11. Aceleración (X,Y,Z) | 12-14. Rotación (X,Y,Z) | 15. Humedad.

> [!IMPORTANT]
> **Seguridad de Datos:** Aunque falle la conexión a Internet, el sistema seguirá guardando la telemetría íntegra en el archivo CSV local. **No cerrar Thonny hasta que el CanSat haya aterrizado.**

---

## 👨‍💻 Equipo
* **Nombre del Equipo:** CAELUM
* **Institución:** IES Diego Velázquez
* **Misión:** CanSat 2024-2025