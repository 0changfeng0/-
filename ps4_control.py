import pygame
import time
import numpy as np
import math
import sys
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中

#导入designer工具生成的login模块
from login import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#pyuic5 -o login.py login.ui
class JoyStick(object):
    def __init__(self, id):
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            raise Exception("Joystick not found!")

        self.joystick = pygame.joystick.Joystick(id)
        self.joystick.init()

        self.axis = np.zeros(self.joystick.get_numaxes())
        self.__alpha = 0.0

        self.button = [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]
        self.hat = [self.joystick.get_hat(i) for i in range(self.joystick.get_numhats())]

        self.lst_button = [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]
        self.lst_hat = [self.joystick.get_hat(i) for i in range(self.joystick.get_numhats())]

        self.button_click = self._check_button_click(self.lst_button, self.button)
        self.hat_click = self._check_hat_click(self.lst_hat, self.hat)

        self.dead_zone = 0.1

    @staticmethod
    def _check_button_click(lst, cur):
        rise = [0] * len(lst)
        for i in range(len(lst)):
            if not lst[i] and cur[i]:
                rise[i] = 1
        return rise

    @staticmethod
    def _check_hat_click(lst, cur):
        rise = [(0, 0)] * len(lst)
        for i in range(len(lst)):
            h0 = 1 if not lst[i][0] and cur[i][0] else 0
            h1 = 1 if not lst[i][1] and cur[i][1] else 0
            rise[i] = (h0, h1)
        return rise

    @staticmethod
    def count():
        pygame.init()
        return pygame.joystick.get_count()

    @staticmethod
    def device_name(id):
        if id < JoyStick.count():
            return pygame.joystick.Joystick(id).get_name()
        else:
            return None

    def name(self):
        return self.joystick.get_name()

    def refresh(self):
        pygame.event.pump()

        for i in range(self.joystick.get_numaxes()):
            axis = self.joystick.get_axis(i)
            self.axis[i] = self.axis[i] * self.__alpha + axis * (1.0 - self.__alpha)
            if -self.dead_zone < self.axis[i] < self.dead_zone:
                self.axis[i] = 0

        self.lst_button = self.button
        self.lst_hat = self.hat

        self.button = [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]
        self.hat = [self.joystick.get_hat(i) for i in range(self.joystick.get_numhats())]

        self.button_click = self._check_button_click(self.lst_button, self.button)
        self.hat_click = self._check_hat_click(self.lst_hat, self.hat)

class PS4Robot(object):
    def __init__(self, id=0):

        self.ps4 = JoyStick(id)
        if self.ps4.name().find("PS4") < 0:
            raise Exception("No a PS4 handle")

        self.dx = 0.0
        self.dy = 0.0
        self.step = 0.0
        self.yaw = 0.0
        self.speed = 0.0

    def refresh(self):
        self.ps4.refresh()

        x = self.ps4.axis[2]
        y = -self.ps4.axis[3]
        xy = math.sqrt(x * x + y * y)
        if xy < 0.1:
            self.dx = 0.0
            self.dy = 0.0
            self.step = 0.0
        else:
            self.dx = x / xy
            self.dy = y / xy
            self.step = max(math.fabs(x), math.fabs(y))
        self.yaw = self.ps4.axis[0]

        if self.ps4.button_click[3]:
            self.speed += 0.1
        elif self.ps4.button_click[0]:
            self.speed -= 0.1
        self.speed = min(1.0, max(0.0, self.speed))

        # print("Yaw = %3.1f" % self.yaw)
        # print("Speed = %3.1f" % self.speed)
class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, robot,parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.robot=robot
        self.pushButton_2.clicked.connect(self.close)
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.display)
        self.timer.start(100)
        # 添加退出按钮信号和槽。调用close函数


    def display(self):
        robot.refresh()
        self.line_2.setGeometry(QtCore.QRect(130+self.robot.yaw*80, 30, 20, 31))
        temp=80
        self.line_3.setGeometry(QtCore.QRect(125+self.robot.dx*temp, 202-self.robot.dy*temp, 50, 20))

        self.line_4.setGeometry(QtCore.QRect(140+self.robot.dx*temp, 187-self.robot.dy*temp, 20, 50))

        self.line_10.setGeometry(QtCore.QRect(299, 300-self.robot.step*200, 20, 20+self.robot.step*200))
        # 利用text Browser控件对象setText()函数设置界面显示
        self.progressBar.setProperty("value",self.robot.speed*100)
        self.textBrowser.setText("连接成功!\n" + "x: " + str(self.robot.dx) + "\n"+"y： "+str(self.robot.dy)+"\n"+"step: " + str(self.robot.step) +"\n"+ "yaw: " + str(self.robot.yaw)+"\n"+"speed: " + str(self.robot.speed))



if __name__ == '__main__':
    #plane = BoomJoystick()
    #PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    robot = PS4Robot()
    print(robot.ps4.name())
    myWin = MyMainForm(robot)


    #将窗口控件显示在屏幕上
    myWin.show()

        #程序运行，sys.exit方法确保程序完整退出。
    myWin.display()
    time.sleep(0.1)
    sys.exit(app.exec_())

