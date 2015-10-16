from datetime import *

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
    print schedule
    
