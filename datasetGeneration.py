import serial
import time
from picamera2 import Picamera2, Preview
from time import sleep

n = 0

# 设置蓝牙串口设备名称
port0 = '/dev/rfcomm0' 
port1 = '/dev/rfcomm1' 

# 初始化串口对象
ser0 = serial.Serial(port0, 9600)
ser1 = serial.Serial(port1, 9600)

# 压力阈值
PRESSURE_THRESHOLD = 300

# 清空串口接收缓s冲区
ser0.flushInput()
ser1.flushInput()

# Dataset initialize
pressure_list = []
body_list = []
image_name_list = []
length = 0

# picam initialize
picam2=Picamera2()
camera_config=picam2.create_preview_configuration(main={"size": (1920,1080)})
picam2.configure(camera_config)
#picam2.start_preview(Preview.QTGL)
picam2.start()
    
# 拍一张照
def getCapture(picture_name, pressure, body):
    picam2.capture_file(picture_name)

# 每次触发向数据集写一行
def generateDataset(pressure, body, picture_name):
    global length
    pressure_list.append(pressure)
    body_list.append(body)
    image_name_list.append(picture_name)
    length += 1

# 结束后写入数据集csv文件存储起来
def writeDataset(datasetName):
    with open(datasetName,'a') as f:
        f.write("pressure,body, image_name" + '\n')
        for i in range(length):
            f.write(str(pressure_list[i]) + ',' + str(body_list[i]) + ','+ str(image_name_list[i]) + '\n')
    
print("start camera")

# 主循环
while (True):
    try:
        # 检查是否有数据
        n0 = ser0.inWaiting()
        n1 = ser1.inWaiting()
        if n0 and n1:
            # 读取数据
            print("----------------\n")
            str_data1 = ser0.read(n0).decode('utf-8')
            print(f"第一个蓝牙：{str_data1}")
            str_data2 = ser1.read(n1).decode('utf-8')
            print(f"第二个蓝牙：{str_data2}")

            pressure = int(str_data1)
            body = int(str_data2)
            if(body):
                picture_name = "./image/" + time.asctime() + ".jpg"
            else:
                picture_name = "None"
            # 将数据存入数据集
            generateDataset(pressure, body, picture_name)
            getCapture(picture_name, pressure, body)
            print("get camera")
            
        # 延迟一段时间
        ser0.flushInput()
        ser1.flushInput()
        sleep(1)

    except serial.SerialException as e:
        print(f"串口错误: {e}")
        # 可以尝试重新连接串口设备

    except KeyboardInterrupt:
        print("程序结束")
        # 写入数据集csv文件
        writeDataset("dataset.csv")
        ser.close()
        break
