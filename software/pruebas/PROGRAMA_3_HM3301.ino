/* * =========================================================================
 * MISION CANSAT- PRUEBAS DE LABORATORIO (ASMA / EPOC)
 * -------------------------------------------------------------------------
 * RESUMEN DE IMPACTO:
 * PM1.0 (ug/m3): Partículas muy finas. Pueden pasar a la sangre.
 * PM2.5 (ug/m3): RIESGO ASMA/EPOC. Inflaman los bronquios.
 * PM10  (ug/m3): RIESGO ALERGIA. Polen y polvo que irritan vías altas.
 * -------------------------------------------------------------------------
 * LÍMITES DE SEGURIDAD (Referencia PM2.5):
 * 🟢 [0-12] Seguro | 🟡 [13-35] Moderado | 🟠 [36-55] Riesgo Asmático | 🔴 [>55] Crisis
 * -------------------------------------------------------------------------
 CONEXIÓN I2C:
 * - VCC: 3.3V o 5V
 * - GND: GND
 * - SDA: Pin A4 (Nano 33 BLE)
 * - SCL: Pin A5 (Nano 33 BLE)
 * =========================================================================
 */

#include <Wire.h>

#define HM3301_ADDR 0x40 

uint16_t pm1_0, pm2_5, pm10;
unsigned long ultimaLectura = 0;

void setup() {
    Serial.begin(9600); 
    Wire.begin();       

    unsigned long inicio = millis();
    while (!Serial && millis() - inicio < 5000);

    // Activación del sensor
    Wire.beginTransmission(HM3301_ADDR);
    Wire.write(0x88); 
    Wire.endTransmission();
    
    Serial.println("\n--- PRUEBA DE LABORATORIO: ANALISIS RESPIRATORIO ---");
    Serial.println("Tiempo | PM1.0 | PM2.5 | PM10  | ESTADO DE RIESGO");
    Serial.println("---------------------------------------------------------");
}

void loop() {
    // Lectura cada 1 segundo
    if (millis() - ultimaLectura > 1000) {
        byte buffer[29];
        Wire.requestFrom(HM3301_ADDR, 29);
        
        int i = 0;
        while (Wire.available() && i < 29) {
            buffer[i] = Wire.read();
            i++;
        }

        uint8_t suma = 0;
        for (int j = 0; j < 28; j++) suma += buffer[j];

        if (suma == buffer[28]) {
            pm1_0 = (uint16_t)buffer[10] << 8 | buffer[11];
            pm2_5 = (uint16_t)buffer[12] << 8 | buffer[13];
            pm10  = (uint16_t)buffer[14] << 8 | buffer[15];

            // Impresión de datos
            Serial.print(millis() / 1000);
            Serial.print("s    | ");
            Serial.print(pm1_0);
            Serial.print("   | ");
            Serial.print(pm2_5);
            Serial.print("   | ");
            Serial.print(pm10);
            Serial.print("   | ");

            // ALERTAS VISUALES CON ICONOS
            if (pm2_5 <= 12) {
                Serial.println("🟢 [AIRE SEGURO]");
            } else if (pm2_5 <= 35) {
                Serial.println("🟡 [RIESGO LEVE]");
            } else if (pm2_5 <= 55) {
                Serial.println("🟠 [RIESGO ASMATICO]");
            } else {
                Serial.println("🔴 [ALERTA DE CRISIS]");
            }
        }
        ultimaLectura = millis();
    }
}
