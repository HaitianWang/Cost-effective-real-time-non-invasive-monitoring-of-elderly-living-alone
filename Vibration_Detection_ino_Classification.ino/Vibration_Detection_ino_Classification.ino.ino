#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include "BluetoothSerial.h"

// Pin definitions based on your board
#define LED_PIN 17  // D17
#define BUZZER_PIN 17  // D16

// I2C address for ADXL345
#define ADXL345_ADDRESS 0x53
#define POWER_CTL_REGISTER 0x2D

// Create ADXL345 instance
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
BluetoothSerial SerialBT;  // Create BluetoothSerial instance

// Initialize packet counter
unsigned long packetCounter = 0;

void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);
  
  // Initialize Bluetooth Serial
  SerialBT.begin("ESP32_Bluetooth");

  // Initialize ADXL345 sensor
  if (!accel.begin()) {
    Serial.println("Ooops, no ADXL345 detected ... Check your wiring!");
    while (1);
  }
  
  // Set ADXL345 to measurement mode (disables low power and sleep modes)
  initializeADXL345();

  // Set sensor range to ±2g (for higher sensitivity)
  accel.setRange(ADXL345_RANGE_2_G);

  // Initialize LED and Buzzer pins
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  // Print CSV header to Bluetooth Serial
  SerialBT.println("Packet, X (m/s^2), Y (m/s^2), Z (m/s^2), State");
}

void initializeADXL345() {
  Wire.beginTransmission(ADXL345_ADDRESS);
  Wire.write(POWER_CTL_REGISTER);
  Wire.write(0x08); // 0x08 表示：进入测量模式，且无低功耗和睡眠模式
  Wire.endTransmission();
}

void loop() {
  // Get accelerometer event
  sensors_event_t event; 
  accel.getEvent(&event);

  // Default state is "Stationary"
  String state = "Stationary";
  bool isStationary = false;

  // Determine if stationary
  if ((event.acceleration.x >= 0.14 && event.acceleration.x <= 0.26) || 
      (event.acceleration.y >= 0.10 && event.acceleration.y <= 0.22)) {
    isStationary = true;
  }

  // Determine if walking
  if (!isStationary) {
    if ((event.acceleration.x >= 0.80 && event.acceleration.x <= 1.2) || 
        (event.acceleration.x >= 0 && event.acceleration.x <= 0.5) || 
        (event.acceleration.y >= 0.3 && event.acceleration.y <= 0.8)) {
      state = "Walking";
      digitalWrite(LED_PIN, HIGH);  // Turn on LED
      delay(1500);  // Keep LED on for 1 second
      digitalWrite(LED_PIN, LOW);  // Turn off LED
    } else {
      state = "Falling";
      digitalWrite(BUZZER_PIN, HIGH);  // Turn on Buzzer
      delay(1500);  // Keep Buzzer on for 1 second
      digitalWrite(BUZZER_PIN, LOW);  // Turn off Buzzer
    }
  }

  // Print packet number, accelerometer values and state to Bluetooth Serial
  SerialBT.print(packetCounter++); SerialBT.print(", ");
  SerialBT.print(event.acceleration.x); SerialBT.print(", ");
  SerialBT.print(event.acceleration.y); SerialBT.print(", ");
  SerialBT.print(event.acceleration.z); SerialBT.print(", ");
  SerialBT.println(state);
  
  // Reduce delay to increase sampling rate
  delay(100);  // Sample every 100ms, equivalent to 10Hz sampling rate
}
