from accounts.models import CustomUser
from eguard.eguardcrawler import EntranceGuard
from eguard.models import Entrance

def main():
    eguard = EntranceGuard()
    doors = Entrance.objects.all()
    for door in doors:
        perm_users = eguard.getEntranceUsers( door.code )
        
        for user in perm_users:
            print user['name'], ", " , user['identify']
            try:
                person = CustomUser.objects.get( surname=user['name'], identify=user['identify'] )
            except CustomUser.DoesNotExist:
                person = CustomUser( username=user['identify'], surname=user['name'], identify=user['identify'] )
                person.save()

            if person.is_expired():
                eguard.doEntranceUserDeleted( person.identify, door.code )
            else:
                door.user.add( person )
