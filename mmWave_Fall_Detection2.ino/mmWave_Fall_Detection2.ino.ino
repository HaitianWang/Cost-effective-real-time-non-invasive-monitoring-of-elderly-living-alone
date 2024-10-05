#include "DFRobot_C4001.h"

// 定义UART2的引脚
#define RX_PIN 21  // GPIO 21 -> C4001 TX
#define TX_PIN 22  // GPIO 22 -> C4001 RX

// 初始化C4001传感器
DFRobot_C4001_UART radar(&Serial1, 9600, RX_PIN, TX_PIN);

void setup() {
  Serial.begin(115200);
  while (!Serial);  // 等待串口连接
  
  // 初始化传感器
  while (!radar.begin()) {
    Serial.println("yes");
    delay(1000);
  }
  Serial.println("C4001 sucessful");

  // 设置传感器模式
  radar.setSensorMode(eSpeedMode);  // 可以根据需要设置为 eSpeedMode 或 eExitMode
  
  // 输出CSV格式的标题行
  Serial.println("Timestamp, Distance(m), Speed(m/s)");
}

void loop() {
  unsigned long currentTime = millis();  // 获取当前时间戳（毫秒）

  uint8_t targetNumber = radar.getTargetNumber();  // 获取目标数量

  // 如果检测到目标
  if (targetNumber > 0) {
    float targetSpeed = radar.getTargetSpeed();      // 获取目标速度
    float targetRange = radar.getTargetRange();      // 获取目标距离

    // 输出CSV格式的数据行
    Serial.print(currentTime);    // 时间戳
    Serial.print(", ");
    Serial.print(targetRange);    // 距离（米）
    Serial.print(", ");
    Serial.println(targetSpeed);    // 速度（米/秒）
  } else {
    // 如果未检测到目标，输出缺省值
    Serial.print(currentTime);    // 时间戳
    Serial.print(", N/A, N/A");  // 没有检测到数据
    Serial.println();
  }

  delay(100);  // 设置采集间隔
}
