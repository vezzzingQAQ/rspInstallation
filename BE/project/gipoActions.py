import random
import time
from adafruit_servokit import ServoKit
import settings
import RPi.GPIO as GPIO
import pcf as ADC
import math


class VG():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        for light_pin in settings.SetObj.LIGHT_PIN:
            GPIO.setup(light_pin, GPIO.OUT)
        for light_pin in settings.SetObj.LIGHT_PIN:
            GPIO.output(light_pin, GPIO.HIGH)
            time.sleep(0.1)

    def setMode1(self):
        # 运转模式1
        def setRandom():
            kit = ServoKit(channels=16)
            kit.servo[random.randint(0, 9)].angle = random.randint(70, 110)
        # 舵机
        for i in range(9):
            kit = ServoKit(channels=16)
            kit.servo[i].angle = 0
            time.sleep(0.2)
        for i in range(9):
            kit = ServoKit(channels=16)
            kit.servo[i].angle = 90
            time.sleep(0.2)
        # 灯
        for light_pin in settings.SetObj.LIGHT_PIN:
            GPIO.output(light_pin, GPIO.LOW)
            time.sleep(0.1)
        time.sleep(2)
        # 参拜
        sleepTime = 1
        angleLeft = 85
        angleRight = 120
        kit = ServoKit(channels=16)
        for i in range(6):
            for c_angle in range((angleRight-angleLeft)*2):
                if c_angle < angleRight-angleLeft:
                    kit.servo[9].angle = angleLeft+c_angle
                else:
                    kit.servo[9].angle = angleRight - \
                        (c_angle-(angleRight-angleLeft))
                setRandom()
                time.sleep(sleepTime/((angleRight-angleLeft)*2))
            # time.sleep(0.5)
        # 灯
        for light_pin in settings.SetObj.LIGHT_PIN:
            GPIO.output(light_pin, GPIO.HIGH)
            time.sleep(0.1)
        print("setMode1")

    def setMode2(self):
        # 参拜
        sleepTime = 1
        angleLeft = 85
        angleRight = 120
        kit = ServoKit(channels=16)
        for i in range(9):
            for c_angle in range((angleRight-angleLeft)*2):
                if c_angle < angleRight-angleLeft:
                    kit.servo[9].angle = angleLeft+c_angle
                else:
                    kit.servo[9].angle = angleRight - \
                        (c_angle-(angleRight-angleLeft))
                time.sleep(sleepTime/((angleRight-angleLeft)*2))
                kit.servo[i].angle = math.sin(i/4+c_angle*2)*90+90
            time.sleep(0.5)
        print("setMode2")

    def setMode3(self):
        for i in range(9):
            kit = ServoKit(channels=16)
            kit.servo[i].angle = 0
            time.sleep(0.2)
        # 灯
        for light_pin in settings.SetObj.LIGHT_PIN:
            GPIO.output(light_pin, GPIO.LOW)
            time.sleep(0.1)
        # 参拜
        sleepTime = 1
        angleLeft = 85
        angleRight = 120
        kit = ServoKit(channels=16)
        for i in range(9):
            for c_angle in range((angleRight-angleLeft)*2):
                if c_angle < angleRight-angleLeft:
                    kit.servo[9].angle = angleLeft+c_angle
                else:
                    kit.servo[9].angle = angleRight - \
                        (c_angle-(angleRight-angleLeft))
                time.sleep(sleepTime/((angleRight-angleLeft)*2))
                kit.servo[i].angle = c_angle*2
            time.sleep(0.5)
        for i in range(9):
            kit = ServoKit(channels=16)
            kit.servo[i].angle = 0
            time.sleep(0.2)
        # 灯
        for light_pin in settings.SetObj.LIGHT_PIN:
            GPIO.output(light_pin, GPIO.HIGH)
            time.sleep(0.1)
        print("setMode2")

    def setMode4(self):
        for i in range(9):
            kit = ServoKit(channels=16)
            kit.servo[i].angle = 0
            time.sleep(0.2)
        # 灯
        for light_pin in settings.SetObj.LIGHT_PIN:
            GPIO.output(light_pin, GPIO.LOW)
            time.sleep(0.1)
        # 参拜
        sleepTime = 1
        angleLeft = 85
        angleRight = 120
        kit = ServoKit(channels=16)
        for i in range(9):
            for c_angle in range((angleRight-angleLeft)*2):
                if c_angle < angleRight-angleLeft:
                    kit.servo[9].angle = angleLeft+c_angle
                else:
                    kit.servo[9].angle = angleRight - \
                        (c_angle-(angleRight-angleLeft))
                time.sleep(sleepTime/((angleRight-angleLeft)*2))
            time.sleep(0.5)
            for i in range(9):
                kit = ServoKit(channels=16)
                kit.servo[i].angle = random.randint(0, 180)
        for i in range(9):
            kit = ServoKit(channels=16)
            kit.servo[i].angle = 0
            time.sleep(0.2)
        # 灯
        for light_pin in settings.SetObj.LIGHT_PIN:
            GPIO.output(light_pin, GPIO.HIGH)
            time.sleep(0.1)
        print("setMode2")

    def customAction(self, settings_obj):
        # 根据指定的动作驱动舵机
        def find_act_by_order(current_list, order):
            # 根据order返回setting对象【order:1-16】
            for setting in current_list:
                if int(setting["order"]) == int(order):
                    print(setting, order)
                    return setting
            return False
        for i in range(10):
            # 驱动舵机
            current_act_pin = find_act_by_order(settings_obj, i+1)
            if not current_act_pin:
                return
            time.sleep(float(current_act_pin["delay"]))
            kit = ServoKit(channels=16)
            kit.servo[int(current_act_pin["node"]) -
                      1].angle = float(current_act_pin["power"])
            time.sleep(float(current_act_pin["duration"]))
        for i in range(10, 15):
            # 驱动灯光
            current_act_pin = find_act_by_order(settings_obj, i+1)
            if not current_act_pin:
                return
            time.sleep(float(current_act_pin["delay"]))
            current_power = float(current_act_pin["power"])
            if current_power > 90:
                GPIO.output(settings.SetObj.LIGHT_PIN[int(
                    current_act_pin["node"])-1-9], GPIO.LOW)
            else:
                GPIO.output(settings.SetObj.LIGHT_PIN[int(
                    current_act_pin["node"])-1-9], GPIO.HIGH)
            time.sleep(float(current_act_pin["duration"]))

    def stop(self):
        # 停止所有动作
        # 舵机回0度
        for i in range(9):
            kit = ServoKit(channels=16)
            kit.servo[i].angle = 0
            time.sleep(0.2)
        # 灯光关闭
        for light_pin in settings.SetObj.LIGHT_PIN:
            GPIO.output(light_pin, GPIO.HIGH)
            time.sleep(0.1)

        print("stop")

    def sensorEnable(self, id):
        # 启动传感器
        print("startSensor")
        # 返回传感器数据
        if int(id) == 1:
            # 超声波传感器
            trig_pin = 27
            echo_pin = 17
            GPIO.setup(trig_pin, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(echo_pin, GPIO.IN)

            def checkdist():
                GPIO.output(trig_pin, GPIO.HIGH)
                time.sleep(0.000015)
                GPIO.output(trig_pin, GPIO.LOW)
                while not GPIO.input(echo_pin):
                    pass
                t1 = time.time()
                while GPIO.input(echo_pin):
                    pass
                t2 = time.time()
                return (t2-t1)*340/2
            return checkdist()
        # else:
        #     i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15), freq=400000)
        #     I2C_ADDR = i2c.scan()[0]
        #     print("I2C addr: ", I2C_ADDR)
        #     cpcf = pcf.PCF8591(i2c, I2C_ADDR)

        #     while True:
        #         light = cpcf.read(0)
        #         temp = cpcf.read(1)
        #         volt = cpcf.read(3)

        #         print("light: {:d} temperature: {:d} volt: {:d}".format(light, temp, volt))
        #         time.sleep(2)

    def sensorDisable(self, id):
        # 停止传感器
        print("stopSensor")
