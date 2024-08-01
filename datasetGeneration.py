import serial
import time
from picamera2 import Picamera2, Preview
from time import sleep

n = 0

# 设置蓝牙串口设备名称
port = '/dev/rfcomm0'  

# 初始化串口对象
ser = serial.Serial(port, 9600)

# 压力阈值
PRESSURE_THRESHOLD = 300

# 清空串口接收缓冲区
ser.flushInput()

# Dataset initialize
pressure_list = []
image_name_list = []
over_threshold_list = []
length = 0

# picam initialize
picam2=Picamera2()
camera_config=picam2.create_preview_configuration(main={"size": (1920,1080)})
picam2.configure(camera_config)
#picam2.start_preview(Preview.QTGL)
picam2.start()
    
# 拍一张照
def getCapture(picture_name):
    time.sleep(0.2)
    picam2.capture_file(picture_name)

# 每次触发向数据集写一行
def generateDataset(pressure, picture_name, success):
    global length
    pressure_list.append(pressure)
    image_name_list.append(picture_name)
    over_threshold_list.append(success)
    length +=1

# 结束后写入数据集csv文件存储起来
def writeDataset(datasetName):
    with open(datasetName,'a') as f:
        # f.write("pressure,image_name,over_threshold" + '\n')
        for i in range(length):
            f.write(str(pressure_list[i]) + ',' + str(image_name_list[i]) + ',' + str(over_threshold_list[i]) + '\n')
    
print("start camera")

# 主循环
while (True):
    try:
        # 检查是否有数据
        n = ser.inWaiting()
        if n:
            # 读取数据
            str_data = ser.read(n).decode('utf-8')
            # 去除干扰数据
            if(str_data == ''):
                continue
            pressure = int(str_data)
            print(f"接收到的数据: {pressure}")
            picture_name = "./image/" + time.asctime() + ".jpg"
            # 将数据存入数据集
            generateDataset(pressure, picture_name, pressure > PRESSURE_THRESHOLD)
            # 高于阈值就拍照
            if(pressure > PRESSURE_THRESHOLD): # 拍照
                getCapture(picture_name)
                print("get camera")
            
        # 延迟一段时间
        sleep(0.05)

    except serial.SerialException as e:
        print(f"串口错误: {e}")
        # 可以尝试重新连接串口设备

    except KeyboardInterrupt:
        print("程序结束")
        # 写入数据集csv文件
        writeDataset("dataset.csv")
        ser.close()
        break
