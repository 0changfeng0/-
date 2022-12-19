import socket
import cv2
import numpy
import time

import sys
import socket
import threading

import serial
import Jetson.GPIO as GPIO
# sys.path.insert(1, './pyKinectAzure/')

# from pyKinectAzure import pyKinectAzure, _k4a


# 添加 Azure Kinect SDK 路径
#modulePath = 'C:\\Program Files\\Azure Kinect SDK v1.4.1\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll'
# modulePath = r'/usr/lib/aarch64-linux-gnu/libk4a.so'
#对获取的深度图像进行颜色处理
# def color_depth_image(depth_image):
#     depth_color_image = cv2.convertScaleAbs(depth_image,
#                                             alpha=0.05)  # alpha is fitted by visual comparison with Azure k4aviewer results
#     depth_color_image = cv2.applyColorMap(depth_color_image, cv2.COLORMAP_JET)

#     return depth_color_image

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

    # 初始化

    img=numpy.zeros((800,800,3),numpy.uint8)

    # 建立sock连接
    # address要连接的服务器IP地址和端口号
    # address = ('103.46.128.49', 25490)
    address = ('192.168.1.101', 25490)
    try:
        # 建立socket对象
        # socket.AF_INET：服务器之间网络通信
        # socket.SOCK_STREAM：流式socket , for TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 开启连接
        sock.connect(address)
    except socket.error as msg:
        print(msg)
    k = 0
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    global channel
    channel = 22
    GPIO.setup(channel, GPIO.OUT)
    # IO=GPIO.input(22)
    GPIO.output(channel, GPIO.HIGH)
    ser = serial.Serial("/dev/ttyTHS1", 4800)  # 选择串口，并设置波特率
    while True:
        try:
            # Get capture
            # pyK4A.device_get_capture()

            # 获取深度图像
            # depth_image_handle = pyK4A.capture_get_depth_image()

            # 获取RGB图像
            # color_image_handle = pyK4A.capture_get_color_image()

            # 检查图像是否读取成功
            # if depth_image_handle and color_image_handle:
                # 停止0.1S 防止发送过快服务的处理不过来，如果服务端的处理很多，那么应该加大这个值
                time.sleep(0.01)
                color_image=img
                # 将获取到的图像转换为nummpy矩阵
                # color_image = pyK4A.image_convert_to_numpy(color_image_handle)[:, :, :3]
                # depth_image = pyK4A.image_convert_to_numpy(depth_image_handle)
                # depth_image = color_depth_image(depth_image)
                #
                cv2.namedWindow(' Color Image', cv2.WINDOW_NORMAL)
                cv2.imshow(' Color Image', color_image)
                # cv2.namedWindow(' Depth Image', cv2.WINDOW_NORMAL)
                # cv2.imshow(' Depth Image', depth_image)



                # cv2.imencode将图片格式转换(编码)成流数据，赋值到内存缓存中;主要用于图像数据格式的压缩，方便网络传输
                # '.jpg'表示将图片按照jpg格式编码。
                # img_test1=cv2.resize(color_image,(0,0),fx=0.25,fy=0.25,interpolation=cv2.INTER_AREA)
                # img_test2 = cv2.resize(depth_image, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
                # result, imgencode1 = cv2.imencode('.jpg', img_test1, encode_param)
                # result1, imgencode2 = cv2.imencode('.jpg', img_test2, encode_param)
                
                result, imgencode1 = cv2.imencode('.jpg', color_image, encode_param)
                # result1, imgencode2 = cv2.imencode('.jpg', depth_image, encode_param)
                # cv2.imwrite('new.jpg',color_image)
                # cv2.imwrite('new1.jpg',imgencode1)
                # cv2.imwrite('new2.jpg', img_test1)
                # 建立矩阵
                # sock.sendall(imgencode1)
                data1 = numpy.array(imgencode1)
                # data2 = numpy.array(imgencode2)
                # 将numpy矩阵转换成字符形式，以便在网络中传输

                stringData1 = data1.tostring()
                # stringData2 = data2.tostring()

                # 先发送要发送的数据的长度
                # ljust() 方法返回一个原字符串左对齐,并使用空格填充至指定长度的新字符串
                # sock.send(str.encode(str(len(stringData1)).ljust(16)))
                # sock.send(str.encode(str(len(stringData2)).ljust(16)))
                # 发送数据

                sock.send(stringData1)

                #sock.send(stringData2)
                # 读取服务器返回值
                data, addr = sock.recvfrom(65535)  # 接收数据和返回地址
                msg = str(data.hex())
                print(data)
                #向串口发送数据
                if ser.is_open:
                    ser_send(msg, ser)
                else:
                    print("port open failed")
                # receive = sock.recv(1024)
                # if len(receive):
                #     print(str(receive, encoding='utf-8'))
                k = cv2.waitKey(25)
                if k == 27:  # Esc
                    break

   
        except socket.error:
            # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # # 开启连接
            # sock.connect(address)
            continue


