"""
CANSAT - Simulador de Telemetría (Versión REST API)
Genera datos simulados y los envía a Firebase usando HTTP REST

✅ No requiere serviceAccountKey.json
✅ Más simple y seguro para GitHub
✅ Ideal para proyectos educativos

Autor: IES Diego Velázquez
Fecha: Enero 2026
"""

import requests
import time
import random
import math
from datetime import datetime

# ============================================
# CONFIGURACIÓN FIREBASE
# ============================================

FIREBASE_URL = "https://cansat-66d98-default-rtdb.europe-west1.firebasedatabase.app"
RUTA_DATOS = "/cansat/telemetria"

# ============================================
# CONFIGURACIÓN SIMULACIÓN
# ============================================

# Posición inicial (Torrelodones, Madrid)
LAT_INICIAL = 40.5795
LON_INICIAL = -3.9184
ALTITUD_INICIAL = 1000  # metros

# Parámetros de vuelo
VELOCIDAD_ASCENSO = 12  # m/s (subida)
VELOCIDAD_CAIDA_LIBRE = 25  # m/s (caída libre)
VELOCIDAD_PARACAIDAS = 3  # m/s (con paracaídas)
INTERVALO_ENVIO = 1  # segundos entre envíos

# Altitudes de cambio de fase
ALT_MAX = 1500  # Separación
ALT_PARACAIDAS = 700  # Apertura paracaídas
ALT_TIERRA = 667  # Nivel del suelo en Torrelodones

# ============================================
# CLASE SIMULADOR
# ============================================

