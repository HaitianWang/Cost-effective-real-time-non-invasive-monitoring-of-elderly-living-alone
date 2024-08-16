import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from collections import deque

# 初始化蓝牙串口连接
bluetooth_serial = serial.Serial('COM8', 115200, timeout=1)  # 请替换为正确的COM端口号

# 初始化图形
fig, ax = plt.subplots()
x_data, y_data, z_data, time_data = deque(maxlen=1000), deque(maxlen=1000), deque(maxlen=1000), deque(maxlen=1000)

# 初始化绘图参数
line_x, = ax.plot([], [], label='X-axis (m/s^2)', color='r')
line_y, = ax.plot([], [], label='Y-axis (m/s^2)', color='g')
line_z, = ax.plot([], [], label='Z-axis (m/s^2)', color='b')

def init():
    ax.set_xlim(0, 10)  # x轴初始范围为10秒
    ax.set_ylim(-10, 10)  # 假定加速度范围为±10m/s^2
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Acceleration (m/s^2)')
    ax.legend()
    return line_x, line_y, line_z

def update(frame):
    try:
        # 读取蓝牙数据并解析
        data = bluetooth_serial.readline().decode('utf-8').strip()
        if data:
            print(f"Received: {data}")
            packet_number, x_str, y_str, z_str, state = data.split(', ')
            x = float(x_str)
            y = float(y_str)
            z = float(z_str)
            current_time = time.time()

            # 更新数据
            x_data.append(x)
            y_data.append(y)
            z_data.append(z)
            time_data.append(current_time)

            # 显示包编号和其他信息
            print(f"Packet {packet_number}: X={x}, Y={y}, Z={z}, State={state}")

            # 更新绘图数据
            line_x.set_data(np.array(time_data) - time_data[0], x_data)
            line_y.set_data(np.array(time_data) - time_data[0], y_data)
            line_z.set_data(np.array(time_data) - time_data[0], z_data)

            # 动态调整x轴范围
            ax.set_xlim(max(0, time_data[-1] - time_data[0] - 10), max(10, time_data[-1] - time_data[0]))
            ax.figure.canvas.draw()

    except Exception as e:
        print(f"Error: {e}")

    return line_x, line_y, line_z

# 将更新间隔调整为100ms，减少绘图频率
ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=100)

plt.show()
