import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import serial, time
from os import system



form_class = uic.loadUiType("design.ui")[0]

ser = serial.Serial(
    port='COM5',
    baudrate=9600
)
Range=""
Target = ""


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        ####### 상단 메뉴바 조작 ##########################
        self.menu.setEnabled(False)
        self.menu_2.setEnabled(False)
        self.radioButton_14.clicked.connect(self.menu_able)
        self.radioButton_15.clicked.connect(self.menu_disable)
        self.radioButton_16.clicked.connect(self.menu_disable)
        self.radioButton_8.clicked.connect(self.stopmenu_able)
        self.radioButton_5.clicked.connect(self.stopmenu_disable)
        self.radioButton_7.clicked.connect(self.stopmenu_disable)
        #########메뉴바 속 세부 메뉴들 조작##########################
        self.radioButton_3.clicked.connect(self.DCVstart)
        self.radioButton_4.clicked.connect(self.DCIstart)

        # self.actionAll_Start.triggered.connect(self.ALLstart)
        # self.actionStop.triggered.connect(self.DCIstop)
        # self.actionDCV_Stop.triggered.connect(self.DCVstop)
        # self.actionAll_Stop.triggered.connect(self.ALLstop)
        #########샘플링 간격 부분##################
        self.radioButton.clicked.connect(self.minimumSampling)
        self.radioButton_2.clicked.connect(self.customSampling)

        ############## Apply 버튼을 눌렀을 때 나머지 그룹들 비활성화 ###############
        self.pushButton_3.clicked.connect(self.ApplyButton)

        ############ Range버튼 구현###############3
        self.comboBox_2.currentTextChanged.connect(self.setDCVRange)
        self.comboBox_3.currentTextChanged.connect(self.setDCIRange)

        #########Spin Box 값 반환부분#################
        self.spinBox_10.valueChanged.connect(self.spinBoxChange)
        self.spinBox_9.valueChanged.connect(self.spinBoxChange)
        self.spinBox_8.valueChanged.connect(self.spinBoxChange)
        self.spinBox_7.valueChanged.connect(self.spinBoxChange)
        self.spinBox_6.valueChanged.connect(self.spinBoxChange)


    def spinBoxChange(self):
        spin10 = self.spinBox_10.value
        print(spin10)




    def minimumSampling(self):
        self.radioButton_2.setEnabled(False)



    def customSampling(self):
        self.radioButton.setEnabled(False)

    def setDCVRange(self):
        if self.comboBox_2.currentText()=="100mV":
            aaa = ':SENS:VOLT:DC:RANG 0.1\r\n'
        elif self.comboBox_2.currentText()=="1V":
            aaa = ':SENS:VOLT:DC:RANG 1\r\n'
        elif self.comboBox_2.currentText()=="10V":
            aaa = ':SENS:VOLT:DC:RANG 10\r\n'
        elif self.comboBox_2.currentText()=="100V":
            aaa = ':SENS:VOLT:DC:RANG 100\r\n'
        elif self.comboBox_2.currentText()=="1000V":
            aaa = ':SENS:VOLT:DC:RANG 1000\r\n'
        else:
            aaa = ':SENS:VOLT:DC:RANG:AUTO ON\r\n'
        fff = aaa.encode()
        ser.write(fff)

    def setDCIRange(self):
        if self.comboBox_2.currentText()=="100mA":
            aaa = ':SENS:VOLT:DC:RANG 0.1\r\n'
        elif self.comboBox_2.currentText()=="1A":
            aaa = ':SENS:VOLT:DC:RANG 1\r\n'
        elif self.comboBox_2.currentText()=="10A":
            aaa = ':SENS:VOLT:DC:RANG 10\r\n'
        elif self.comboBox_2.currentText()=="100A":
            aaa = ':SENS:VOLT:DC:RANG 100\r\n'
        elif self.comboBox_2.currentText()=="1000A":
            aaa = ':SENS:VOLT:DC:RANG 1000\r\n'
        else:
            aaa = ':SENS:VOLT:DC:RANG:AUTO ON\r\n'
        fff = aaa.encode()
        ser.write(fff)


    def ApplyButton(self):
        self.groupBox_4.setEnabled(False)
        self.groupBox_3.setEnabled(False)
        self.groupBox.setEnabled(False)
        self.groupBox_2.setEnabled(False)#여기까지가 그룹박스들 비활성화
        # system("python pyqtgraph.py")



    def menu_able(self):
        self.menu.setEnabled(True)

    def menu_disable(self):
        self.menu.setEnabled(False)

    def stopmenu_able(self):
        self.menu_2.setEnabled(True)

    def stopmenu_disable(self):
        self.menu_2.setEnabled(False)





    def DCIstart(self): #일단은 기능전환은 되는 것 확인, 하지만 오류 남아있음
        global Target
        print("Clicked DCI")
        Currc = ':SENS:FUNC "CURR:DC"\r\n'
        currentchange = Currc.encode()
        ser.write(currentchange) #여기까지가 기능변경 코드
        Target = "DCI"
        #콤보박스2가 DCV꺼, 콤보박스3이 DCI꺼
        if not self.comboBox_3.setEnabled:
            self.comboBox_3.setEnabled
        self.comboBox_2.setEnabled(False) #막는다.



    def DCVstart(self):
        global Target
        print("Clicked DCV")
        voltc = ':SENS:FUNC "VOLT:DC"\r\n'  # 기능 변경 구문 8.10현재 기능변경만 가능하고 출력은 안되는 문제있음.
        voltchange = voltc.encode()
        ser.write(voltchange)
        #콤보박스2가 DCV꺼, 콤보박스3이 DCI꺼
        if not self.comboBox_2.setEnabled:
            self.comboBox_2.setEnabled
        self.comboBox_3.setEnabled(False)



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