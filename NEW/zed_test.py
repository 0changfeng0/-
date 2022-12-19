import sys
import socket
import threading

import serial
import Jetson.GPIO as GPIO

import pyzed.sl as sl
import time
import cv2
import numpy as np
from ZEDCamera import ZEDCamera

def ser_send(msg, ser):
    global channel
    # begin_data ='55'+'0C'+'07'
    # data = list(msg)
    # msg=adjust_str(msg)
    # temp=str(msg)
    # crc16= calculateCRC(temp)
    send_data = str(msg)
    # print(send_data)
    send_date = bytes.fromhex(send_data)
    ser.write(send_date)
    # ser.write((msg+str(hex(crc16))[2:]+'\r\n').encode('utf-8'))  # 发送命令
    print(1)
    time.sleep(0.1)  # 延时，否则len_return_data将返回0
    # GPIO.output(channel,GPIO.LOW)
    len_return_data = ser.inWaiting()  # 获取缓冲数据（接收数据）长度

    # if len_return_data:
    # return_data = ser.read(len_return_data)  # 读取缓冲数据
    # print(feedback_data)
    # GPIO.output(channel,GPIO.HIGH)
if __name__ == '__main__':

        # 建立sock连接
    # address要连接的服务器IP地址和端口号
    # address = ('103.46.128.49', 25490)
    address = ('192.168.1.101', 25490)
    # try:
    #     # 建立socket对象
    #     # socket.AF_INET：服务器之间网络通信
    #     # socket.SOCK_STREAM：流式socket , for TCP
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     # 开启连接
    #     sock.connect(address)
    # except socket.error as msg:
    #     print(msg)
    k = 0
    # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    global channel
    channel = 22
    GPIO.setup(channel, GPIO.OUT)
    # IO=GPIO.input(22)
    GPIO.output(channel, GPIO.HIGH)
    ser = serial.Serial("/dev/ttyTHS1", 4800)  # 选择串口，并设置波特率
    #set ZED-camera!
    cameras = ZEDCamera.enum_cameras()
    print("installed zed cameras:")
    print(cameras)

    camera1 = ZEDCamera(cameras[0], resolution=720, camera_fps=15, depth_min=400, depth_max=5000, streaming=True)

    key = 0
    while True:
        try:

            camera1.refresh()
            img = camera1.get_RGBimage()
            cv2.imshow("", img)
            stringData1='success send!'
            # sock.send(stringData1.encode())
            
            #end=time.time()
            #print(end-start)                
            #sock.send(stringData2)
            #time.sleep(0.05)
            # 读取服务器返回值

            # data, addr = sock.recvfrom(65535)  # 接收数据和返回地址

            #msg = str(data.hex())
            #print(str(data.hex()))

            #向串口发送数据
            # if ser.is_open:
            #     ser_send(data, ser)
            # else:
            #     print("port open failed")

            # receive = sock.recv(1024)
            # if len(receive):
            #     print(str(receive, encoding='utf-8'))
            key = cv2.waitKey(50) & 0xFF
            if (key == ord('e') or key == ord('E')):
                break
        except  BaseException as ex:
            print(ex)

        # except socket.error:

        #     #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #     # 开启连接
        #     #sock.connect(address)
        #     print('connect error!')
        #     continue
