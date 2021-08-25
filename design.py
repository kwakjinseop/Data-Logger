import csv #CSV 읽기/쓰기
import subprocess #프로그램 시작/재시작
from PyQt5.QtCore import QDateTime #시간관련 위젯
from PyQt5.QtWidgets import * # 기본적인 위젯구조
from PyQt5 import uic #ui 파일과의 연결
from serial import Serial # 시리얼 통신
import pyqtgraph as pg # pyqtgraph(그래프)
from threading import Thread # 스레드 구현
import sys # 시스템 접근
import time # 시간관련 라이브러리
from datetime import datetime, timedelta
import datetime
import serial.tools.list_ports # 연결가능한 COM포트 출력
import os # 운영체제 접근

form_class = uic.loadUiType("design.ui")[0]

xlabel = []
ylabel = []

DCVsignal = 0
DCIsignal = 0

DCVxlabel = []
DCIxlabel = []

now = datetime.datetime.now()
nowTime = now.strftime('%H:%M:%S')

new_time_data = 0
limit_time = 0
specifictime = 0
realtime= ""

start_time=""
startsignal = 0

ser = ""

Range = ""
Target = ""

stopvalue = 1

SSeconds = 0
millisecond = 0

minimumsignal = 0
customsignal = 0
timetable=[]
timelabel=[]

