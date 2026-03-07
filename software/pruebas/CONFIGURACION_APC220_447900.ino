/*
 * ========================================================================
 * PROGRAMA CONFIGURACIÓN APC220
 * ========================================================================
 * 
 * Autor: IES Diego Velázquez - CanSat 2026
 * Fuente base: https://github.com/inopya/APC220_Transceiver
 * 
 * FUNCIÓN: Configurar módulo APC220 directamente desde Arduino UNO
 * 
 * CONEXIÓN ARDUINO → APC220:
 *   GND  →  GND
 *   D13  →  VCC
 *   D12  →  EN
 *   D11  →  RXD
 *   D10  →  TXD
 *   D9   →  AUX
 *   D8   →  SET
 * 
 * CONFIGURACIÓN APLICADA:
 *   Frecuencia : 447.9 MHz
 *   Velocidad RF: 9600 bps
 *   Potencia   : 9 (máxima)
 *   Puerto serie: 9600 bps
 *   Paridad    : Sin paridad
 * 
 * PARÁMETROS FORMATO "WR AAAAAA B C D E":
 *   AAAAAA = Frecuencia en KHz (418000–455000)
 *   B = Velocidad RF: 1(2400) 2(4800) 3(9600) 4(19200)
 *   C = Potencia emisión: 0–9 (9=máxima)
 *   D = Velocidad serie: 0(1200) 1(2400) 2(4800) 3(9600) 4(19200) 5(38400) 6(57600)
 *   E = Paridad: 0(sin) 1(par) 2(impar)
 * 
 * ⚠️  IMPORTANTE: Usar Arduino UNO, NO el Nano 33 BLE
 * ⚠️  AMBOS módulos APC220 deben tener la MISMA configuración
 * ========================================================================
 */

#include <SoftwareSerial.h>

// ── Pines ────────────────────────────────────────────────────────────────
#define SET      8
#define AUX      9
#define TXD     11
#define RXD     10
#define EN      12
#define VCC     13

// ── Configuración a grabar ───────────────────────────────────────────────
#define FRECUENCIA "447900"   // 447.9 MHz
#define CONFIG_STRING "WR 447900 3 9 3 0"

// ── Puerto serie software ────────────────────────────────────────────────
SoftwareSerial APCport(RXD, TXD);

// ────────────────────────────────────────────────────────────────────────
void setup()
{
  Serial.begin(9600);
  delay(1000);

  Serial.println();
  Serial.println("╔════════════════════════════════════════╗");
  Serial.println("║   Configuración APC220 - CanSat 2026  ║");
  Serial.println("║   Frecuencia : 447.9 MHz              ║");
  Serial.println("║   Vel. RF    : 9600 bps               ║");
  Serial.println("║   Potencia   : 9 (MAX)                ║");
  Serial.println("║   Puerto serie: 9600 bps              ║");
  Serial.println("╚════════════════════════════════════════╝");
  Serial.println();

  // Inicializar pines
  pinMode(SET, OUTPUT);
  pinMode(AUX, INPUT);
  pinMode(EN,  OUTPUT);
  pinMode(VCC, OUTPUT);

  // Encender APC220
  digitalWrite(VCC, HIGH);
  digitalWrite(EN,  HIGH);
  digitalWrite(SET, HIGH);
  delay(1000);

  // Inicializar puerto serie software
  APCport.begin(9600);
  delay(500);

  // PASO 1: Escribir configuración
  Serial.println("═══════════════════════════════════════════");
  Serial.println("PASO 1: ESCRIBIENDO CONFIGURACIÓN...");
  Serial.println("═══════════════════════════════════════════");
  write_config();
  delay(1000);

  // PASO 2: Leer y verificar
  Serial.println();
  Serial.println("═══════════════════════════════════════════");
  Serial.println("PASO 2: VERIFICANDO CONFIGURACIÓN...");
  Serial.println("═══════════════════════════════════════════");
  read_config();

  Serial.println();
  Serial.println("═══════════════════════════════════════════");
  Serial.println("✅ PROCESO COMPLETADO");
  Serial.println("   Verifica que aparezca: PARAM 447900 3 9 3 0");
  Serial.println("   Si es correcto → repite con el segundo APC220");
  Serial.println("═══════════════════════════════════════════");
}

void loop()
{
  // Nada — configuración es un proceso de una sola vez
}

// ── Escribir configuración ───────────────────────────────────────────────
void write_config()
{
  Serial.print("Enviando: ");
  Serial.println(CONFIG_STRING);

  digitalWrite(SET, LOW);       // Modo configuración
  delay(50);

  APCport.print(CONFIG_STRING);
  APCport.write(0x0D);          // CR
  APCport.write(0x0A);          // LF
  delay(200);

  // Leer respuesta del APC220
  String respuesta = "";
  unsigned long t = millis();
  while (millis() - t < 1000) {
    if (APCport.available()) {
      respuesta += (char)APCport.read();
    }
  }

  if (respuesta.length() > 0) {
    Serial.print("Respuesta APC220: ");
    Serial.println(respuesta);
  } else {
    Serial.println("⚠️  Sin respuesta (normal en algunos módulos)");
  }

  digitalWrite(SET, HIGH);      // Volver a modo normal
  delay(100);
}

// ── Leer configuración actual ────────────────────────────────────────────
void read_config()
{
  Serial.println("Leyendo configuración actual...");

  digitalWrite(SET, LOW);       // Modo configuración
  delay(50);

  APCport.print("RD");
  APCport.write(0x0D);
  APCport.write(0x0A);
  delay(300);

  String respuesta = "";
  unsigned long t = millis();
  while (millis() - t < 1000) {
    if (APCport.available()) {
      respuesta += (char)APCport.read();
    }
  }

  if (respuesta.length() > 0) {
    Serial.print("Configuración leída: ");
    Serial.println(respuesta);

    // Verificar frecuencia
    if (respuesta.indexOf(FRECUENCIA) >= 0) {
      Serial.println("✅ Frecuencia 447900 confirmada correctamente");
    } else {
      Serial.println("❌ Frecuencia NO coincide — repite el proceso");
    }
  } else {
    Serial.println("⚠️  Sin respuesta al leer");
    Serial.println("   Prueba a intercambiar los cables RXD/TXD (pines 10 y 11)");
  }

  digitalWrite(SET, HIGH);      // Volver a modo normal
}
