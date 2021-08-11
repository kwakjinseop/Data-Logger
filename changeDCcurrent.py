import time
import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# configure the serial connections
import gui2


xlabel = []
ylabel = []

def Currc():
    Currc = ':SENS:FUNC "CURR:DC"\r\n' #기능 변경 구문 8.10현재 기능변경만 가능하고 출력은 안되는 문제있음.
    currentchange = Currc.encode()
    gui2.ser.write(currentchange)

