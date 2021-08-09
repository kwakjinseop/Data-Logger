import time
import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# configure the serial connections
ser = serial.Serial(
    port='COM5',
    baudrate=9600
)
xlabel = []
ylabel = []

while True :
    aaa = ':SENS:FUNC "volt:ac"\r\n' #기능 변경 구문
    fff = aaa.encode()
    ser.write(fff)
    #wait one second before reading output.
    time.sleep(1)
    out=''
    out = out.rstrip()
    stamp = time.time()
    tm = time.localtime(stamp)
    hour = tm.tm_hour
    minute = tm.tm_min
    sec = tm.tm_sec
    string=""

    while ser.inWaiting() > 0: #ser.inWaiting == 16
        out += ser.read().decode()
        characters = "'-'"
        for x in range(len(characters)):
            string = out.replace(characters[x],"")
    print(string)
        # print ("%s:%s:%s %s"%(hour, minute, sec, out)) #time.time() == 타임스탬프를 얻는것임 이것을 보기쉽게 변환해야함. tm_sec만 골라 쓸것임.
    #     print(out)
    #     # intout = float(out)
    #     # print(type(intout))
    #     xlabel.append(sec)
    #     ylabel.append(3)
    # # print(xlabel)
    # print(ylabel)
    # plt.plot([xlabel], [ylabel])
    # plt.show()




      # print(out)