#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include "BluetoothSerial.h"  // 包含蓝牙串口库

// 创建ADXL345加速度计实例
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
BluetoothSerial SerialBT;  // 创建蓝牙串口实例
unsigned long startTime;

void setup() {
  // 启用串口监视器
  Serial.begin(115200);
  
  // 启用蓝牙串口
  SerialBT.begin("ESP32_Bluetooth");  // 蓝牙设备名可以根据需求修改
  
  // 初始化传感器
  if(!accel.begin()) {
    Serial.println("Ooops, no ADXL345 detected ... Check your wiring!");
    while(1);
  }
  
  // 设置量程为±2g（更高的灵敏度）
  accel.setRange(ADXL345_RANGE_2_G);
  
  // 记录开始时间
  startTime = millis();
  
  // 输出CSV文件的表头到蓝牙串口
  SerialBT.println("X (m/s^2), Y (m/s^2), Z (m/s^2)");
}

void loop() {
  // 获取加速度计事件
  sensors_event_t event; 
  accel.getEvent(&event);
  
  // 输出CSV格式的加速度值到蓝牙串口
  SerialBT.print(event.acceleration.x); SerialBT.print(", ");
  SerialBT.print(event.acceleration.y); SerialBT.print(", ");
  SerialBT.println(event.acceleration.z);
  
  // 减少延迟，提高采样率
  delay(10);  // 每10毫秒采样一次，相当于100Hz采样率
}
