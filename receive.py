import serial
from time import sleep

# 设置蓝牙串口设备名称
port = '/dev/rfcomm1'  

# 初始化串口对象
ser = serial.Serial(port, 9600)

# 清空串口接收缓冲区
ser.flushInput()

while True:
    try:
        # 检查是否有数据
        n = ser.inWaiting()
        if n:
            # 读取数据
            data = ser.read(n).decode('utf-8')
            print(f"接收到的数据: {data}")

        # 延迟一段时间
        sleep(0.1)

    except serial.SerialException as e:
        print(f"串口错误: {e}")
        # 可以尝试重新连接串口设备

    except KeyboardInterrupt:
        print("程序结束")
        ser.close()
        break
