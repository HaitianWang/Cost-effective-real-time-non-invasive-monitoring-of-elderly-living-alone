import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# 初始化蓝牙串口连接
bluetooth_serial = serial.Serial('COM8', 115200, timeout=1)  # 请替换为正确的COM端口号

# 初始化图形
fig, ax = plt.subplots()
magnitude_data, time_data = [], []

# 初始化绘图参数
line, = ax.plot([], [], label='Magnitude of Acceleration (m/s^2)', color='m')

def init():
    ax.set_xlim(0, 10)  # x轴初始范围为10秒
    ax.set_ylim(0, 20)  # 合成加速度的假定范围
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Magnitude (m/s^2)')
    ax.legend()
    return line,

def update(frame):
    try:
        # 读取蓝牙数据并解析
        data = bluetooth_serial.readline().decode('utf-8').strip()
        if data:
            print(f"Received: {data}")
            x_str, y_str, z_str, state = data.split(', ')
            x = float(x_str)
            y = float(y_str)
            z = float(z_str)
            current_time = time.time()

            # 计算合成加速度的模
            magnitude = np.sqrt(x**2 + y**2 + z**2)

            # 更新数据
            magnitude_data.append(magnitude)
            time_data.append(current_time)

            # 更新绘图数据
            line.set_data(np.array(time_data) - time_data[0], magnitude_data)

            # 动态调整x轴范围
            ax.set_xlim(time_data[-1] - time_data[0] - 10, time_data[-1] - time_data[0])
            ax.figure.canvas.draw()

    except Exception as e:
        print(f"Error: {e}")

    return line,

ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=50)

plt.show()
