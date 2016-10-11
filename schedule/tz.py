import pytz
from datetime import datetime
cntz = pytz.timezone('Asia/Shanghai')
utctz = pytz.timezone('UTC')

def navicetoaware( time ):
    return cntz.localize( time )

def cnfromutc( time ):
    time = cntz.normalize(time.astimezone(cntz))# + datetime.timedelta(minutes=7)
    return time
def cntoutc( time ):
    time = utctz.normalize(time.astimezone(utctz))
    return time

def strptime( time_str ):
    time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    time = navicetoaware(time)
    return time
