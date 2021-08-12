import serial
import time
from design import ser


while True:
    aaa = ':SENS:CURR:AC:NPLC? MAX\r\n'  # 현재 설정되어있는 측정값을 그대로 반한해줌
    fff = aaa.encode()
    ser.write(fff)
    out = ''
    stamp = time.time()
    tm = time.localtime(stamp)
    hour = tm.tm_hour
    minute = tm.tm_min
    sec = tm.tm_sec
    string = ""

    while ser.inWaiting() > 0:  # ser.inWaiting == 16
        out += ser.read().decode()
    print(out)

