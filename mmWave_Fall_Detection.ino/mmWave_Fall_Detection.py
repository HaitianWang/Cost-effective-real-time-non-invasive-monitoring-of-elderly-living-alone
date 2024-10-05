import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


ser = serial.Serial('COM6', 115200, timeout=1)

data_points = []

# 从串口读取并处理数据
def read_data():
    if ser.in_waiting:
        try:
            line = ser.readline().decode('utf-8').strip()
            print(f"Received: {line}")
            packet, timestamp, range_, velocity, angle, signal_strength = map(float, line.split(","))
            data_points.append((range_, velocity, angle, signal_strength))
        except ValueError:
            print("Failed to parse data")

# 动态绘图
def animate(i):
    if data_points:
        plt.cla()
        ranges = [dp[0] for dp in data_points]
        velocities = [dp[1] for dp in data_points]
        plt.plot(ranges, label="Range")
        plt.plot(velocities, label="Velocity")
        plt.legend(loc='upper right')
        plt.tight_layout()

if __name__ == "__main__":
    ani = FuncAnimation(plt.gcf(), animate, interval=1000)

    try:
        while True:
            read_data()
            plt.pause(0.1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()
