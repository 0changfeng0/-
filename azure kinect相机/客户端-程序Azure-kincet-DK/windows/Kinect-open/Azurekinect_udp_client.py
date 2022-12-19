import socket
import cv2
import numpy
import time

import sys

sys.path.insert(1, './pyKinectAzure/')

from pyKinectAzure import pyKinectAzure, _k4a


# 添加 Azure Kinect SDK 路径
modulePath = 'C:\\Program Files\\Azure Kinect SDK v1.4.1\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll'

#对获取的深度图像进行颜色处理
def color_depth_image(depth_image):
    depth_color_image = cv2.convertScaleAbs(depth_image,
                                            alpha=0.05)  # alpha is fitted by visual comparison with Azure k4aviewer results
    depth_color_image = cv2.applyColorMap(depth_color_image, cv2.COLORMAP_JET)

    return depth_color_image

if __name__ == '__main__':

    # 初始化
    pyK4A = pyKinectAzure(modulePath)
    pyK4A.device_open()
    device_config = pyK4A.config
    device_config.color_format = _k4a.K4A_IMAGE_FORMAT_COLOR_BGRA32
    device_config.color_resolution = _k4a.K4A_COLOR_RESOLUTION_720P
    device_config.depth_mode = _k4a.K4A_DEPTH_MODE_WFOV_2X2BINNED
    print(device_config)

    # 开启摄像头
    pyK4A.device_start_cameras(device_config)
    # 获取相机序列号
    serial_number = pyK4A.device_get_serialnum()
    print(serial_number)

    # 建立sock连接
    # address要连接的服务器IP地址和端口号
    # address = ('103.46.128.49', 25490)
    address = ('10.102.4.112', 25490)
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
    while True:
        try:
            # Get capture
            pyK4A.device_get_capture()

            # 获取深度图像
            depth_image_handle = pyK4A.capture_get_depth_image()

            # 获取RGB图像
            color_image_handle = pyK4A.capture_get_color_image()

            # 检查图像是否读取成功
            if depth_image_handle and color_image_handle:
                # 停止0.1S 防止发送过快服务的处理不过来，如果服务端的处理很多，那么应该加大这个值
                time.sleep(0.01)

                # 将获取到的图像转换为nummpy矩阵
                color_image = pyK4A.image_convert_to_numpy(color_image_handle)[:, :, :3]
                depth_image = pyK4A.image_convert_to_numpy(depth_image_handle)
                depth_image = color_depth_image(depth_image)
                #
                # cv2.namedWindow(' Color Image', cv2.WINDOW_NORMAL)
                # cv2.imshow(' Color Image', color_image)
                # cv2.namedWindow(' Depth Image', cv2.WINDOW_NORMAL)
                # cv2.imshow(' Depth Image', depth_image)



                # cv2.imencode将图片格式转换(编码)成流数据，赋值到内存缓存中;主要用于图像数据格式的压缩，方便网络传输
                # '.jpg'表示将图片按照jpg格式编码。
                # img_test1=cv2.resize(color_image,(0,0),fx=0.25,fy=0.25,interpolation=cv2.INTER_AREA)
                # img_test2 = cv2.resize(depth_image, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
                # result, imgencode1 = cv2.imencode('.jpg', img_test1, encode_param)
                # result1, imgencode2 = cv2.imencode('.jpg', img_test2, encode_param)
                result, imgencode1 = cv2.imencode('.jpg', color_image, encode_param)
                result1, imgencode2 = cv2.imencode('.jpg', depth_image, encode_param)
                # cv2.imwrite('new.jpg',color_image)
                # cv2.imwrite('new1.jpg',imgencode1)
                # cv2.imwrite('new2.jpg', img_test1)
                # 建立矩阵
                # sock.sendall(imgencode1)
                data1 = numpy.array(imgencode1)
                data2 = numpy.array(imgencode2)
                # 将numpy矩阵转换成字符形式，以便在网络中传输

                stringData1 = data1.tostring()
                stringData2 = data2.tostring()

                # 先发送要发送的数据的长度
                # ljust() 方法返回一个原字符串左对齐,并使用空格填充至指定长度的新字符串
                # sock.send(str.encode(str(len(stringData1)).ljust(16)))
                # sock.send(str.encode(str(len(stringData2)).ljust(16)))
                # 发送数据

                sock.send(stringData1)

                # sock.send(stringData2)
                # 读取服务器返回值
                # receive = sock.recv(1024)
                # if len(receive):
                #     print(str(receive, encoding='utf-8'))
                k = cv2.waitKey(25)
                if k == 27:  # Esc
                    break

            pyK4A.image_release(depth_image_handle)
            pyK4A.image_release(color_image_handle)
            pyK4A.capture_release()
        except socket.error:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 开启连接
            sock.connect(address)



    pyK4A.device_stop_cameras()
    pyK4A.device_close()