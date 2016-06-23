#!/usr/bin/python

from datetime import *
import Adafruit_DHT

offset = 0
base   = 62

schedule = {
    'Weekend': {
        6:  base + 3,
        20: base
    },
    'Weekday': {
        6:  base + 3,
        8:  base,
        16: base + 3,
        20: base
    }
}

def getIndoor():
    sensor = Adafruit_DHT.DHT22
    pin = 4
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    temperature = temperature * 9/5.0 + 32
    return temperature, humidity
    
def getOutdoor():
    api_key = "e7c48fe5a0555a4792c51c1c6df2064c"
    lat, lng = 42.8543818,-76.1192197
    forecast = forecastio.load_forecast(api_key, lat, lng)
    data = forecast.currently().d
    return int(round(data[u'temperature'], 0))

def getDayOfWeek(now):
    if now.date().weekday in [5,6]:  
        return 'Weekend'
    else:                            
        return 'Weekday'
        
def getTarget():
    now = datetime.now()
    temp = base
    dayOfWeek = getDayOfWeek(now)
    
    for hour in sorted(schedule[dayOfWeek]):
        if now.hour > hour:
            temp = schedule[dayOfWeek][hour]
            
    return temp+offset

def getNextEventTime():
    now = datetime.now()
    dayOfWeek = getDayOfWeek(now)

    if now.hour >= max(schedule[dayOfWeek]):
        ## go to next day
        newDate = now.date() + timedelta(1)
        dayOfWeek = getDayOfWeek(datetime.combine(newDate, time(0)))
        nextTime  = time(min(schedule[dayOfWeek]))
        nextEvent = datetime.combine(newDate, nextTime)
    
    else:
        times = sorted(schedule[dayOfWeek])
        times.reverse()

        for t in times:
            if now.hour < t: nextTime = time(t)
            
        nextEvent = datetime.combine(now.date(), nextTime)

    return nextEvent.timetuple()
    

if __name__ == '__main__':
    print getIndoor()
    
