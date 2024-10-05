#include <Wire.h>
#include <HardwareSerial.h>
#include <esp_timer.h>
#include "BluetoothSerial.h"

// 定义用于 mmWave 传感器的 UART 引脚
#define RX_PIN 16  // GPIO16 for RX
#define TX_PIN 17  // GPIO17 for TX

// 初始化两个 UART
HardwareSerial mmWaveSerial(2);  // 使用 UART2
BluetoothSerial SerialBT;        // 使用经典蓝牙
unsigned long packetCounter = 0;

void setup() {
  // 初始化 mmWave 传感器 UART 通信
  mmWaveSerial.begin(115200, SERIAL_8N1, RX_PIN, TX_PIN);
  
  // 初始化经典蓝牙通信
  SerialBT.begin("ESP32_MMWave_Classic");

  // 输出列标题
  SerialBT.println("Packet Number, Timestamp(ms), Range(m), Velocity(m/s), Angle(deg), Signal Strength(dB)");

  // 初始化 UART0 以进行串口监视器通信（调试用）
  Serial.begin(115200);
}

void loop() {
  // 从 mmWave 传感器读取数据
  if (mmWaveSerial.available()) {
    String sensorData = mmWaveSerial.readStringUntil('\n');
    
    if (sensorData.startsWith("$") && sensorData.endsWith("*")) {
      sensorData = sensorData.substring(1, sensorData.length() - 1);
      
      float range, velocity, angle, signalStrength;
      int parsedItems = sscanf(sensorData.c_str(), "%f,%f,%f,%f", &range, &velocity, &angle, &signalStrength);

      if (parsedItems == 4) {
        unsigned long currentTime = esp_timer_get_time() / 1000;
        packetCounter++;

        // 格式化数据为 CSV 格式字符串
        char buffer[100];
        sprintf(buffer, "%lu,%lu,%.2f,%.2f,%.2f,%.2f", packetCounter, currentTime, range, velocity, angle, signalStrength);

        if (SerialBT.hasClient()) {
          // 通过经典蓝牙发送数据
          SerialBT.println(buffer);
        }

        // 也输出到串口监视器（调试用）
        Serial.println(buffer);
      }
    }
  }

  delay(100);
}