class SimuladorCanSat:
    def __init__(self):
        self.tiempo = 0
        self.altitud = ALTITUD_INICIAL
        self.lat = LAT_INICIAL
        self.lon = LON_INICIAL
        self.temperatura_base = 20
        self.presion_base = 1013.25
        self.fase = "ascenso"
        
    def actualizar_fase(self):
        """Determina la fase actual del vuelo"""
        if self.fase == "ascenso" and self.altitud >= ALT_MAX:
            self.fase = "caida_libre"
            print(f"\n{'='*60}")
            print("⚠️  SEPARACIÓN - INICIO DE CAÍDA LIBRE")
            print("=" * 60)
        elif self.fase == "caida_libre" and self.altitud <= ALT_PARACAIDAS:
            self.fase = "paracaidas"
            print(f"\n{'='*60}")
            print("🪂 APERTURA DE PARACAÍDAS")
            print("=" * 60)
        elif self.fase == "paracaidas" and self.altitud <= ALT_TIERRA:
            self.fase = "tierra"
            print(f"\n{'='*60}")
            print("🎯 ATERRIZAJE EXITOSO")
            print("=" * 60)
    
    def actualizar(self, dt):
        """Actualiza estado del CanSat"""
        self.tiempo += dt
        
        # Actualizar altitud según fase
        if self.fase == "ascenso":
            self.altitud += VELOCIDAD_ASCENSO * dt
            self.altitud += random.uniform(-1, 1)
        elif self.fase == "caida_libre":
            self.altitud -= VELOCIDAD_CAIDA_LIBRE * dt
            self.altitud += random.uniform(-2, 2)
        elif self.fase == "paracaidas":
            self.altitud -= VELOCIDAD_PARACAIDAS * dt
            self.altitud += random.uniform(-0.5, 0.5)
        else:  # tierra
            self.altitud = ALT_TIERRA + random.uniform(-0.2, 0.2)
        
        # Limitar altitud mínima
        self.altitud = max(self.altitud, ALT_TIERRA)
        
        # Deriva horizontal (viento)
        self.lat += random.uniform(-0.0001, 0.0001)
        self.lon += random.uniform(-0.0001, 0.0001)
        
        self.actualizar_fase()
    
    def leer_gps(self):
        """Simula GPS ATGM336H"""
        return {
            'latitud': round(self.lat, 6),
            'longitud': round(self.lon, 6),
            'altitudGPS': round(self.altitud, 1),
            'satelites': random.randint(7, 12)
        }
    
    def leer_bmp280(self):
        """Simula BMP280 (presión y temperatura)"""
        # Temperatura disminuye ~6.5°C por cada 1000m
        temp = self.temperatura_base - (self.altitud / 1000.0) * 6.5
        temp += random.uniform(-0.5, 0.5)
        
        # Presión atmosférica (ecuación barométrica)
        presion = self.presion_base * math.exp(-self.altitud / 8500)
        presion += random.uniform(-1, 1)
        
        # Altitud barométrica calculada
        alt_baro = 44330 * (1 - (presion / self.presion_base) ** 0.1903)
        
        return {
            'temperatura': round(temp, 2),
            'presion': round(presion, 2),
            'altitud': round(alt_baro, 1)
        }
    
    def leer_mpu6050(self):
        """Simula MPU6050 (acelerómetro y giroscopio)"""
        if self.fase == "ascenso":
            # Subida: aceleración hacia arriba
            accel = [
                random.uniform(-5, 5),
                random.uniform(-5, 5),
                random.uniform(100, 120)  # Aceleración vertical
            ]
            rot = [
                random.uniform(-5, 5),
                random.uniform(-5, 5),
                random.uniform(-10, 10)
            ]
        elif self.fase == "caida_libre":
            # Caída libre: rotación rápida, baja aceleración
            accel = [
                random.uniform(-10, 10),
                random.uniform(-10, 10),
                random.uniform(-5, 5)  # Casi 0 (caída libre)
            ]
            rot = [
                random.uniform(-80, 80),
                random.uniform(-80, 80),
                random.uniform(-100, 100)
            ]
        elif self.fase == "paracaidas":
            # Con paracaídas: estabilizado
            accel = [
                random.uniform(-3, 3),
                random.uniform(-3, 3),
                random.uniform(95, 105)  # ~1g
            ]
            rot = [
                random.uniform(-15, 15),
                random.uniform(-15, 15),
                random.uniform(-20, 20)
            ]
        else:  # tierra
            # En tierra: quieto
            accel = [
                random.uniform(-0.5, 0.5),
                random.uniform(-0.5, 0.5),
                random.uniform(98, 100)
            ]
            rot = [
                random.uniform(-1, 1),
                random.uniform(-1, 1),
                random.uniform(-1, 1)
            ]
        
        return {
            'accelX': round(accel[0], 2),
            'accelY': round(accel[1], 2),
            'accelZ': round(accel[2], 2),
            'rotX': round(rot[0], 1),
            'rotY': round(rot[1], 1),
            'rotZ': round(rot[2], 1)
        }
    
    def leer_sgp30(self):
        """Simula SGP30 (calidad del aire)"""
        # Simular diferentes niveles según altitud
        if 400 < self.altitud < 450:
            # Zona contaminada (tráfico)
            tvoc = random.uniform(800, 2000)
            eco2 = random.uniform(1000, 1500)
        elif 200 < self.altitud < 250:
            # Zona muy contaminada (industria)
            tvoc = random.uniform(1500, 3000)
            eco2 = random.uniform(1500, 2500)
        else:
            # Aire limpio
            tvoc = random.uniform(100, 400)
            eco2 = random.uniform(400, 800)
        
        return {
            'tvoc': round(tvoc, 0),
            'eco2': round(eco2, 0),
            'h2': round(random.uniform(11000, 13500), 0),
            'etanol': round(random.uniform(16000, 18500), 0)
        }
    
    def obtener_telemetria_completa(self):
        """Obtiene lectura completa de todos los sensores"""
        telemetria = {}
        telemetria.update(self.leer_gps())
        telemetria.update(self.leer_bmp280())
        telemetria.update(self.leer_mpu6050())
        telemetria.update(self.leer_sgp30())
        telemetria['timestamp'] = datetime.now().isoformat()
        telemetria['fase'] = self.fase
        
        return telemetria
    
    def get_emoji_fase(self):
        """Retorna emoji según fase"""
        emojis = {
            "ascenso": "🚀",
            "caida_libre": "📉",
            "paracaidas": "🪂",
            "tierra": "✅"
        }
        return emojis.get(self.fase, "📡")

