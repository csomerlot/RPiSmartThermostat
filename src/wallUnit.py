import sys, time, urllib, datetime

##sys.path.append(r'..\libs\Adafruit_Python_DHT')
##sys.path.append(r'..\libs\Adafruit_Python_CharLCD')
##
##import Adafruit_DHT
##sensor = Adafruit_DHT.DHT22
##pin = 4

from pymongo import MongoClient
mongo_client = MongoClient()

def getTarget():
    return 68

def getTemp():
##    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
##    temperature = temperature * 9/5.0 + 32
    return 62

def main():
    while True:
        

        mongo_client['HomeControl'].temperature.drop ()
        mongo_client['HomeControl']['temperature'].insert(temperature)

        if temperature < getTarget:
            urllib.urlopen(r'http://192.168.42.130/relay2On')
        else:
            urllib.urlopen(r'http://192.168.42.130/relay2On')
                
        time.sleep(60)


if __name__ == '__main__':

    ## check internet connection
    
    ## check for relay module

    ## get local weather
    
