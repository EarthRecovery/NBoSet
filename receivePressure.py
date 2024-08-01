import serial
import time
from picamera2 import Picamera2, Preview
from time import sleep

pre = 0

# 设置蓝牙串口设备名称
port = '/dev/rfcomm0'  

# 初始化串口对象
ser = serial.Serial(port, 9600)

# 清空串口接收缓冲区
ser.flushInput()

while (pre == 0):
    try:
        # 检查是否有数据
        n = ser.inWaiting()
        if n:
            # 读取数据
            str_data = ser.read(n).decode('utf-8')
            data = int(str_data) # 转换成数字
            print(f"接收到的数据: {data}")
            if(data > 300):
                pre = 1
            
        # 延迟一段时间
        sleep(1)

    except serial.SerialException as e:
        print(f"串口错误: {e}")
        # 可以尝试重新连接串口设备

    except KeyboardInterrupt:
        print("程序结束")
        ser.close()
        break
        
if(pre == 1):
    picam2=Picamera2()
    camera_config=picam2.create_preview_configuration()
    picam2.configure(camera_config)
    picam2.start_preview(Preview.QTGL)
    picam2.start()
    time.sleep(2)
    picam2.capture_file("test.jpg")
else:
    print("No picture taken")
