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
    try:
        time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    except ValueError:
        time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
    time = navicetoaware(time)
    return time
