/*
 * ========================================================================
 * PROGRAMA 2: SGP30 - SENSOR DE GASES
 * ========================================================================
 * 
 * Autor: CanSat Misión 2
 * Fecha: Enero 2026
 * Proyecto: CanSat Misión 2
 * 
 * SENSOR: Adafruit SGP30
 * FUNCIÓN: Medir TVOC (ppb) + eCO2 (ppm) + H2 raw + Ethanol raw
 * 
 * CONEXIÓN:
 *   A4 (SDA) → SGP30 SDA
 *   A5 (SCL) → SGP30 SCL
 *   3.3V → SGP30 VCC (⚠️ NUNCA 5V)
 *   GND → GND
 * 
 * OBJETIVO: Prueba y calibración de sensor de gases
 * 
 * ========================================================================
 */

#include "Adafruit_SGP30.h"
#include <Wire.h>

Adafruit_SGP30 sgp30;

int contador = 0;
boolean sgp30Ok = false;

void setup() {
  Serial.begin(9600);
  delay(2000);
  
  Serial.println();
  Serial.println("╔════════════════════════════════════════╗");
  Serial.println("║  Programa 2: SGP30 (Gases)            ║");
  Serial.println("║  TVOC + eCO2 + H2 + Ethanol           ║");
  Serial.println("╚════════════════════════════════════════╝");
  Serial.println();
  
  // Inicializar SGP30
  Serial.print("Iniciando SGP30... ");
  if (!sgp30.begin()) {
    Serial.println("❌ ERROR");
    Serial.println();
    Serial.println("CAUSAS POSIBLES:");
    Serial.println("  1. Cable mal conectado");
    Serial.println("  2. Voltaje incorrecto (¿5V en lugar de 3.3V?)");
    Serial.println("  3. SGP30 defectuoso");
    Serial.println("  4. Dirección I2C incorrecta");
    Serial.println();
    Serial.println("VERIFICAR:");
    Serial.println("  • A4 (SDA) conectado");
    Serial.println("  • A5 (SCL) conectado");
    Serial.println("  • 3.3V (NO 5V) conectado");
    Serial.println("  • GND conectado");
    while(1) delay(1000);
  }
  
  Serial.println("✓ OK");
  sgp30Ok = true;
  
  Serial.println();
  Serial.println("⏳ Esperando estabilización (15 segundos)...");
  delay(15000);
  
  Serial.println("✓ Sensor listo");
  Serial.println();
  Serial.println("═══════════════════════════════════════════════════");
  Serial.println("Midiendo gases...");
  Serial.println("═══════════════════════════════════════════════════");
  Serial.println();
}

void loop() {
  if (!sgp30Ok) {
    delay(1000);
    return;
  }
  
  // Medir gases
  if (!sgp30.IAQmeasure()) {
    Serial.println("❌ Error en medición");
    return;
  }
  
  // Mostrar datos
  if (contador % 5 == 0) {
    Serial.println();
    Serial.println("N° | TVOC (ppb) | eCO2 (ppm) | H2_raw | Ethanol_raw | Interpretación");
    Serial.println("───┼────────────┼────────────┼────────┼─────────────┼────────────────");
  }
  
  Serial.print(contador);
  Serial.print(" | ");
  
  // TVOC
  if(sgp30.TVOC < 100) Serial.print(" ");
  Serial.print(sgp30.TVOC);
  Serial.print("      | ");
  
  // eCO2
  if(sgp30.eCO2 < 1000) Serial.print(" ");
  Serial.print(sgp30.eCO2);
  Serial.print("      | ");
  
  // H2 raw
  Serial.print(sgp30.rawH2);
  Serial.print("   | ");
  
  // Ethanol raw
  Serial.print(sgp30.rawEthanol);
  Serial.print("       | ");
  
  // Interpretación
  if (sgp30.TVOC < 220) {
    Serial.print("🟢 Limpio");
  } else if (sgp30.TVOC < 660) {
    Serial.print("🟡 Normal");
  } else if (sgp30.TVOC < 2200) {
    Serial.print("🟠 Moderado");
  } else if (sgp30.TVOC < 5500) {
    Serial.print("🔴 Alto");
  } else {
    Serial.print("⛔ Muy alto");
  }
  
  Serial.println();
  
  contador++;
  delay(2000);
}

/*
 * ========================================================================
 * TABLA DE REFERENCIA - CALIDAD DEL AIRE (TVOC)
 * 
 * 0-220 ppb       🟢 EXCELENTE - Aire limpio (exterior normal)
 * 220-660 ppb     🟡 BUENA - Zona residencial aceptable
 * 660-2200 ppb    🟠 MODERADA - Tráfico/Industrial suave
 * 2200-5500 ppb   🔴 MALA - Fuente cercana (generador, biomasa)
 * >5500 ppb       ⛔ MUY MALA - Fuente directa, peligroso
 * 
 * ========================================================================
 * FIRMAS DE COMBUSTIÓN DETECTABLES:
 * 
 * TRÁFICO VEHICULAR:
 *   • TVOC: 300-800 ppb
 *   • H2 raw: Elevado (>12000)
 *   • Ubicación: Carretera/Autovía
 * 
 * GENERADORES DIÉSEL:
 *   • TVOC: >1000 ppb
 *   • H2 raw: MUY elevado (>14000)
 *   • Patrón: Picos pronunciados
 * 
 * BIOMASA/FUEGO:
 *   • TVOC: >500 ppb
 *   • Ethanol raw: Alto (>18000)
 *   • Ubicación: Zona forestal
 * 
 * ========================================================================
 * NOTAS IMPORTANTES:
 * 
 * ⚠️ SGP30 NECESITA TIEMPO:
 *    - Calibración: 15 segundos
 *    - Primeras lecturas: No confíes
 *    - Valores estables después de 1 minuto
 * 
 * ⚠️ SGP30 VOLTAJE:
 *    - DEBE estar a 3.3V
 *    - Si lo conectas a 5V → SE DAÑA PERMANENTEMENTE
 *    - Verifica con multímetro
 * 
 * ✅ DATOS RAW (H2 + Ethanol):
 *    - Sin procesar
 *    - Sirven para identificar TIPO de contaminación
 *    - No son ppb ni ppm
 * 
 * ========================================================================
 */
