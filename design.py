import csv
import subprocess
import sys
from PyQt5.QtCore import QTimer, QDateTime, QProcess
from PyQt5.QtWidgets import *
from PyQt5 import uic
import serial, time
import pyqtgraph as pg
from threading import Thread
import sys
import time
import pandas as pd
from pandas import DataFrame
from datetime import datetime, timedelta
import datetime
import serial.tools.list_ports
import os



form_class = uic.loadUiType("design.ui")[0]

xlabel = []
ylabel = []

DCVsignal=0
DCIsignal=0

DCVxlabel=[]
DCIxlabel=[]

now = datetime.datetime.now()
nowTime = now.strftime('%H:%M:%S')


new_time_data = 0
limit_time = 0
specifictime = 0


ser = serial.Serial(
    port='COM5',
    baudrate=9600
)

Range=""
Target = ""

stopvalue = 1

SSeconds = 0
millisecond = 0




minimumsignal = 0
customsignal = 0



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
    global xlabel, new_time_data, DCVsignal, DCIsignal, DCVxlabel, DCIxlabel, limit_time
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        ####### 상단 메뉴바 조작 ##########################
        self.timeEdit.setEnabled(False)
        self.radioButton_14.clicked.connect(self.menu_able)
        self.radioButton_15.clicked.connect(self.menu_disable)
        self.radioButton_16.clicked.connect(self.menu1_disable)
        self.timeEdit.setDateTime(QDateTime.currentDateTime())
        # self.timeEdit.dateTimeChanged.connect(self.makelimittime)
        #########메뉴바 속 세부 메뉴들 조작##########################
        self.radioButton_3.clicked.connect(self.DCVstart)
        self.radioButton_4.clicked.connect(self.DCIstart)

        #########샘플링 간격 부분##################
        self.radioButton.clicked.connect(self.minimumSampling)

        self.radioButton_2.clicked.connect(self.customSampling)
        self.spinBox_10.setEnabled(False)
        self.spinBox_9.setEnabled(False)
        self.spinBox_8.setEnabled(False)
        self.spinBox_7.setEnabled(False)
        self.spinBox_6.setEnabled(False)



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
        self.timeEdit_2.setDateTime(QDateTime.currentDateTime())
        self.timeEdit_2.dateTimeChanged.connect(self.makelimittime)
        self.radioButton_7.clicked.connect(self.aftersample)
        self.timeEdit_2.setEnabled(False)
        self.lineEdit_2.setEnabled(False)


        # ######### Stop버튼 부분 #############
        self.pushButton_4.setText("Stop")
        self.pushButton_4.clicked.connect(self.stopping)
        # ######### load버튼 부분 #############
        # self.pushButton.clicked.connect(self.loadcsv)
        # ######### Save버튼 부분 #############
        self.pushButton_2.clicked.connect(self.savecsv)

        ####### 설정메뉴 부분 #################3
        ports = serial.tools.list_ports.comports()
        a = [port.name for port in ports]
        self.actionCOM1.setObjectName("actionCOM")
        self.actionCOM1.setText(a[0])
        # self.actionCOM1.clicked.connect(self.actioncom1)

        ############재시작기능 구현##############
        self.pushButton_5.clicked.connect(self.restartfunction)

    def restartfunction(self):
        ser.close()
        self.close()
        subprocess.call("python" + " design.py", shell=True)


    def makelimittime(self):
        global limit_time, specifictime
        limit_time = self.timeEdit_2.time() #dateTimeEdit의 시간 값을 반환해줌
        specifictime = 1
        # print(nowTime)
        # print(limit_time.toString())



    def stopping(self):
        global stopvalue
        stopvalue +=1



    def instantstop(self):
        self.timeEdit_2.setEnabled(False)
        self.lineEdit_2.setEnabled(False)




    def aftertime(self):
        global limit_time, specifictime
        self.timeEdit_2.setEnabled(True)
        limit_time = self.timeEdit_2.time()  # dateTimeEdit의 시간 값을 반환해줌
        specifictime = 1
        # print(nowTime)
        # print(limit_time.toString())
        self.lineEdit_2.setEnabled(False)



    def aftersample(self):
        self.lineEdit_2.setEnabled(True)
        self.timeEdit_2.setEnabled(False)




    def spinBoxChange(self):
        global msecond, second, minute, hour, day ,MS, SS, MM, HH, DD, SSeconds, millisecond
        if self.spinBox_10.valueChanged:
            MS = self.spinBox_10.value()
            # print(MS)
        if self.spinBox_9.valueChanged:
            SS = self.spinBox_9.value()
            # print(SS)
        if self.spinBox_8.valueChanged:
            MM = self.spinBox_8.value()
            # print(MM)
        if self.spinBox_7.valueChanged:
            HH = self.spinBox_7.value()
            # print(HH)
        if self.spinBox_6.valueChanged:
            DD = self.spinBox_6.value()
            # print(DD)

        msecond = timedelta(milliseconds=MS)
        second = timedelta(seconds=SS)
        minute =timedelta(minutes=MM)
        hour = timedelta(hours=HH)
        day = timedelta(days = DD)

        days_and_time = msecond + second + minute + hour + day
        days = days_and_time.days
        SSeconds = days_and_time.seconds
        millisecond = MS/1000

        hours = SSeconds//3600
        minutes = (SSeconds//60)%60

        print("days:", days, "hours:", hours, "minutes:", minutes, "milliseconds", millisecond, "second",SSeconds)


    def minimumSampling(self):
        global msecond, minimumsignal, customsignal,SSeconds, millisecond
        self.spinBox_10.setEnabled(False)
        self.spinBox_9.setEnabled(False)
        self.spinBox_8.setEnabled(False)
        self.spinBox_7.setEnabled(False)
        self.spinBox_6.setEnabled(False)
        minimumsignal = 1
        customsignal = 0
        SSeconds = 100/1000
        print(SSeconds)




    def customSampling(self):
        global msecond1, customsignal, minimumsignal
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
            bbb= ':SENS:CURR:DC:RANG:AUTO ON\r\n'
        kkk = bbb.encode()
        ser.write(kkk)


    def menu_able(self):
        self.timeEdit.setEnabled(False)

    def menu_disable(self): #'특정 시간에' 항목을 선택했을 경우
        self.timeEdit.setEnabled(True)


    def menu1_disable(self):
        self.timeEdit.setEnabled(False)




    def DCIstart(self): #일단은 기능전환은 되는 것 확인, 하지만 오류 남아있음
        global Target, DCIsignal, DCVsignal
        DCIsignal=1
        DCVsignal=0
        print("Clicked DCI")
        Currc = ':SENS:FUNC "CURR:DC"\r\n'
        currentchange = Currc.encode()
        ser.write(currentchange) #여기까지가 기능변경 코드
        Target = "DCI"
        #콤보박스2가 DCV꺼, 콤보박스3이 DCI꺼
        self.comboBox_3.setEnabled(True)
        self.comboBox_2.setEnabled(False) #막는다.



    def DCVstart(self):
        global Target, DCVsignal, DCIsignal
        DCVsignal=1
        DCIsignal=0
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
        global answer,xlabel, stopvalue, new_time_data, DCVsignal, DCIsignal, customsignal, minimumsignal, SSeconds

        if stopvalue%2 != 0 and DCVsignal==1 and DCIsignal==0:
            while True:
                aaa = ':SENS:DATA?\r\n'  # 현재 설정되어있는 측정값을 그대로 반한해줌
                fff = aaa.encode()
                ser.write(fff)
                time.sleep(SSeconds)
                out = ''
                new_time_data = int(time.time())
                # print(new_time_data)
                while ser.inWaiting() > 0:  # ser.inWaiting == 16
                    out += ser.read().decode()
                DCVxlabel.append(float(out))
                self.update_plot(new_time_data)
                print(DCVxlabel)

                if stopvalue%2 == 0:
                    aaa = '*CLS\r\n'
                    ddd = aaa.encode()
                    ser.write(ddd)
                    break

        elif stopvalue % 2 != 0 and DCIsignal==1 and DCVsignal==0:
            while True:
                aaa = ':SENS:DATA?\r\n'  # 현재 설정되어있는 측정값을 그대로 반한해줌
                fff = aaa.encode()
                ser.write(fff)
                time.sleep(SSeconds)
                out = ''
                new_time_data = int(time.time())
                # print(new_time_data)
                while ser.inWaiting() > 0:  # ser.inWaiting == 16
                    out += ser.read().decode()
                DCIxlabel.append(float(out))
                self.update_plot(new_time_data)

                if stopvalue%2 == 0:
                    aaa = '*CLS\r\n'
                    ddd = aaa.encode()
                    ser.write(ddd)
                    break


    def update_plot(self, new_time_data: int):
        global xlabel, DCIsignal, DCVsignal, DCVxlabel, DCIxlabel, specifictime, limit_time, stopvalue

        if specifictime == 1: #특정시간이 설정되어 있는 경우
            print(new_time_data)
            now = datetime.datetime.now().strftime('%H:%M:%S')
            print(now+ " Now ")
            print(limit_time.toString())
            if DCVsignal == 1 and DCIsignal == 0:
                self.plotData['y'].append(DCVxlabel[len(DCVxlabel) - 1])
                self.plotData['x'].append(new_time_data)
                self.pw.setXRange(new_time_data - 10, new_time_data + 1, padding=0)  # 항상 x축 시간을 최근 범위만 보여줌.
                self.pdi.setData(self.plotData['x'], self.plotData['y'])

            if DCVsignal == 0 and DCIsignal == 1:
                self.plotData['y'].append(DCIxlabel[len(DCIxlabel) - 1])
                self.plotData['x'].append(new_time_data)
                self.pw.setXRange(new_time_data - 10, new_time_data + 1, padding=0)  # 항상 x축 시간을 최근 범위만 보여줌.
                self.pdi.setData(self.plotData['x'], self.plotData['y'])

            if now == limit_time.toString():
                stopvalue = 2*stopvalue
                self.collect()

        if specifictime == 0: #특정시간이 설정되어 있지 않은 경우
            if DCVsignal == 1 and DCIsignal == 0:
                self.plotData['y'].append(DCVxlabel[len(DCVxlabel) - 1])
                self.plotData['x'].append(new_time_data)
                self.pw.setXRange(new_time_data - 10, new_time_data + 1, padding=0)  # 항상 x축 시간을 최근 범위만 보여줌.
                self.pdi.setData(self.plotData['x'], self.plotData['y'])

            if DCVsignal == 0 and DCIsignal == 1:
                self.plotData['y'].append(DCIxlabel[len(DCIxlabel) - 1])
                self.plotData['x'].append(new_time_data)
                self.pw.setXRange(new_time_data - 10, new_time_data + 1, padding=0)  # 항상 x축 시간을 최근 범위만 보여줌.
                self.pdi.setData(self.plotData['x'], self.plotData['y'])

    def savecsv(self): #저장되는 부분:
        global new_time_data,DCVsignal, DCIsignal
        if DCVsignal == 1:
            timedata=[]
            data = {'DCV':DCVxlabel}
            data_df = DataFrame(data, index=timedata.append(new_time_data))
            data_df.to_csv(self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)', sep=',', na_rep='NaN')
        elif DCIsignal == 1:
            timedata = []
            data = {'DCI': DCIxlabel}
            data_df = DataFrame(data, index=timedata.append(new_time_data))
            data_df.to_csv('C:\\Users\\Geoplan\\Desktop\\곽진섭_인턴\\Keithley_Datalogger\\dcinew.csv', sep=',',
                           na_rep='NaN')


    def writeCsv(self):
        global new_time_data, DCVsignal, DCIsignal
        path = QFileDialog.getSaveFileName(self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], 'w') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                timedata = []
                data = {'DCV': DCVxlabel}
                data_df = DataFrame(data, index=timedata.append(new_time_data))
                for row in range(self.tableWidget_2.rowCount()): #len(data_df)
                    row_data = []
                    for column in range(self.tableWidget_2.columnCount()):
                        item = self.tableWidget_2.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                    writer.writerow(row_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()