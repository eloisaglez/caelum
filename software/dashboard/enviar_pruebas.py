#!/usr/bin/env python3
"""
CANSAT MISIÓN 2 - Enviar Datos de Pruebas
Recibe del puerto COM durante pruebas con sensores reales

Ruta Firebase: /cansat/pruebas/
Uso: ANTES DEL CONCURSO para probar sensores
"""

import serial
import requests
import time

# ============================================
# CONFIGURACIÓN
# ============================================

PUERTO_SERIAL = 'COM3'  # Cambiar según tu puerto
BAUDIOS = 9600

FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app"
RUTA_DATOS = "/cansat/pruebas"

CABECERA = ['timestamp', 'datetime', 'lat', 'lon', 'alt', 'alt_mar', 'sats', 
            'temp', 'hum', 'presion', 'co2', 'pm1_0', 'pm2_5', 'pm10', 
            'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'fase']

def limpiar_firebase():
    try:
        requests.delete(f"{FIREBASE_URL}{RUTA_DATOS}.json")
        print("🗑️ Pruebas anteriores borradas")
    except:
        pass

def parsear_linea(linea):
    datos = linea.split(',')
    if len(datos) < 10:
        return None
    
    payload = {}
    for i, campo in enumerate(CABECERA):
        if i < len(datos):
            try:
                v = datos[i].strip()
                payload[campo] = float(v) if '.' in v else int(v)
            except:
                payload[campo] = datos[i].strip()
    return payload

def main():
    print("=" * 50)
    print("🧪 PRUEBAS → /cansat/pruebas/")
    print("=" * 50)
    print(f"📡 Puerto: {PUERTO_SERIAL}")
    print("⚠️ NO guarda CSV (solo para probar)")
    print("=" * 50)
    
    limpiar_firebase()
    contador = 0
    
    try:
        ser = serial.Serial(PUERTO_SERIAL, BAUDIOS, timeout=1)
        print("\n⏳ Esperando datos...\n")
        
        while True:
            linea = ser.readline().decode('utf-8', errors='ignore').strip()
            
            if linea:
                payload = parsear_linea(linea)
                if payload:
                    contador += 1
                    try:
                        url = f"{FIREBASE_URL}{RUTA_DATOS}/{int(time.time()*1000)}.json"
                        requests.put(url, json=payload, timeout=0.5)
                        print(f"🧪 [{contador:4d}] Alt={payload.get('alt',0):6.1f}m | "
                              f"CO2={payload.get('co2',0)}ppm | PM2.5={payload.get('pm2_5',0)}µg/m³ ✅")
                    except:
                        print(f"🧪 [{contador:4d}] ⚠️ Firebase offline")
    
    except serial.SerialException as e:
        print(f"❌ Error puerto: {e}")
    except KeyboardInterrupt:
        print(f"\n\n🛑 PRUEBAS FINALIZADAS: {contador} paquetes")
        print("🌐 Panel: https://cansat-66d98.web.app (modo Pruebas)")

if __name__ == "__main__":
    main()
