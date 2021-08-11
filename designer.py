import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import serial, time
import matplotlib_prices
import Rangesetup


Range=""

form_class = uic.loadUiType("design.ui")[0]

ser = serial.Serial(
    port='COM5',
    baudrate=9600
)


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        global Range
        super().__init__()
        self.setupUi(self)
        #############DCI인지 DCV인지 라디오 버튼으로 조작##############
        self.radioButton_3.clicked.connect(self.DCVstart)
        self.radioButton_4.clicked.connect(self.DCIstart)
        ####### 상단 메뉴바 조작##########################
        self.menu.setEnabled(False)
        self.menu_2.setEnabled(False)
        self.radioButton_14.clicked.connect(self.menu_able)
        self.radioButton_15.clicked.connect(self.menu_disable)
        self.radioButton_16.clicked.connect(self.menu_disable2)
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
        #########Range 콤보박스 부분##################
        self.comboBox_2.currentTextChanged.connect(self.combosubject)


        ##########Apply버튼이 눌렸을 경우#################
        self.pushButton_3.clicked.connect(self.settingfinish)

    def combosubject(self):
        global Range, ser
        if(self.comboBox_2.currentText() == "100mA"):
             Range= "100mA"
             Range = ':SENS:VOLT:DC:RANG 0.1\r\n'
        elif(self.comboBox_2.currentText() == "1V"):
             Range= "1V"
             Range = ':SENS:VOLT:DC:RANG 1\r\n'
        elif(self.comboBox_2.currentText() == "10V"):
             Range= "10V"
             Range = ':SENS:VOLT:DC:RANG 10\r\n'
        elif(self.comboBox_2.currentText() == "100V"):
             Range= "100V"
             Range = ':SENS:VOLT:DC:RANG 100\r\n'
        elif(self.comboBox_2.currentText() == "1000V"):
             Range= "1000V"
             Range = ':SENS:VOLT:DC:RANG 1000\r\n'
        elif(self.comboBox_2.currentText() == "Auto"):
             Range= "Auto"
             Range = ':SENS:VOLT:DC:RANG:AUTO?\r\n'
        fff = Range.encode()
        ser.write(fff)



    def settingfinish(self):
        self.groupBox_4.setEnabled(False)
        self.groupBox_3.setEnabled(False)


    def menu_able(self):
        self.menu.setEnabled(True)
        self.dateTimeEdit.setEnabled(False)

    def menu_disable(self):
        self.menu.setEnabled(False)
        self.dateTimeEdit.setEnabled(True)

    def menu_disable2(self):
        self.menu.setEnabled(False)
        self.dateTimeEdit.setEnabled(False)

    def stopmenu_able(self):
        self.menu_2.setEnabled(True)

    def stopmenu_disable(self):
        self.menu_2.setEnabled(False)



    def DCIstart(self): #일단은 기능전환은 되는 것 확인, 하지만 오류 남아있음
        print("Clicked DCI")
        Currc = ':SENS:FUNC "CURR:DC"\r\n'  # 기능 변경 구문 8.10현재 기능변경만 가능하고 출력은 안되는 문제있음.
        currentchange = Currc.encode()
        ser.write(currentchange)
        self.graphview.addWidget(matplotlib_prices)



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