import sys, time, urllib2, datetime

sys.path.append(r'..\libs\Adafruit_Python_DHT')
sys.path.append(r'..\libs\Adafruit_Python_CharLCD')

import Adafruit_DHT
sensor = Adafruit_DHT.DHT22
pin = 4

from pymongo import MongoClient
mongo_client = MongoClient()

def getTarget():
    return 68

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    temperature = temperature * 9/5.0 + 32

    mongo_client['HomeControl'].temperature.drop ()
    mongo_client['HomeControl']['temperature'].insert(temperature)

    if temperature < getTarget:
        urllib2.urlopen(r'http:\\192.168.1.101\relay2On')
    else:
        urllib2.urlopen(r'http:\\192.168.1.101\relay2Off')
            
    time.sleep(60)
