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
    Serial.println("initial fail, retry...");
    delay(1000);
  }
  Serial.println("C4001 initial successfully");

  // 设置传感器为速度模式
  radar.setSensorMode(eSpeedMode);



  // 输出CSV格式的标题行
  Serial.println("Timestamp(ms), Target Number, Distance(m), Speed(m/s), Energy");
}

void loop() {
  // 获取当前时间戳（毫秒）
  unsigned long currentTime = millis();

  // 获取目标数量
  uint8_t targetNumber = radar.getTargetNumber();

  // 如果检测到目标
  if (targetNumber > 0) {
    // 获取目标的速度、距离和信号能量
    float targetSpeed = radar.getTargetSpeed();  // 目标速度，单位为 m/s
    float targetRange = radar.getTargetRange();  // 目标距离，单位为 m
    uint16_t targetEnergy = radar.getTargetEnergy(); // 目标信号能量

    // 输出CSV格式的数据行
    Serial.print(currentTime);  // 时间戳
    Serial.print(", ");
    Serial.print(targetNumber); // 目标数量
    Serial.print(", ");
    Serial.print(targetRange);  // 距离（米）
    Serial.print(", ");
    Serial.print(targetSpeed);  // 速度（米/秒）
    Serial.print(", ");
    Serial.println(targetEnergy); // 信号能量
  } else {
    // 如果未检测到目标，输出缺省值
    Serial.print(currentTime);  // 时间戳
    Serial.println(", 0, N/A, N/A, N/A");  // 未检测到目标时输出
  }

  // 设置合适的采集间隔，避免传感器过载（根据经验和文档推荐值设置为100ms以提高采样率）
  delay(100);
}
