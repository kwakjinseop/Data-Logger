import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import serial, time
import pyqtgraph as pg

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


form_class = uic.loadUiType("design.ui")[0]

ser = serial.Serial(
    port='COM5',
    baudrate=9600
)


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        ####### 상단 메뉴바 조작##########################
        self.menu.setEnabled(False)
        self.menu_2.setEnabled(False)
        self.radioButton_14.clicked.connect(self.menu_able)
        self.radioButton_15.clicked.connect(self.menu_disable)
        self.radioButton_16.clicked.connect(self.menu_disable)
        self.radioButton_8.clicked.connect(self.stopmenu_able)
        self.radioButton_5.clicked.connect(self.stopmenu_disable)
        self.radioButton_7.clicked.connect(self.stopmenu_disable)
        #########메뉴바 속 세부 메뉴들 조작##########################
        self.actionStart.triggered.connect(self.DCIstart)
        self.actionDCV.triggered.connect(self.DCVstart)
        self.actionAll_Start.triggered.connect(self.ALLstart)
        self.actionStop.triggered.connect(self.DCIstop)
        self.actionDCV_Stop.triggered.connect(self.DCVstop)
        self.actionAll_Stop.triggered.connect(self.ALLstop)
        #########timeedit 박스의 시간반환##################
        self.dateTimeVar = self.dateTimeEdit.dateTime()

        ############그래프 위젯 삽입하는 부분#################
        self.widget = Graphplace(Dialog)







    def menu_able(self):
        self.menu.setEnabled(True)

    def menu_disable(self):
        self.menu.setEnabled(False)

    def stopmenu_able(self):
        self.menu_2.setEnabled(True)

    def stopmenu_disable(self):
        self.menu_2.setEnabled(False)





    def DCIstart(self): #일단은 기능전환은 되는 것 확인, 하지만 오류 남아있음
        print("Clicked DCI")
        Currc = ':SENS:FUNC "CURR:DC"\r\n'
        currentchange = Currc.encode()
        ser.write(currentchange) #여기까지가 기능변경 코드
        self.widget = PlotWidget(Dialog)





    def DCVstart(self):
        print("Clicked DCV")
        voltc = ':SENS:FUNC "VOLT:DC"\r\n'  # 기능 변경 구문 8.10현재 기능변경만 가능하고 출력은 안되는 문제있음.
        voltchange = voltc.encode()
        ser.write(voltchange)
        Datachange = ':SENS:DATA?\r\n'
        datachange = Datachange.encode()
        ser.write(datachange)
        time.sleep(0.5)
        out = ''
        # out = out.rstrip()
        stamp = time.time()
        tm = time.localtime(stamp)
        hour = tm.tm_hour
        minute = tm.tm_min
        sec = tm.tm_sec
        string = ""

        while ser.inWaiting() > 0:  # ser.inWaiting == 16
            out += ser.read().decode()
        print(out)

    def ALLstart(self):
        print("ALL Success")

    def DCIstop(self):
        print("DCI Success")

    def DCVstop(self):
        print("DCV Success")

    def ALLstop(self):
        print("ALL Success")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()