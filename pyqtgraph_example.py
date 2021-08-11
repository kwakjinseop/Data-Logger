from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *

import pyqtgraph as pg

import time


class TimeAxisItem(pg.AxisItem):
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


class ExampleWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.pw = pg.PlotWidget(
            title="Example plot",
            labels={'left': 'y 축'},
            axisItems={'bottom': TimeAxisItem(orientation='bottom')}
        )

        hbox = QHBoxLayout()
        hbox.addWidget(self.pw)
        self.setLayout(hbox)

        self.pw.setYRange(0, 70, padding=0)

        time_data = int(time.time())
        self.pw.setXRange(time_data - 10, time_data + 1)  # 생략 가능.

        self.pw.showGrid(x=True, y=True)
        # self.pw.enableAutoRange()

        self.pdi = self.pw.plot(pen='y')   # PlotDataItem obj 반환.

        self.plotData = {'x': [], 'y': []}

    def update_plot(self, new_time_data: int):
        data_sec = time.strftime("%S", time.localtime(new_time_data))

        ####이 쪽이 실질적으로 데이터가 들어가는 부분#####
        self.plotData['y'].append(int(data_sec))
        self.plotData['x'].append(new_time_data)

        self.pw.setXRange(new_time_data - 10, new_time_data + 1, padding=0)   # 항상 x축 시간을 최근 범위만 보여줌.

        self.pdi.setData(self.plotData['x'], self.plotData['y'])


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    ex = ExampleWidget()

    def get_data():
        new_time_data = int(time.time())
        ex.update_plot(new_time_data)

    mytimer = QTimer()
    mytimer.start(1000)  # 1초마다 갱신 위함...
    mytimer.timeout.connect(get_data)

    ex.show()
    sys.exit(app.exec_())