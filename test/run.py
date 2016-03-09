import sqlite3 as sql
from accounts.models import CustomUser
from schedule.models import Experiment
from schedule.models import Instrument

def output_users():
    conn = sql.connect('bk.sqlite3')
    keys = "id, username, surname, identify".split(",")
    keys = [key.strip() for key in keys ]
    cur  = conn.execute("""
            SELECT id, username, surname, identify from customAuth_CustomUser
            """
            )
    users = {}
    for item in cur:
        users[item[0]] = {"surname":item[2], "identify":str(item[3])}
            
    return users

def output_experiment():
    conn = sql.connect('bk.sqlite3')
    keys = "user_id, instrument, start_time, stop_time, created_time".split(',')
    keys = [key.strip() for key in keys ]
    cur  = conn.execute("""
            SELECT user_id, instrument, start_time, stop_time, created_time from schedule_Experiment
            """
            )
    exps = []
    for item in cur:
        u = {}
        for i, key in enumerate(keys):
            u[key] = item[i]
        exps.append(u)
 
    return exps

from datetime import datetime
def main():
    users = output_users()
    exps = output_experiment()

    for exp in exps:
        user = users[exp["user_id"]]
        try:
            person = CustomUser.objects.get(surname=user['surname'], identify=user['identify'])
        except CustomUser.DoesNotExist:
            print("user does not exist", user['surname'])
            return;
        try:
            instrument = Instrument.objects.get( short_name=exp["instrument"] )
        except Instrument.DoesNotExist:
            print("Inst does not exist")
            return;
        experiment = Experiment()
        start_time = datetime.strptime(exp["start_time"], "%Y-%m-%d %H:%M:%S")
        stop_time = datetime.strptime(exp["stop_time"], "%Y-%m-%d %H:%M:%S")
        experiment.start_time = start_time
        experiment.created_time  = datetime.strptime(exp["created_time"], "%Y-%m-%d %H:%M:%S.%f")
        experiment.times = ( stop_time-start_time ).seconds / 3600.
        experiment.user = person
        experiment.instrument = instrument
        experiment.save()
