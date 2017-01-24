import machine
import time
import json
import urequest

button = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
boardled = machine.Pin(2, machine.Pin.OUT)
boardled.high()
state = 0

class ApiError(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

def readdevicedata():
    deviceName = "device.config"
    with open(deviceName, 'r') as f:
        device = json.load(f)
    return device

def postmsg(channel, message):
    global device
    resp=''
    requrl = '{}/pub/{}/{}'.format(device["url"],device["user"],channel)
    try:
        resp = urequest.urlopen(requrl,user=device["user"], passwd=device["pwd"], data=json.dumps(message),method="POST")
    except:
        print ("Error connecting to {}".format(requrl))
        for i in range(0,2):
            boardled.low()
            time.sleep_ms(100)
            boardled.high()

    return resp

device = readdevicedata()

while True:
    state = button.value()
    if state:
        postmsg('estado', {"botao": 1})
        print(state)
    time.sleep(0.2)
