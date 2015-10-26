#!/usr/bin/python

import sys, os, time, urllib, datetime, socket, sched, threading
basepath = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

sys.path.append(basepath + '/libs/Adafruit_Python_CharLCD')
import Adafruit_CharLCD as LCD

sys.path.append(basepath + '/libs/requests')
sys.path.append(basepath + '/libs/python-forecast.io')
import requests
from requests.packages import urllib3
urllib3.disable_warnings()
import forecastio

import tempControl

UI = [
    "time",
    {"indoor temp": ['offset up', 'offset down']},
    "outdoor temp",
    {"diagnostics": ['IP', 'reboot']},
    {'auxiliaries': [
        {"fan": ['on', 'off']},
        {"patio melter": ['on', 'off']},
        {"outside light": ['on', 'off']},
        {"garden hose": ['on', 'off']}
    ]}
]

threads = []
topUIidx = 1
##from pymongo import MongoClient
##mongo_client = MongoClient()
def log(message):
    with file(sys.argv[0]+".log", 'a') as logFile:
        logFile.write("%s: %s\n" % (datetime.datetime.now(), message))

def getOutdoor(lcd):
    global topUIidx
    api_key = "e7c48fe5a0555a4792c51c1c6df2064c"
    lat, lng = 42.8543818,-76.1192197
    forecast = forecastio.load_forecast(api_key, lat, lng)
    data = forecast.currently().d
    temp = int(round(data[u'temperature'], 0))
    if topUIidx == 3:
        lcd.clear()
        lcd.message("Outside temp\n%i deg F" % temp)    # return data

def getIp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        return s.getsockname()[0]
    except:
        return "unknown"

def getTime():
    try:
        d = datetime.datetime.now()
        return d.strftime("%m/%d %I:%M %p\n%A")
    except:
        return "error with date"

def setTopMessage(lcd, on=True):
    global topUIidx
    global threads

    lcd.clear()
    if   topUIidx == 1: lcd.message(getTime())
    elif topUIidx == 2:
        temp, humidity = tempControl.getIndoor()
        target = tempControl.getTarget()
        lcd.message("Inside temp: %iF\nSet to:      %iF" % (int(round(temp,0)), target))
    elif topUIidx == 3:
        lcd.message("Outside temp\n...")
        t = threading.Thread(name="outsideTemp", target=getOutdoor, args=(lcd,))
        threads.append(t)	
        t.start()
    elif topUIidx == 4: lcd.message('Press up/down to\nuse Aux. systems')
    elif topUIidx == 5: lcd.message('Welcome to\nRPi Thermostat')

def setAuxMessage(idx, lcd, on):
    lcd.clear()
    if   idx == 0:
        if not on: lcd.message('Press select to\nturn fan on')
        else:      lcd.message('Press select to\nturn fan off')
    elif idx == 1: 
        if not on: lcd.message('Press select to\nturn melter on')
        else:      lcd.message('Press select to\nturn melter off')
    elif idx == 2: 
        if not on: lcd.message('Press select to\nturn light on')
        else:      lcd.message('Press select to\nturn light off')
    elif idx == 3: 
        if not on: lcd.message('Press select to\nturn hose on')
        else:      lcd.message('Press select to\nturn hose off')
    else: lcd.message('Aux menu level\nerror: choice=%i' % idx)

def setDiagMessage(idx, lcd):
    lcd.clear()
    if   idx == 0:
        lcd.message("IP address\n%s" % (getIp()))
    elif idx == 1:
        lcd.message("Press select\nto reboot")

    else:
        lcd.message('Menu Error\ntop level choice=%i' % idx)
    

def setFurnace():
    temp, humidity = tempControl.getIndoor()
    target = tempControl.getTarget()
    if target > temp:
        On = True
    else:
        On = False
        
    callRelay(3, On)

def callRelay(idx, On):
    url = r'http://192.168.42.44/relay%i%s' % (idx, {True:'On', False:"Off"}[On])
    log(url)
    try:
        result = urllib.urlopen(url).read()
    except IOError:
        result = "Remote control unit not responding"
    log(result)

def restart():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    log( output )
    
def main():
    global topUIidx
    global threads

    scheduler = sched.scheduler(time.time, time.sleep)
    nextEventTime = time.mktime(tempControl.getNextEventTime())
    nextEvent = scheduler.enterabs(nextEventTime, 1, setFurnace, None)
    # Start a thread to run the events
    t = threading.Thread(target=scheduler.run)
    t.start()
    
    lcd = LCD.Adafruit_CharLCDPlate()
    lcd.set_color(1,1,1)
    secUIidx = 0
    auxDevices = [False, False, False, False]
    setTopMessage(lcd)
    
    while True:
        
##        mongo_client['HomeControl'].temperature.drop ()
##        mongo_client['HomeControl']['temperature'].insert(temperature)
                
        if lcd.is_pressed(LCD.LEFT):
            secUIidx = 0
            topUIidx -= 1
            if topUIidx < 1:
                topUIidx = len(UI)
            setTopMessage(lcd)
            
        if lcd.is_pressed(LCD.RIGHT):
            secUIidx = 0
            topUIidx += 1
            if topUIidx > len(UI):
                topUIidx = 1
            setTopMessage(lcd)
			
        if lcd.is_pressed(LCD.UP):
            if topUIidx ==2:
                tempControl.offset += 1
                    
                setTopMessage(lcd)
                t = threading.Thread(name="furnaceUp", target=setFurnace)
                threads.append(t)
                t.start()
            if topUIidx == 4:
                secUIidx += 1
                if secUIidx > 3:
                    secUIidx = 0
                setAuxMessage(secUIidx, lcd, auxDevices[secUIidx])

            if topUIidx == 5:
                secUIidx += 1
                if secUIidx > 1:
                    secUIidx = 0
                setDiagMessage(secUIidx, lcd)
                
            
        if lcd.is_pressed(LCD.DOWN):
            if topUIidx ==2:
                tempControl.offset -= 1
                    
                setTopMessage(lcd)
                t = threading.Thread(name="furnaceDown", target=setFurnace)
                threads.append(t)
                t.start()
                
            if topUIidx == 4:
                secUIidx -= 1
                if secUIidx < 0:
                    secUIidx = 1
                setAuxMessage(secUIidx, lcd, auxDevices[secUIidx])
                
            if topUIidx == 5:
                secUIidx -= 1
                if secUIidx < 0:
                    secUIidx = 1
                setDiagMessage(secUIidx, lcd)            
            
        if lcd.is_pressed(LCD.SELECT):
            if topUIidx == 5 and secUIidx == 1:
                lcd.clear()
                lcd.message("\nrebooting...")
                restart()
              
            if topUIidx == 4:
                t = threading.Thread(name="callRelayAux", target=callRelay, args =(secUIidx, auxDevices[secUIidx]))
                threads.append(t)
                t.start()
                auxDevices[secUIidx] = not auxDevices[secUIidx]
                setAuxMessage(secUIidx, lcd, auxDevices[secUIidx])

if __name__ == '__main__':
    
##     check internet connection
##
##     check for relay module

    main()

    
    
