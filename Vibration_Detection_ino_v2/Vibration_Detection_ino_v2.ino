#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>

// 创建ADXL345加速度计实例
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
unsigned long startTime;

void setup() {
  // 以115200波特率启动串口通信
  Serial.begin(115200);
  
  // 初始化传感器
  if(!accel.begin()) {
    Serial.println("Ooops, no ADXL345 detected ... Check your wiring!");
    while(1);
  }
  
  // 设置量程为±16g
  accel.setRange(ADXL345_RANGE_16_G);
  
  // 记录开始时间
  startTime = millis();
  
  // 输出CSV文件的表头
  Serial.println("Timestamp (ms), X (m/s^2), Y (m/s^2), Z (m/s^2)");
}

void loop() {
  // 获取加速度计事件
  sensors_event_t event; 
  accel.getEvent(&event);
  
  // 获取当前时间戳
  unsigned long currentTime = millis() - startTime;
  
  // 输出CSV格式的加速度值和时间戳
  Serial.print(currentTime); Serial.print(", ");
  Serial.print(event.acceleration.x); Serial.print(", ");
  Serial.print(event.acceleration.y); Serial.print(", ");
  Serial.println(event.acceleration.z);
  
  // 延迟100毫秒
  delay(100);
}
