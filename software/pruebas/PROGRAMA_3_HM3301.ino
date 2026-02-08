/*
 * =========================================================================
 * TEST SENSOR DE PARTÍCULAS HM3301 - CANSAT RAM
 * =========================================================================
 * CONEXIÓN I2C:
 * - VCC: 3.3V o 5V
 * - GND: GND
 * - SDA: Pin A4 (Nano 33 BLE)
 * - SCL: Pin A5 (Nano 33 BLE)
 * * NOTA: Este sensor mide concentración de polvo/partículas PM1.0, PM2.5 y PM10.
 * =========================================================================
 */

#include <Seeed_HM3301.h>

HM3301 sensor;
uint8_t buf[29];

void setup() {
    Serial.begin(9600);

    // --- CONTROL DE ARRANQUE AUTÓNOMO (ESPERA INTELIGENTE) ---
    unsigned long ventanaInicio = millis();
    while (!Serial && millis() - ventanaInicio < 5000) {
        // Espera 5s al USB; si no hay, arranca solo para la misión.
        // Esto permite que la batería tome el control si no hay PC.
    }

    Serial.println("Iniciando HM3301...");

    if (sensor.init()) {
        Serial.println(">>> ERROR: HM3301 no detectado. Revisa cables I2C <<<");
        while (1);
    }
    
    Serial.println("HM3301 OK! Leyendo datos...");
    Serial.println("Tiempo(s)\tPM1.0\tPM2.5\tPM10 (ug/m3)");
    Serial.println("----------------------------------------------");
}

void loop() {
    if (sensor.read_sensor_value(buf, 29)) {
        Serial.println("Error al leer del sensor");
        return;
    }

    // El sensor entrega los datos en el buffer. 
    // Los valores estándar (CF=1) están en las posiciones:
    // PM1.0: bytes 10-11 | PM2.5: bytes 12-13 | PM10: bytes 14-15
    uint16_t pm1_0 = (uint16_t)buf[10] << 8 | buf[11];
    uint16_t pm2_5 = (uint16_t)buf[12] << 8 | buf[13];
    uint16_t pm10  = (uint16_t)buf[14] << 8 | buf[15];

    // Imprimir resultados cada segundo
    static unsigned long ultimaMuestra = 0;
    if (millis() - ultimaMuestra > 1000) {
        Serial.print(millis() / 1000); Serial.print("s\t\t");
        Serial.print(pm1_0);           Serial.print("\t");
        Serial.print(pm2_5);           Serial.print("\t");
        Serial.println(pm10);
        
        ultimaMuestra = millis();
    }
}