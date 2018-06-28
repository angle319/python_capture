#from key_control.dd import dd,ddClick
import time
import datetime
def getNowTime():
            now=datetime.datetime.now()
            timestamp = time.mktime(now.timetuple())
            return timestamp



print  getNowTime()
# time.sleep(5)
# ddClick(1291,340)

# time.sleep(1)

# ddClick(1577,654)