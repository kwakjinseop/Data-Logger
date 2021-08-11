##8.9 works: 기본적인 UI 재개편
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import serial
import time

ser = serial.Serial(
    port='COM5',
    baudrate=9600
)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # MainWindow.setEnabled(True)
        MainWindow.resize(1346, 865)
        self.centralwidget = \
            QtWidgets.QWidget(MainWindow)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.gridLayout_2.addWidget(self.pushButton_2, 1, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.groupview = QtWidgets.QVBoxLayout()
        self.groupview.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.groupview.setContentsMargins(-1, -1, 0, -1)
        self.groupview.setSpacing(2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_3)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 31, 72, 141))
        #################여기부터가 <정보> 그룹의 내용들#######################
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.verticalLayout.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.verticalLayout.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget)
        self.verticalLayout.addWidget(self.label_7)
        self.label_34 = QtWidgets.QLabel(self.layoutWidget)
        self.verticalLayout.addWidget(self.label_34)
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox_3)
        self.layoutWidget1.setGeometry(QtCore.QRect(100, 30, 81, 151))
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.verticalLayout_13.addWidget(self.lineEdit_4)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.verticalLayout_13.addWidget(self.lineEdit_5)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.verticalLayout_13.addWidget(self.lineEdit_6)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.verticalLayout_13.addWidget(self.lineEdit_7)
        self.groupview.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.layoutWidget2 = QtWidgets.QWidget(self.groupBox_4)
        self.layoutWidget2.setGeometry(QtCore.QRect(20, 30, 231, 141))
        ###################여기부터 <데이터 로깅 시장> 그룹의 내용들###############################
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.radioButton_14 = QtWidgets.QRadioButton(self.layoutWidget2)
        self.verticalLayout_12.addWidget(self.radioButton_14)
        self.radioButton_15 = QtWidgets.QRadioButton(self.layoutWidget2)
        self.verticalLayout_12.addWidget(self.radioButton_15)
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.layoutWidget2)
        self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())

        self.verticalLayout_12.addWidget(self.dateTimeEdit)
        self.radioButton_16 = QtWidgets.QRadioButton(self.layoutWidget2)
        self.verticalLayout_12.addWidget(self.radioButton_16)
        self.groupview.addWidget(self.groupBox_4)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setEnabled(True)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.layoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 130, 300, 31))
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.spinBox_6 = QtWidgets.QSpinBox(self.layoutWidget_2)

        self.horizontalLayout_6.addWidget(self.spinBox_6)
        self.spinBox_7 = QtWidgets.QSpinBox(self.layoutWidget_2)
        self.horizontalLayout_6.addWidget(self.spinBox_7)
        self.spinBox_8 = QtWidgets.QSpinBox(self.layoutWidget_2)

        self.horizontalLayout_6.addWidget(self.spinBox_8)
        self.spinBox_9 = QtWidgets.QSpinBox(self.layoutWidget_2)

        self.horizontalLayout_6.addWidget(self.spinBox_9)
        self.spinBox_10 = QtWidgets.QSpinBox(self.layoutWidget_2)

        self.horizontalLayout_6.addWidget(self.spinBox_10)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setEnabled(True)
        self.radioButton_2.setGeometry(QtCore.QRect(11, 67, 77, 19))

        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setEnabled(True)
        self.radioButton.setGeometry(QtCore.QRect(11, 41, 57, 19))

        self.label_29 = QtWidgets.QLabel(self.groupBox)
        self.label_29.setGeometry(QtCore.QRect(60, 110, 21, 16))

        self.label_30 = QtWidgets.QLabel(self.groupBox)
        self.label_30.setGeometry(QtCore.QRect(160, 110, 21, 16))

        self.label_31 = QtWidgets.QLabel(self.groupBox)
        self.label_31.setGeometry(QtCore.QRect(10, 110, 21, 16))

        self.label_32 = QtWidgets.QLabel(self.groupBox)
        self.label_32.setGeometry(QtCore.QRect(210, 110, 21, 16))

        self.label_33 = QtWidgets.QLabel(self.groupBox)
        self.label_33.setGeometry(QtCore.QRect(110, 110, 31, 16))

        self.groupview.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)

        self.radioButton_7 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_7.setEnabled(True)
        self.radioButton_7.setGeometry(QtCore.QRect(10, 130, 211, 19))

        self.radioButton_5 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_5.setEnabled(True)
        self.radioButton_5.setGeometry(QtCore.QRect(10, 90, 111, 19))

        self.radioButton_8 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_8.setEnabled(True)
        self.radioButton_8.setGeometry(QtCore.QRect(10, 30, 151, 51))

        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_2.setEnabled(True)
        self.lineEdit_2.setGeometry(QtCore.QRect(210, 130, 81, 21))

        self.layoutWidget3 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget3.setGeometry(QtCore.QRect(140, 80, 195, 45))

        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)

        self.label_15 = QtWidgets.QLabel(self.layoutWidget3)

        self.gridLayout_3.addWidget(self.label_15, 0, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.layoutWidget3)

        self.gridLayout_3.addWidget(self.label_16, 0, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.layoutWidget3)

        self.gridLayout_3.addWidget(self.label_14, 0, 2, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.layoutWidget3)
        self.gridLayout_3.addWidget(self.label_28, 0, 3, 1, 1)
        self.spinBox_18 = QtWidgets.QSpinBox(self.layoutWidget3)
        self.gridLayout_3.addWidget(self.spinBox_18, 1, 0, 1, 1)
        self.spinBox_16 = QtWidgets.QSpinBox(self.layoutWidget3)
        self.gridLayout_3.addWidget(self.spinBox_16, 1, 1, 1, 1)
        self.spinBox_15 = QtWidgets.QSpinBox(self.layoutWidget3)
        self.gridLayout_3.addWidget(self.spinBox_15, 1, 2, 1, 1)
        self.spinBox_17 = QtWidgets.QSpinBox(self.layoutWidget3)
        self.gridLayout_3.addWidget(self.spinBox_17, 1, 3, 1, 1)
        self.groupview.addWidget(self.groupBox_2)
        self.gridLayout.addLayout(self.groupview, 1, 0, 1, 1)
        self.graphview = QtWidgets.QHBoxLayout()
        self.graphview.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        ################### MatPlotlib 들어갈 영역 ########################
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setEnabled(True)
        self.graphview.addWidget(self.tableView)
        self.gridLayout.addLayout(self.graphview, 1, 1, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)

        ########## 메뉴 영역 ###############################
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1346, 26))
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setEnabled(False)
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setEnabled(False)

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)

        MainWindow.setStatusBar(self.statusbar)
        self.actionStart = QtWidgets.QAction(MainWindow) #DCI 부분

        self.actionDCV = QtWidgets.QAction(MainWindow)
        self.actionAll_Start = QtWidgets.QAction(MainWindow)
        self.actionStop = QtWidgets.QAction(MainWindow)

        self.actionDCV_Stop = QtWidgets.QAction(MainWindow)
        self.actionAll_Stop = QtWidgets.QAction(MainWindow)
        self.menu.addAction(self.actionStart) #DCI부분
        self.actionStart.triggered.connect(self.DCIstart)
        self.menu.addAction(self.actionDCV)
        self.actionDCV.triggered.connect(self.DCVstart)
        self.menu.addAction(self.actionAll_Start)
        self.actionAll_Start.triggered.connect(self.ALLstart)
        self.menu_2.addAction(self.actionStop)
        self.actionStop.triggered.connect(self.DCIstop)
        self.menu_2.addAction(self.actionDCV_Stop)
        self.actionDCV_Stop.triggered.connect(self.DCVstop)
        self.menu_2.addAction(self.actionAll_Stop)
        self.actionAll_Stop.triggered.connect(self.ALLstop)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())





        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def DCIstart(self): #일단은 기능전환은 되는 것 확인, 하지만 오류 남아있음
        print("Clicked DCI")
        Currc = ':SENS:FUNC "CURR:DC"\r\n'  # 기능 변경 구문 8.10현재 기능변경만 가능하고 출력은 안되는 문제있음.
        currentchange = Currc.encode()
        ser.write(currentchange)
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


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "Save"))
        self.pushButton.setText(_translate("MainWindow", "Load"))
        self.groupBox_3.setTitle(_translate("MainWindow", "정보"))
        self.label_5.setText(_translate("MainWindow", "이름:"))
        self.label_6.setText(_translate("MainWindow", "포트 번호:"))
        self.label_7.setText(_translate("MainWindow", "Duration:"))
        self.label_34.setText(_translate("MainWindow", "Range:"))
        self.groupBox_4.setTitle(_translate("MainWindow", "데이터 로깅 시작"))
        self.radioButton_14.setText(_translate("MainWindow", "즉시 시작 버튼 사용"))
        self.radioButton_15.setText(_translate("MainWindow", "특정 시간에:"))
        self.radioButton_16.setText(_translate("MainWindow", "외부 트리거 시"))
        self.groupBox.setTitle(_translate("MainWindow", "샘플링 간격"))
        self.radioButton_2.setText(_translate("MainWindow", "Custom"))
        self.radioButton.setText(_translate("MainWindow", "최소"))
        self.label_29.setText(_translate("MainWindow", "HH"))
        self.label_30.setText(_translate("MainWindow", "SS"))
        self.label_31.setText(_translate("MainWindow", "DD"))
        self.label_32.setText(_translate("MainWindow", "MS"))
        self.label_33.setText(_translate("MainWindow", "MM"))
        self.groupBox_2.setTitle(_translate("MainWindow", "데이터 로깅 중지"))
        self.radioButton_7.setText(_translate("MainWindow", "지정한 수의 샘플 수집 후"))
        self.radioButton_5.setText(_translate("MainWindow", "경과 시간 후"))
        self.radioButton_8.setText(_translate("MainWindow", "즉시 중지버튼 사용"))
        self.label_15.setText(_translate("MainWindow", "DD"))
        self.label_16.setText(_translate("MainWindow", "HH"))
        self.label_14.setText(_translate("MainWindow", "MM"))
        self.label_28.setText(_translate("MainWindow", "SS"))
        self.menu.setTitle(_translate("MainWindow", "재생"))
        self.menu_2.setTitle(_translate("MainWindow", "정지"))
        self.actionStart.setText(_translate("MainWindow", "DCI"))
        self.actionStop.setText(_translate("MainWindow", "DCI_Stop"))
        self.actionDCV.setText(_translate("MainWindow", "DCV"))
        self.actionDCV_Stop.setText(_translate("MainWindow", "DCV_Stop"))
        self.actionAll_Stop.setText(_translate("MainWindow", "All_Stop"))
        self.actionAll_Start.setText(_translate("MainWindow", "All_Start"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

