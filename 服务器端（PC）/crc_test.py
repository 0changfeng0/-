import numpy
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
    # crc16 = data_rule(crc16)
    # crc16=crc16[2:4]+crc16[0:2]

    return crc16

def data_rule(data):
        temp = ''
        if data >= 0:
            if data <= 65535:
                temp = str(hex(int(data)))[2:]
                if data <= 4095:
                    temp = '0' + str(hex(int(data)))[2:]
                    if data <= 255:
                        temp = '00' + str(hex(int(data)))[2:]
                        if data <= 15:
                            temp = '000' + str(hex(int(data)))[2:]
                            if data == 0:
                                temp = '0000'
        else:
            temp = str(hex(data & (2 ** 16 - 1)))[2:]
        return temp


def adjust_str(msg1):
    temp = msg1[2:4] + msg1[0:2] + msg1[6:8] + msg1[4:6] + msg1[10:12] + msg1[8:10] + msg1[14:16] + msg1[12:14] + msg1[
                                                                                                                  18:20] + msg1[
                                                                                                                           16:18] + msg1[
                                                                                                                                    22:24] + msg1[                                                                                                                                         20:22]
    return temp


ctr0 = 0x55
ctr1 = 10
ctr2 = 7
dx = int(0* 1000.0)

dy = int(1.0 * 1000.0)
yaw =int (0.5 * 1000.0)
xyheight = int(0.8*1000.0)
speed = int(0.04 * 1000.0)
speed1=0.4
print(speed1)
new_msg = numpy.array((ctr0, ctr1, ctr2, dx, dx >> 8, dy, dy >> 8, yaw,yaw>>8,xyheight,xyheight>>8,speed,speed>>8), dtype=numpy.uint8)
print(new_msg)
msg1=(new_msg.tostring())
msg1=msg1.hex()
print(msg1)
crc1=calculateCRC(msg1)

print(crc1)
dx1 = data_rule(dx)
dy1 = data_rule(dy)
yaw1 = data_rule(yaw)
xyheight1 = data_rule(xyheight)
speed1 = data_rule(speed)
msg = str(dx1) + str(dy1) + str(yaw1) + str(xyheight1) + str(speed1)
msg=adjust_str(msg)
# msg=adjust_str(msg)
msg2 = str(hex(int(ctr0)))[2:] + '0a' + '07' + msg
crc=calculateCRC(msg2)
print(crc)
