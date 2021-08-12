import time
import serial

ser = serial.Serial(
    port='COM5',
    baudrate=9600
)
xlabel = []
ylabel = []




while True :
    aaa = ':SENS:DATA?\r\n' #현재 설정되어있는 측정값을 그대로 반한해줌
    fff = aaa.encode()
    ser.write(fff)
    time.sleep(0.5)
    out=''
    stamp = time.time()
    tm = time.localtime(stamp)
    hour = tm.tm_hour
    minute = tm.tm_min
    sec = tm.tm_sec
    string = ""

    while ser.inWaiting() > 0: #ser.inWaiting == 16
        out += ser.read().decode()


    xlabel.append(float(out))
    print(xlabel[len(xlabel)-1])





