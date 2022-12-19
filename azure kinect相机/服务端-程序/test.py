import cv2

# -*- coding: utf-8 -*-

import urllib
from PIL import Image
import ffmpeg
import socket
import time
import cv2
import numpy
import imagezmq
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


if __name__ == '__main__':
    #局域网内传输
    image_hub= imagezmq.ImageHub()

    while True:
        try:

            name1, image1 = image_hub.recv_image()
            frame1 = cv2.imdecode(image1, cv2.IMREAD_UNCHANGED)
            # print(frame1.shape[:2])

            image_hub.send_reply(b'OK')
            name2, image2 = image_hub.recv_image()
            frame2 = cv2.imdecode(image2, cv2.IMREAD_UNCHANGED)

            cv2.namedWindow('color image',cv2.WINDOW_NORMAL)
            cv2.imshow('color image', frame1)  # 显示图像
            cv2.namedWindow('depth image', cv2.WINDOW_NORMAL)
            cv2.imshow('depth image', frame2)  # 显示图像
            key = cv2.waitKey(25)
            if key == 27:
                break
            image_hub.send_reply(b'OK1')
        except Exception as e:
            print(e)

    cv2.destroyAllWindows()



