import machine
import time
import json
import urequest

led = machine.Pin(4, machine.Pin.OUT)
boardled = machine.Pin(2, machine.Pin.OUT)
boardled.high()

state = 0

def toggle(p):
    p.value(not p.value())

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

def getmsg(channel, oldest=None):
    global device
    resp = ''
    if oldest is None:
        requrl = '{}/sub/{}/{}'.format(device["url"], device["user"], channel)
    else:
        requrl = '{}/sub/{}/{}?offset={}'.format(device["url"],device["user"],channel, oldest)
    try:
        resp = urequest.urlopen(requrl,user=device["user"], passwd=device["pwd"],method="GET")
    except:
        print("Error connecting to {}".format(requrl))
        for i in range(0,2):
            boardled.low()
            time.sleep_ms(100)
            boardled.high()

    return resp

device = readdevicedata()
oldest = 1477873572713

while True:
    resp = getmsg('estado')
    checkdata = resp.split("[{")
    if len(checkdata) == 1:
        header = checkdata[0]
        data = ''
    elif len(checkdata) == 2:
        header, data = checkdata
    else:
        pass  # handle error; there's two #s

    if data:
        data = "[{"+data
        data = json.loads(data)
        for i in data:
            if i['meta']['timestamp']>oldest:
                oldest = i['meta']['timestamp']
                if(i['data'].get('botao')):
                    print("Changing Led State")
                    toggle(led)
                    time.sleep_ms(100)

        time.sleep_ms(500)