plotx=[]
ploty=[]


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
        self.timeEdit.setDateTime(QDateTime.currentDateTime()) #timeEdit속 기본 시간값을 현재시간으로 설정

        ########### 연결도입 부분 #######################
        ports = serial.tools.list_ports.comports() # 연결가능한 포트 번호 출력
        a = [port.name for port in ports]
        if len(a) != 0:
            self.comboBox.addItem(a[0])
        self.pushButton_6.clicked.connect(self.serialconnect)
        self.pushButton_7.clicked.connect(self.disconnectserial)

        self.timeEdit.dateTimeChanged.connect(self.makestarttime)
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
        self.timeEdit_2.setEnabled(False)


        ########## Stop버튼 부분 #############
        self.pushButton_4.setText("Stop")
        self.pushButton_4.clicked.connect(self.stopping)
        # ######### load버튼 부분 #############
        self.pushButton.clicked.connect(self.loadcsv)
        # ######### Save버튼 부분 #############
        self.pushButton_2.clicked.connect(self.writeCsv)

        ####### 설정메뉴 부분 #################
        ports = serial.tools.list_ports.comports()
        a = [port.name for port in ports]
        # self.actionCOM1.setObjectName("actionCOM")
        # self.actionCOM1.setText(a[0])

        ############재시작기능 구현##############
        self.pushButton_5.clicked.connect(self.restartfunction)







    def makestarttime(self):
        global start_time, startsignal
        start_time = self.timeEdit.time().toString()  # dateTimeEdit의 시간 값을 반환해줌
        startsignal= 1



    def serialconnect(self): #Serial 연결부분
        global ser
        ser = serial.Serial(port='COM5', baudrate=9600) #포트번호와 baudrate를 맞춰주어야 함.
        reply = QMessageBox.question(self, 'Message', 'Sucessfully Connected',
                                     QMessageBox.Yes)
        print(serial.Serial)

    def disconnectserial(self):
        global ser
        ser.close() #Serial 연결 종료구문
        reply = QMessageBox.question(self, 'Message', 'Successfully Disconnected',
                                     QMessageBox.Yes)

    def restartfunction(self):
        ser.close()
        self.close()
        subprocess.call("python" + " design.py", shell=True)

    def makelimittime(self):  # 시작 시간 설정부분
        global limit_time, specifictime
        limit_time = self.timeEdit_2.time()  # dateTimeEdit의 시간 값을 반환해줌
        specifictime = 1
        # print(nowTime)
        # print(limit_time.toString())

    def stopping(self):
        global stopvalue
        stopvalue += 1

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

    def spinBoxChange(self):  # 시간제한 설정 부분
        global msecond, second, minute, hour, day, MS, SS, MM, HH, DD, SSeconds, millisecond
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
        minute = timedelta(minutes=MM)
        hour = timedelta(hours=HH)
        day = timedelta(days=DD)

        days_and_time = msecond + second + minute + hour + day
        days = days_and_time.days
        SSeconds = days_and_time.seconds
        millisecond = MS / 1000

        hours = SSeconds // 3600
        minutes = (SSeconds // 60) % 60

        print("days:", days, "hours:", hours, "minutes:", minutes, "milliseconds", millisecond, "second", SSeconds)

    def minimumSampling(self):
        global msecond, minimumsignal, customsignal, SSeconds, millisecond
        self.spinBox_10.setEnabled(False)
        self.spinBox_9.setEnabled(False)
        self.spinBox_8.setEnabled(False)
        self.spinBox_7.setEnabled(False)
        self.spinBox_6.setEnabled(False)
        minimumsignal = 1
        customsignal = 0
        SSeconds = 100 / 1000
        print(SSeconds)

    def customSampling(self):
        global msecond1, customsignal, minimumsignal
        self.spinBox_10.setEnabled(True)
        self.spinBox_9.setEnabled(True)
        self.spinBox_8.setEnabled(True)
        self.spinBox_7.setEnabled(True)
        self.spinBox_6.setEnabled(True)

    def setDCVRange(self):
        if self.comboBox_2.currentText() == "100mV":
            aaa = ':SENS:VOLT:DC:RANG 0.1\r\n'
        elif self.comboBox_2.currentText() == "1V":
            aaa = ':SENS:VOLT:DC:RANG 1\r\n'
        elif self.comboBox_2.currentText() == "10V":
            aaa = ':SENS:VOLT:DC:RANG 10\r\n'
        elif self.comboBox_2.currentText() == "100V":
            aaa = ':SENS:VOLT:DC:RANG 100\r\n'
        elif self.comboBox_2.currentText() == "1000V":
            aaa = ':SENS:VOLT:DC:RANG 1000\r\n'
        else:
            aaa = ':SENS:VOLT:DC:RANG:AUTO ON\r\n'
        fff = aaa.encode()
        ser.write(fff)

    def setDCIRange(self):
        if self.comboBox_3.currentText() == "10mA":
            bbb = ':SENS:CURR:DC:RANG 0.01\r\n'
        elif self.comboBox_3.currentText() == "100mA":
            bbb = ':SENS:CURR:DC:RANG 0.1\r\n'
        elif self.comboBox_3.currentText() == "1A":
            bbb = ':SENS:CURR:DC:RANG 1\r\n'
        elif self.comboBox_3.currentText() == "3A":
            bbb = ':SENS:CURR:DC:RANG 3\r\n'
        else:
            bbb = ':SENS:CURR:DC:RANG:AUTO ON\r\n'
        kkk = bbb.encode()
        ser.write(kkk)

    def menu_able(self):
        self.timeEdit.setEnabled(False)

    def menu_disable(self):  # '특정 시간에' 항목을 선택했을 경우
        self.timeEdit.setEnabled(True)


    def DCIstart(self):
        global Target, DCIsignal, DCVsignal
        DCIsignal = 1
        DCVsignal = 0
        print("Clicked DCI")
        Currc = ':SENS:FUNC "CURR:DC"\r\n'
        currentchange = Currc.encode()
        ser.write(currentchange)  # 여기까지가 기능변경 코드
        Target = "DCI"
        # 콤보박스2가 DCV꺼, 콤보박스3이 DCI꺼
        self.comboBox_3.setEnabled(True)
        self.comboBox_2.setEnabled(False)  # 막는다.

    def DCVstart(self):
        global Target, DCVsignal, DCIsignal
        DCVsignal = 1
        DCIsignal = 0
        print("Clicked DCV")
        voltc = ':SENS:FUNC "VOLT:DC"\r\n'  # 기능 변경 구문 8.10현재 기능변경만 가능하고 출력은 안되는 문제있음.
        voltchange = voltc.encode()
        ser.write(voltchange)
        Target = "DCV"
        # 콤보박스2가 DCV꺼, 콤보박스3이 DCI꺼
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
        print("시간형태", type(time_data)) #형태는 int임.

        self.pw.setXRange(time_data - 10, time_data + 1)  # 생략 가능.
        self.pw.showGrid(x=True, y=True)
        # self.pw.enableAutoRange()
        self.pdi = self.pw.plot(pen='y')  # PlotDataItem obj 반환.

        self.plotData = {'x': [], 'y': []}

        self.th = Thread(target=self.update_plot, args=())
        self.th2 = Thread(target=self.collect, args=())
        # self.th3 = Thread(target=self.csvupdate, args=())
        self.th.start()
        self.th2.start()
        # self.th3.start()


    def collect(self):
        global answer, xlabel, stopvalue, new_time_data, DCVsignal, DCIsignal, customsignal, minimumsignal, SSeconds, start_time, startsignal
        if startsignal == 1: #예정시간이 정해져 있는 경우
            if stopvalue % 2 != 0 and DCVsignal == 1 and DCIsignal == 0:
                now=""
                while now==start_time:
                    now = datetime.datetime.now().strftime('%H:%M:%S')
                    print(now," now")
                    print(start_time," start")
                    if now == start_time:
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
                        # print(DCVxlabel)

                        if stopvalue % 2 == 0:
                            aaa = '*CLS\r\n'
                            ddd = aaa.encode()
                            ser.write(ddd)
                            break

            elif stopvalue % 2 != 0 and DCIsignal == 1 and DCVsignal == 0:
                now=""
                while now==start_time:
                    now = datetime.datetime.now().strftime('%H:%M:%S')
                    print(now)
                    print(start_time)
                    if now == start_time:
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

                        if stopvalue % 2 == 0:
                            aaa = '*CLS\r\n'
                            ddd = aaa.encode()
                            ser.write(ddd)
                            break
        else:
            if stopvalue % 2 != 0 and DCVsignal == 1 and DCIsignal == 0:
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
                    # print(DCVxlabel)

                    if stopvalue % 2 == 0:
                        aaa = '*CLS\r\n'
                        ddd = aaa.encode()
                        ser.write(ddd)
                        break

            elif stopvalue % 2 != 0 and DCIsignal == 1 and DCVsignal == 0:
                while True:
                    aaa = ':SENS:DATA?\r\n'  # 현재 설정되어있는 측정값을 그대로 반한해줌
                    fff = aaa.encode()
                    ser.write(fff)
                    time.sleep(SSeconds)
                    out = ''
                    new_time_data = (time.time()) #여기서 타임스탬프를 정수단위로 끊어줌.
                    # print(type(new_time_data))
                    while ser.inWaiting() > 0:  # ser.inWaiting == 16
                        out += ser.read().decode()
                    DCIxlabel.append(float(out))
                    self.update_plot(new_time_data)

                    if stopvalue % 2 == 0:
                        aaa = '*CLS\r\n'
                        ddd = aaa.encode()
                        ser.write(ddd)
                        break

    def loadcsv(self):
        global DCIxlabel, DCVxlabel, DCVsignal, DCIsignal, timelabel

        if DCIsignal == 1:
            path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')[0]
            f = open(path, 'r')
            rdr = csv.reader(f)
            for line in rdr:
                floatx = float(line[0])
                floaty = float(line[2])
                print("floatx 형", type(floatx))
                timelabel.append(floatx)
                DCIxlabel.append(floaty)





        if DCVsignal == 1:
            path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')[0]
            f = open(path, 'r')
            rdr = csv.reader(f)

            for line in rdr:
                floatx = float(line[0])
                floaty = float(line[2])
                print("가가나다 형",type(line[0]))
                timelabel.append(floatx)
                DCVxlabel.append(floaty)

                print("들어갑니다~~",timelabel)
                print("들어갑니다~~",DCVxlabel)

        self.maker()



    def update_plot(self, new_time_data: float): #new_time_data 수신(timestamp형태로 들어감)
        global xlabel, DCIsignal, DCVsignal, DCVxlabel, DCIxlabel, specifictime, limit_time, stopvalue, timetable, plotx, ploty, realtime
        string = time.localtime(new_time_data)
        realtime = time.strftime('%Y-%m-%d %I:%M:%S:%MS %p', string)
        if specifictime == 1:  # 특정시간이 설정되어 있는 경우
            print("new_time_data입니다.",new_time_data)
            now = datetime.datetime.now().strftime('%H:%M:%S')
            print(now + " Now ")
            print(limit_time.toString())
            if DCVsignal == 1 and DCIsignal == 0:
                self.plotData['y'].append(DCVxlabel[len(DCVxlabel) - 1])
                self.plotData['x'].append(new_time_data)
                timetable.append(new_time_data)

                self.pw.setXRange(new_time_data - 10, new_time_data + 1, padding=0)  # 항상 x축 시간을 최근 범위만 보여줌.
                self.pdi.setData(self.plotData['x'], self.plotData['y'])



            if DCVsignal == 0 and DCIsignal == 1:
                self.plotData['y'].append(DCIxlabel[len(DCIxlabel) - 1])
                self.plotData['x'].append(new_time_data)
                timetable.append(new_time_data)

                self.pw.setXRange(new_time_data - 10, new_time_data + 1, padding=0)  # 항상 x축 시간을 최근 범위만 보여줌.
                self.pdi.setData(self.plotData['x'], self.plotData['y'])

            if now == limit_time.toString():
                stopvalue = 2 * stopvalue
                self.collect()

        if specifictime == 0:  # 특정시간이 설정되어 있지 않은 경우
            tm = time.localtime(new_time_data)
            print("new_time_data입니다.", new_time_data)
            # print("변환한 timestamp입니다.", time.localtime(new_time_data))
            string = time.strftime('%Y-%m-%d %I:%M:%S %p', tm)
            print(string)
            if DCVsignal == 1 and DCIsignal == 0:
                self.plotData['y'].append(DCVxlabel[len(DCVxlabel) - 1])
                self.plotData['x'].append(new_time_data)
                print("실시간y축", self.plotData['y'])
                print("실시간x축", self.plotData['x'])
                plotx = self.plotData['x']
                ploty = self.plotData['y']
                print("원소가 대입되는 부분의 형",type(ploty[0]))
                print("y축", self.plotData['y'])
                print("x축", self.plotData['x'])

                timetable.append(string)

                self.pw.setXRange(new_time_data - 10, new_time_data + 1, padding=0)  # 항상 x축 시간을 최근 범위만 보여줌.
                self.pdi.setData(self.plotData['x'], self.plotData['y'])

            if DCVsignal == 0 and DCIsignal == 1:
                self.plotData['y'].append(DCIxlabel[len(DCIxlabel) - 1])
                self.plotData['x'].append(new_time_data)
                print("실시간y축", self.plotData['y'])
                print("실시간x축", self.plotData['x'])
                timetable.append(new_time_data)
                plotx = self.plotData['x']
                ploty = self.plotData['y']

                self.pw.setXRange(new_time_data - 10, new_time_data + 1, padding=0)  # 항상 x축 시간을 최근 범위만 보여줌.
                self.pdi.setData(self.plotData['x'], self.plotData['y'])


    def maker(self): #xmcdk가 주 레이아웃이름
        global DCVxlabel, DCIxlabel, DCVsignal, DCIsignal, timelabel
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
        self.pdi2 = self.pw.plot(pen='y')  # PlotDataItem obj 반환.
        self.plotData = {'x': [], 'y': []}

        if DCVsignal == 1:
            for i in range (len(DCVxlabel)):
                self.plotData['y'].append(DCVxlabel[i])
                self.plotData['x'].append(timelabel[i])
            print("y축", self.plotData['y'])
            print("x축", self.plotData['x'])
            self.pdi2.setData(self.plotData['x'], self.plotData['y'])

        if DCIsignal == 1:
            for i in range(len(DCIxlabel)):
                self.plotData['y'].append(DCIxlabel[i])
                self.plotData['x'].append(timelabel[i])
            print("y축", self.plotData['y'])
            print("x축", self.plotData['x'])
            self.pdi2.setData(self.plotData['x'], self.plotData['y'])


    def writeCsv(self):
        global DCVsignal, DCIsignal, DCVxlabel, DCIxlabel, timetable, plotx, ploty, realtime
        path = QFileDialog.getSaveFileName(self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')

        print("저장될 plotx",plotx)
        print("저장될 ploty",ploty)
        if DCVsignal == 1:
            if path[0] != '':
                with open(path[0], 'w', newline="") as csv_file:
                    writer = csv.writer(csv_file, dialect='excel')
                    for i in range(len(plotx)):
                        writer.writerow([plotx[i]]+[realtime]+[ploty[i]])

        if DCIsignal == 1:
            if path[0] != '':
                with open(path[0], 'w', newline="") as csv_file:
                    writer = csv.writer(csv_file, dialect='excel')
                    for i in range(len(plotx)):
                        writer.writerow([plotx[i]] +[realtime]+[ploty[i]])




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()