#!/usr/bin/python

import sys, os, time, urllib, datetime, socket
basepath = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

##sys.path.append(basepath + '/libs/Adafruit_Python_DHT')
##import Adafruit_DHT
##sensor = Adafruit_DHT.DHT22
##pin = 4

sys.path.append(basepath + '/libs/Adafruit_Python_CharLCD')
import Adafruit_CharLCD as LCD

sys.path.append(basepath + '/libs/requests')
sys.path.append(basepath + '/libs/python-forecast.io')
import requests
from requests.packages import urllib3
urllib3.disable_warnings()
import forecastio


##from pymongo import MongoClient
##mongo_client = MongoClient()

def getTarget():
    return 68

def getIndoor():
##    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
##    temperature = temperature * 9/5.0 + 32
    return 62

def getOutdoor():
    api_key = "e7c48fe5a0555a4792c51c1c6df2064c"
    lat, lng = 42.8543818,-76.1192197
    forecast = forecastio.load_forecast(api_key, lat, lng)
    data = forecast.currently().d
    return data

def main():
    lcd = LCD.Adafruit_CharLCDPlate()
    lcd.set_color(1,1,1)
    mindx = 1
    setMessage(0, lcd)
    
    while True:
        
##        mongo_client['HomeControl'].temperature.drop ()
##        mongo_client['HomeControl']['temperature'].insert(temperature)
##
##        if temperature < getTarget:
##            urllib.urlopen(r'http://192.168.42.130/relay2On')
##        else:
##            urllib.urlopen(r'http://192.168.42.130/relay2On')
                
        if lcd.is_pressed(LCD.UP):
            mindx -= 1
            if mindx < 0:
                mindx = 3
            setMessage(mindx, lcd)
            
        if lcd.is_pressed(LCD.DOWN):
            mindx += 1
            if mindx > 3:
                mindx = 0
            setMessage(mindx, lcd)

def setMessage(idx, lcd):
    lcd.clear()
    if   idx == 1: lcd.message(getTime())
    elif idx == 2: lcd.message("IP address\n%s" % (getIp()))
    elif idx == 3:
        lcd.message("Outside temp\n...")
        temp = int(round(getOutdoor()[u'temperature'], 0))
        lcd.clear()
        lcd.message("Outside temp\n%i deg F" % temp)
    else: lcd.message('Welcome to\nRPi Thermostat')
    
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

if __name__ == '__main__':
    
##     check internet connection
##
##     check for relay module

    main()

    
    
