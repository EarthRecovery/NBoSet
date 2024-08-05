import serial
import time
from picamera2 import Picamera2, Preview
from time import sleep

pre = 0
body = 0

# 设置蓝牙串口设备名称
portPre = '/dev/rfcomm0'
portBody = '/dev/rfcomm1'

# 初始化串口对象
ser1 = serial.Serial(portPre, 9600)
ser2 = serial.Serial(portBody, 9600)

# 清空串口接收缓冲区
ser1.flushInput()
ser2.flushInput()

while (pre == 0):
    try:
        # 检查是否有数据
        n = ser1.inWaiting()
        m = ser2.inWaiting()
        # if n:
        #     # 读取数据
        #     str_data1 = ser1.read(n).decode('utf-8')
        #     data1 = int(str_data1) # 转换成数字
        #     print(f"接收到的数据: {data1}")
        #     str_data2 = ser2.read(m).decode('utf-8')
        #     str_data2_list = str_data2.split('\r\n')
        #     data2 = int(str_data2_list[0]) # 转换成数字
        #     print(f"接收到的数据: {data2}")
        #     if(data1 > 300):
        #         pre = 1

        if n and m:
            print("----------------\n")
            str_data1 = ser1.read(n).decode('utf-8')
            print(f"第一个蓝牙：{str_data1}")
            str_data2 = ser2.read(m).decode('utf-8')
            print(f"第二个蓝牙：{str_data2}")
            
        # 延迟一段时间
        ser1.flushInput()
        ser2.flushInput()
        sleep(1)
        

    except serial.SerialException as e:
        print(f"串口错误: {e}")
        # 可以尝试重新连接串口设备

    except KeyboardInterrupt:
        print("程序结束")
        ser.close()
        break