# ============================================
# ENVÍO A FIREBASE
# ============================================

def enviar_a_firebase(datos):
    """Envía datos a Firebase usando REST API"""
    try:
        # Usar timestamp como clave única
        timestamp_key = str(int(time.time() * 1000))
        url = f"{FIREBASE_URL}{RUTA_DATOS}/{timestamp_key}.json"
        
        response = requests.put(url, json=datos, timeout=5)
        
        if response.status_code == 200:
            return True
        else:
            print(f"❌ Error HTTP {response.status_code}: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

# ============================================
# BUCLE PRINCIPAL
# ============================================

def main():
    print("=" * 60)
    print("🛰️  CANSAT - SIMULADOR DE TELEMETRÍA (REST API)")
    print("=" * 60)
    print("\n📡 Sensores simulados:")
    print("  • GPS ATGM336H")
    print("  • BMP280 (Presión/Temperatura)")
    print("  • MPU6050 (Acelerómetro/Giroscopio)")
    print("  • SGP30 (TVOC, eCO₂, H₂, Etanol)")
    print("\n" + "=" * 60)
    print(f"🔥 Firebase: {FIREBASE_URL}")
    print(f"📍 Posición inicial: {LAT_INICIAL}, {LON_INICIAL}")
    print(f"📏 Altitud inicial: {ALTITUD_INICIAL}m")
    print(f"⏱️  Intervalo: {INTERVALO_ENVIO}s")
    print("=" * 60)
    print("\n▶️  Iniciando simulación...")
    print(f"{'='*60}\n")
    
    cansat = SimuladorCanSat()
    contador = 0
    errores = 0
    
    try:
        while cansat.fase != "tierra" or contador < 10:  # Continuar 10s después de aterrizar
            # Actualizar estado
            cansat.actualizar(INTERVALO_ENVIO)
            
            # Obtener telemetría
            telemetria = cansat.obtener_telemetria_completa()
            
            # Enviar a Firebase
            if enviar_a_firebase(telemetria):
                contador += 1
                emoji = cansat.get_emoji_fase()
                
                # Mostrar progreso
                print(f"{emoji} [{contador:3d}] "
                      f"t={cansat.tiempo:4.0f}s | "
                      f"Alt={telemetria['altitud']:6.1f}m | "
                      f"T={telemetria['temperatura']:5.1f}°C | "
                      f"P={telemetria['presion']:7.1f}hPa | "
                      f"TVOC={telemetria['tvoc']:4.0f}ppb")
            else:
                errores += 1
                print(f"⚠️  [{contador:3d}] Error en envío (total: {errores})")
            
            # Esperar antes del siguiente envío
            time.sleep(INTERVALO_ENVIO)
        
        print("\n" + "=" * 60)
        print("🎉 SIMULACIÓN COMPLETADA")
        print("=" * 60)
        print(f"\n📊 Estadísticas:")
        print(f"   ✅ Paquetes enviados: {contador}")
        print(f"   ❌ Errores: {errores}")
        print(f"   ⏱️  Tiempo total: {cansat.tiempo:.1f}s")
        print(f"   📏 Altitud final: {cansat.altitud:.1f}m")
        print(f"   🌍 Posición final: ({cansat.lat:.6f}, {cansat.lon:.6f})")
        
        print(f"\n🌐 Ver datos en tiempo real:")
        print(f"   Panel web: https://cansat-66d98.web.app")
        print(f"   Firebase: {FIREBASE_URL}/cansat/telemetria")
        print("\n" + "=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Simulación interrumpida por el usuario")
        print(f"📊 Paquetes enviados: {contador}")
        print(f"❌ Errores: {errores}")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()

# ============================================
# EJECUTAR
# ============================================

if __name__ == "__main__":
    main()
