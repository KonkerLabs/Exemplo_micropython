import webrepl
import network
import json

def do_connect():
    WifiConfFile = "wifi.config"
    with open(WifiConfFile, 'r') as f:
        WifiConf = f.read()

    WifiConf = json.loads(WifiConf)
    SSID = WifiConf['ssid']
    PASSWORD = WifiConf['pwd']

    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.active():
        ap_if.active(False)
    if not sta_if.isconnected():
        print('connecting to network {}...'.format(SSID))
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            pass
    print('Network configuration:', sta_if.ifconfig())

do_connect()
webrepl.start()
