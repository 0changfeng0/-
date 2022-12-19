# -*- coding: utf-8 -*-


import socket
import time
import cv2
import numpy
def img_encode(img):
    result, img_code = cv2.imencode('.jpg', img)
    return img_code
def img_decode(img):
    # flag:IMREAD_GRAYSCALE(无论传入哪种类型，都将以灰度图保存)

    # IMREAD_UNCHANGED(传入什么类型的图片，就保存成什么类型的)
    #
    # IMREAD_COLOR(无论传入哪种类型，都将以彩色图保存)
    frame = cv2.imdecode(img, cv2.IMREAD_GRAYSCALE)
    return frame

def Tcp_connecct(address):

    # 建立socket对象
    # socket.AF_INET：服务器之间网络通信
    # socket.SOCK_STREAM：流式socket , for TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 将套接字绑定到地址, 在AF_INET下,以元组（host,port）的形式表示地址.
    s.bind(address)
    # 开始监听TCP传入连接。参数指定在拒绝连接之前，操作系统可以挂起的最大连接数量。
    s.listen(5)
    print("wait connect")
    conn, addr = s.accept()
    print('connect from:' + str(addr))
    return s,conn,addr

def UDP_connect():
    HOST = '192.168.191.122'
    PORT = 9999
    buffSize = 65535
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建socket对象
    server.bind((HOST, PORT))
    return server
def recvall(sock, count):
    buf = b''  # buf是一个byte类型
    while count:
        # 接受TCP套接字的数据。数据以字符串形式返回，count指定要接收的最大数据量.
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf
if __name__ == '__main__':
    address = ('0.0.0.0', 8080)
    s,conn,addr=Tcp_connecct(address)

    while True:
        try:
            start = time.time()  # 用于计算帧率信息

            length1 = recvall(conn, 16)  # 获得图片文件的长度,16代表获取长度
            length2 = recvall(conn, 16)  # 获得图片文件的长度,16代表获取长度

            stringData1 = recvall(conn, int(length1))  # 根据获得的文件长度，获取图片文件
            stringData2 = recvall(conn, int(length2))  # 根据获得的文件长度，获取图片文件

            data1 = numpy.frombuffer(stringData1, numpy.uint8)  # 将获取到的字符流数据转换成1维数组
            data2 = numpy.frombuffer(stringData2, numpy.uint8)  # 将获取到的字符流数据转换成1维数组

            decimg1 = cv2.imdecode(data1, cv2.IMREAD_UNCHANGED)  # 将数组解码成图像
            decimg2 = cv2.imdecode(data2, cv2.IMREAD_UNCHANGED)  # 将数组解码成图像

            cv2.namedWindow('color image',cv2.WINDOW_NORMAL)
            cv2.imshow('color image', decimg1)  # 显示图像
            cv2.namedWindow('depth image', cv2.WINDOW_NORMAL)
            cv2.imshow('depth image', decimg2)  # 显示图像

            # 将帧率信息回传
            end = time.time()
            seconds = end - start
            fps = 1 / seconds
            conn.send(bytes(str(int(fps)), encoding='utf-8'))
            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break
        except socket.error:
            address = ('0.0.0.0', 8080)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(address)
            s.listen(5)
            print("wait connect")
            conn, addr = s.accept()
            print('connect from:' + str(addr))
        except BaseException as e:
            cv2.destroyAllWindows()
            address = ('0.0.0.0', 8080)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(address)
            s.listen(5)
            print("wait connect")
            conn, addr = s.accept()
            print('connect from:' + str(addr))

    s.close()
    cv2.destroyAllWindows()
