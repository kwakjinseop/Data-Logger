import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5 import uic
import serial, time
import pyqtgraph as pg
from threading import Thread
import sys
import time

## 현재 ui 파일에 mypyqtgraph 위젯을 만들어 놓았기 때문에 컴파일할 경우 해당 선언이 되어있지 않아 오류가 발생한다. 참고!!

form_class = uic.loadUiType("design.ui")[0]

xlabel=[]

ser = serial.Serial(
    port='COM5',
    baudrate=9600
)
Range=""
Target = ""




class Main(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(text='Time(초)', units=None)
        self.enableAutoSIPrefix(False)


    def tickStrings(self, values, scale, spacing):
        """ override 하여, tick 옆에 써지는 문자를 원하는대로 수정함.
            values --> x축 값들   ; 숫자로 이루어진 Itarable data --> ex) List[int]
        """
        # print("--tickStrings valuse ==>", values)
        return [time.strftime("%H:%M:%S", time.localtime(local_time)) for local_time in values]



class MyWindow(QMainWindow, form_class):
    global xlabel, new_time_data
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        ####### 상단 메뉴바 조작 ##########################
        self.menu.setEnabled(False)
        self.menu_2.setEnabled(False)
        self.radioButton_14.clicked.connect(self.menu_able)
        self.radioButton_15.clicked.connect(self.menu_disable)
        self.radioButton_16.clicked.connect(self.menu1_disable)
        self.radioButton_8.clicked.connect(self.stopmenu_able)
        self.radioButton_5.clicked.connect(self.stopmenu_disable)
        self.radioButton_7.clicked.connect(self.stopmenu_disable)
        #########메뉴바 속 세부 메뉴들 조작##########################
        self.radioButton_3.clicked.connect(self.DCVstart)
        self.radioButton_4.clicked.connect(self.DCIstart)

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

        ########## 중지 메뉴부분######################
        self.radioButton_8.clicked.connect(self.instantstop)
        self.radioButton_5.clicked.connect(self.aftertime)
        self.radioButton_7.clicked.connect(self.aftersample)
        self.spinBox_15.valueChanged.connect(self.spinBoxChange1)
        self.spinBox_16.valueChanged.connect(self.spinBoxChange1)
        self.spinBox_17.valueChanged.connect(self.spinBoxChange1)
        self.spinBox_18.valueChanged.connect(self.spinBoxChange1)

        ######### Clear버튼 부분 ############
        self.pushButton_4.clicked.connect(self.clear)



    def clear(self):
        aaa = ':*CLS\r\n'  # 현재 설정되어있는 측정값을 그대로 반한해줌
        fff = aaa.encode()
        ser.write(fff)


    def spinBoxChange1(self):
        ss = self.spinBox_17.value()
        mm = self.spinBox_15.value()
        hh = self.spinBox_16.value()
        dd = self.spinBox_18.value()
        print(ss)
        print(mm)
        print(hh)
        print(dd)




    def instantstop(self):
        self.spinBox_15.setEnabled(False)
        self.spinBox_16.setEnabled(False)
        self.spinBox_17.setEnabled(False)
        self.spinBox_18.setEnabled(False)
        self.lineEdit_2.setEnabled(False)


    def aftertime(self):
        self.lineEdit_2.setEnabled(False)
        self.spinBox_15.setEnabled(True)
        self.spinBox_16.setEnabled(True)
        self.spinBox_17.setEnabled(True)
        self.spinBox_18.setEnabled(True)


    def aftersample(self):
        self.lineEdit_2.setEnabled(True)
        self.spinBox_15.setEnabled(False)
        self.spinBox_16.setEnabled(False)
        self.spinBox_17.setEnabled(False)
        self.spinBox_18.setEnabled(False)




    def spinBoxChange(self):
        MS = self.spinBox_10.value()
        SS = self.spinBox_9.value()
        MM = self.spinBox_8.value()
        HH = self.spinBox_7.value()
        DD = self.spinBox_6.value()
        print(SS)




    def minimumSampling(self):
        self.spinBox_10.setEnabled(False)
        self.spinBox_9.setEnabled(False)
        self.spinBox_8.setEnabled(False)
        self.spinBox_7.setEnabled(False)
        self.spinBox_6.setEnabled(False)



    def customSampling(self):
        self.spinBox_10.setEnabled(True)
        self.spinBox_9.setEnabled(True)
        self.spinBox_8.setEnabled(True)
        self.spinBox_7.setEnabled(True)
        self.spinBox_6.setEnabled(True)




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
        if self.comboBox_3.currentText()=="10mA":
            bbb = ':SENS:CURR:DC:RANG 0.01\r\n'
        elif self.comboBox_3.currentText()=="100mA":
            bbb = ':SENS:CURR:DC:RANG 0.1\r\n'
        elif self.comboBox_3.currentText()=="1A":
            bbb = ':SENS:CURR:DC:RANG 1\r\n'
        elif self.comboBox_3.currentText()=="3A":
            bbb = ':SENS:CURR:DC:RANG 3\r\n'
        else:
            bbb= ':SENS:VOLT:DC:RANG:AUTO ON\r\n'
        kkk = bbb.encode()
        ser.write(kkk)


    def ApplyButton(self):
        self.groupBox_4.setEnabled(False)
        self.groupBox_3.setEnabled(False)
        self.groupBox.setEnabled(False)
        self.groupBox_2.setEnabled(False)#여기까지가 그룹박스들 비활성화
        # system("python mypyqtgraph.py")



    def menu_able(self):
        self.menu.setEnabled(True)
        self.dateTimeEdit.setEnabled(False)

    def menu_disable(self):
        self.menu.setEnabled(False)
        self.dateTimeEdit.setEnabled(True)

    def menu1_disable(self):
        self.dateTimeEdit.setEnabled(False)

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
        self.comboBox_3.setEnabled(True)
        self.comboBox_2.setEnabled(False) #막는다.



    def DCVstart(self):
        global Target
        print("Clicked DCV")
        voltc = ':SENS:FUNC "VOLT:DC"\r\n'  # 기능 변경 구문 8.10현재 기능변경만 가능하고 출력은 안되는 문제있음.
        voltchange = voltc.encode()
        ser.write(voltchange)
        Target="DCV"
        #콤보박스2가 DCV꺼, 콤보박스3이 DCI꺼
        self.comboBox_2.setEnabled(True)
        self.comboBox_3.setEnabled(False)



    def ALLstart(self):
        print("ALL Success")

    def DCIstop(self):
        print("DCI Success")

    def DCVstop(self):
        print("DCV Success")

    def ALLstop(self):
        print("ALL Success")

    def ApplyButton(self):
        self.groupBox_4.setEnabled(False)
        self.groupBox_3.setEnabled(False)
        self.groupBox.setEnabled(False)
        self.groupBox_2.setEnabled(False)
        self.pw = pg.PlotWidget(
            title="Example plot",
            labels={'left': 'y 축'},
            axisItems={'bottom': Main(orientation='bottom')}
        )
        hbox = self.xmcdk
        hbox.addWidget(self.pw)
        self.setLayout(hbox)
        self.pw.setYRange(0, 70, padding=0)
        time_data = int(time.time())
        self.pw.setXRange(time_data - 10, time_data + 1)  # 생략 가능.
        self.pw.showGrid(x=True, y=True)
        # self.pw.enableAutoRange()
        self.pdi = self.pw.plot(pen='y')  # PlotDataItem obj 반환.
        self.plotData = {'x': [], 'y': []}

        self.th = Thread(target=self.update_plot, args=())
        self.th2 = Thread(target=self.collect, args=())
        self.th.start()
        self.th2.start()

    def collect(self):
        global answer,xlabel
        while True:
            aaa = ':SENS:DATA?\r\n'  # 현재 설정되어있는 측정값을 그대로 반한해줌
            fff = aaa.encode()
            ser.write(fff)
            time.sleep(0.5)
            out = ''

            while ser.inWaiting() > 0:  # ser.inWaiting == 16
                out += ser.read().decode()
            xlabel.append(float(out))
            print(xlabel[len(xlabel) - 1])
            new_time_data = int(time.time())
            self.update_plot(new_time_data)



    def update_plot(self, new_time_data: int):
        global xlabel
        self.plotData['y'].append(xlabel[len(xlabel) - 1])
        self.plotData['x'].append(new_time_data)
        # self.pw.setXRange(new_time_data - 10, new_time_data + 1, padding=0)  # 항상 x축 시간을 최근 범위만 보여줌.

        self.pdi.setData(self.plotData['x'], self.plotData['y'])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()