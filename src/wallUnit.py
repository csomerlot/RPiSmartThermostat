#!/usr/bin/python

import sys, time, urllib, datetime, socket

import Adafruit_CharLCD as LCD

##sys.path.append(r'..\libs\Adafruit_Python_DHT')
##sys.path.append(r'..\libs\Adafruit_Python_CharLCD')
##
##import Adafruit_DHT
##sensor = Adafruit_DHT.DHT22
##pin = 4

##from pymongo import MongoClient
##mongo_client = MongoClient()

def getTarget():
    return 68

def getTemp():
##    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
##    temperature = temperature * 9/5.0 + 32
    return 62

def main():
    lcd = LCD.Adafruit_CharLCDPlate()
    lcd.set_color(1,1,1)
    
    messages = ['RPi Thermostat']
    messages.append(getTime())
    messages.append("IP %s" % getIp())
    mindx = 1
    lcd.message(messages[mindx])
    
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
            if mindx == 0:
                mindx = len(messages)-1

            lcd.clear()
            lcd.message(messages[mindx])
            
        if lcd.is_pressed(LCD.DOWN):
            mindx += 1
            if mindx == len(messages)-1:
                mindx = 0

            lcd.clear()
            lcd.message(messages[mindx])

def getIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    return s.getsockname()[0]

def getTime():
    d = datetime.datetime.now()
    return d.strftime("%m/%d %I:%M")

if __name__ == '__main__':
    
    ## check internet connection
    
    ## check for relay module

    ## get local weather

    main()
    
    
