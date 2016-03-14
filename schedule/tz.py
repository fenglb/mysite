import pytz
import datetime
cntz = pytz.timezone('Asia/Shanghai')
utctz = pytz.timezone('UTC')

def cnfromutc( time ):
    time = cntz.normalize(time.astimezone(cntz))# + datetime.timedelta(minutes=7)
    return time
def cntoutc( time ):
    time = utctz.normalize(time.astimezone(utctz))
    return time
    
