#服务器端
import socket
import threading
import time
import serial
import Jetson.GPIO as GPIO
# CRC16 
def calculateCRC(datalist):
    data1 = bytearray.fromhex(datalist)
    crc16 = 0xFFFF
    poly = 0xA001
    for data in data1:
        # a=int(data,16)
        crc16 = data ^ crc16
        for i in range(8):
            if 1 & (crc16) == 1:
                crc16 = crc16 >> 1
                crc16 = crc16 ^ poly
            else:
                crc16 = crc16 >> 1
    #crc16 = data_rule(crc16)
    crc16=crc16[2:4]+crc16[0:2]
    return crc16


def ser_send(msg,ser):
    global channel
    #begin_data ='55'+'0C'+'07'
    # data = list(msg)
    #msg=adjust_str(msg)
    #temp=str(msg)
    #crc16= calculateCRC(temp)

    send_data=str(msg)
    
    #print(send_data)
    send_date=bytes.fromhex(send_data)
    ser.write(send_date)
    # ser.write((msg+str(hex(crc16))[2:]+'\r\n').encode('utf-8'))  # 发送命令
    print(1)
    time.sleep(0.1)  # 延时，否则len_return_data将返回0
    #GPIO.output(channel,GPIO.LOW)
    len_return_data = ser.inWaiting()  # 获取缓冲数据（接收数据）长度
 
    #if len_return_data:
         #return_data = ser.read(len_return_data)  # 读取缓冲数据
         #print(feedback_data)
    #GPIO.output(channel,GPIO.HIGH)

def main():
    try:
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host='192.168.1.100'
        port=8080
        socket_server.bind((host, port))
        print('wait connect!')

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        global channel
        channel=22
        GPIO.setup(channel,GPIO.OUT)
        #IO=GPIO.input(22)
        GPIO.output(channel,GPIO.HIGH)
        ser = serial.Serial("/dev/ttyTHS1", 4800)  # 选择串口，并设置波特率

        # 发送消息
        while True:
            try:
                data,address = socket_server.recvfrom(1024)
                # 把接收到的东西解码
                msg = str(data.hex())
                print(str(data.hex()))
                print(address)
                socket_server.sendto(data,address)

                if ser.is_open:
                    ser_send(msg, ser)
                else:
                    print("port open failed")

            except socket.error:

                    socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    socket_server.bind(('192.168.1.100', 8080))
                    print("connect again!!!")
                    
            except BaseException as e:
                    print(e)
                    socket_server.close()
                    break
    except BaseException as e:
        print(e)
if __name__=='__main__':
    main()
