import time
import serial

# configure the serial connections
ser = serial.Serial(
    port='COM5',
    baudrate=9600
)
xlabel = []
ylabel = []

aaa = '*rst\r\n' #기능 변경 구문 8.10현재 기능변경만 가능하고 출력은 안되는 문제있음.
fff = aaa.encode()
ser.write(fff)
