#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>

// 创建ADXL345加速度计实例
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);

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
  
  // 显示传感器详情
  displaySensorDetails();
}

void loop() {
  // 获取加速度计事件
  sensors_event_t event; 
  accel.getEvent(&event);
  
  // 显示x, y, z轴的数据
  Serial.print("X: "); Serial.print(event.acceleration.x); Serial.print(" ");
  Serial.print("Y: "); Serial.print(event.acceleration.y); Serial.print(" ");
  Serial.print("Z: "); Serial.print(event.acceleration.z); Serial.print(" ");
  Serial.println("m/s^2 ");
  
  // 延迟100毫秒
  delay(100);
}

void displaySensorDetails(void) {
  sensor_t sensor;
  accel.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" m/s^2");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" m/s^2");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" m/s^2");  
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
}
