import requests
from bs4 import BeautifulSoup
from datetime import datetime

admin_id = '2009100146'
admin_password = '123456'
login_link = "http://idstar.xmu.edu.cn/amserver/UI/Login"
search_link = 'http://eguard.xmu.edu.cn/ImportUser.asp'
search_user_link = 'http://eguard.xmu.edu.cn/SearchUser.asp'
entrance_search_link = 'http://eguard.xmu.edu.cn/SearchList.asp'
entrance_add_link = 'http://eguard.xmu.edu.cn/IntoList.asp'
entrance_record_search_link = 'http://eguard.xmu.edu.cn/SearchResult.asp'
entrance_delete_link = 'http://eguard.xmu.edu.cn/BatchDel.Asp'

headers = {'content-type':'application/x-www-form-urlencoded', 
           'User-Agent':'Mozilla/5.0(X11;Ubuntu;Linux x86_64;rv:37.0) Gecko/20100101 Firefox/37.0'}

def login():
    s = requests.session()
    login_data = {'IDToken0': '',
                    'IDToken1': admin_id,
                    'IDToken2': admin_password, 
                    'IDButton':'Log In',
                    'goto':'http://eguard.xmu.edu.cn/index.asp',
                    'gx_charset': 'UTF-8', }
    r = s.post(login_link, data=login_data, headers=headers)
    return s

def searchUser( s, identify, name ):

    entrance_data = { 'txtNo': identify,
                      'txtName': name.encode('gbk'),
                      'submit':'查询', }

    r = s.post(search_link, data=entrance_data, headers=headers)

    return r.content
def parseUsersInfo( f ):

    if "没有相关的查询结果，请重试！" in f:
        return True, ""

    soup = BeautifulSoup( f )
    tables = soup.find_all("table")
    curPage, endPage = [int(x) for x in tables[1].select("td strong")[0].text.split("/")]
    trs = tables[0].select("tr")
    Users = []
    isEnd = curPage == endPage

    for tr in trs[2:]:
        tds = tr.select("td")
        user = {}
        user['identify'] = tds[1].string.strip()
        user['name'] = tds[2].string.strip()
        user['department'] = tds[5].string.strip()
        user['college'] = tds[6].string.strip()
        Users.append( user )

    return isEnd, Users

def checkUserExist( name, identify ):
    s = login()
    f = searchUser( s, identify, name )
    isEnd, user = parseUsersInfo( f.decode('gbk') )
    if user:
        return True
    else:
        return False

# entrace Id
# 75|2*     核磁室外门[500M]
# 75|3*     高102
# 75|4*     里门
# 76|2*     核磁室里门[600M]
def searchEntranceUsers( s, door, identify=None, name=None ):

    #if name:
    #    name = name.encode('gb2312')

    entrance_data = { 'selWorkArea': door,
                    'txtNo': identify,
                    'txtName': name.encode('gbk'),
                   'submit':'查询', }

    r = s.post(entrance_search_link, data=entrance_data, headers=headers)

    return s

def getEntranceUsersInfo( s, index ):
    pageload = {'page':index}
    r = s.get( entrance_search_link, params=pageload, headers=headers)
    return r.content

def parseEntranceUsersInfo( f ):

    if "没有相关的查询结果，请重试！" in f:
        return True, ""

    soup = BeautifulSoup( f  )
    tables = soup.find_all("table")
    curPage, endPage = [int(x) for x in tables[1].select("td strong")[0].text.split("/")]
    trs = tables[0].select("tr")
    Users = []
    isEnd = curPage == endPage

    for tr in trs[1:]:
        tds = tr.select("td")
        user = {}
        user['identify'] = tds[1].string.strip()
        user['name'] = tds[2].string.strip()
        user['department'] = tds[5].string.strip()
        user['college'] = tds[6].string.strip()
        Users.append( user )

    return isEnd, Users

def deleteEntranceUser( s, cmd ):

    data =  { 'ck': cmd, 'action': 'ListBatchDel', 'Submit':'查询', }

    f = s.post(entrance_delete_link, data=data, headers=headers)
    return True

def addEntranceUser( s, identify, door ):

    data = {"selWorkArea": door,
            "ck": identify }
    r = s.post( entrance_add_link, data=data, headers=headers )

    return "操作成功" in r.content.decode("gbk")

def searchEntranceRecord(s, door, startdate, enddate, starttime, endtime ):

    search_data = { 'startdate': startdate, #2016-2-18
                    'enddate': enddate, #2016-2-18
                    'starttime': starttime, #00:00:00
                    'endtime': endtime, #23:59:59
                    'selWorkArea': door, #75|2*75|3*75|4*76|1*76|2*76|3*
                    'submit':'查询', }

    r = s.post(entrance_record_search_link, data=search_data, headers=headers)
    return s

def getEntranceRecordInfo( s, index ):

    pageload = {'page': index}

    r = s.get( entrance_record_search_link, params=pageload, headers=headers)
    return r.content

def parseEntranceRecordInfo( f ):

    if "没有相关的查询结果，请重试！" in f:
        return True, ""

    soup = BeautifulSoup( f )
    tables = soup.find_all("table")
    curPage, endPage = [int(x) for x in tables[1].select("td strong")[0].text.split("/")]
    trs = tables[0].select("tr")
    Users = []
    isEnd = curPage == endPage

    for tr in trs[2:]:
        tds = tr.select("td")
        user={}
        user['identify'] = tds[1].a.string.strip()
        user['name'] = tds[2].a.string.strip()
        date = tds[4].string.strip()
        time = tds[5].string.strip()
        dt = "{0} {1}".format( date, time )
        user['datetime'] = datetime.strptime( dt, "%Y-%m-%d %H:%M:%S" )
        user['door'] = tds[6].string.strip()
        Users.append(user)

    return isEnd, Users

# door dict
# keys ----> index
# 0    ----> door id for search 
# 1    ----> door id for add
# 2    ----> door id for delete
# 3    ----> door introduction
door_dict = {"D500": {"search":"75|2*", "add": "75|2", "delete":"75|2", "intro":"高-102旁边"}, #核磁室500M门
             "D102": {"search":"75|3*", "add":"75|3", "delete":"75|4", "intro":"高-102"}, #大门
             "D103": {"search":"75|4*", "add":"75|4", "delete":"75|8", "intro":"化院附属楼103楼梯旁"}, #里门
             "D600": {"search":"76|2*", "add":"76|2", "delete":"76|2", "intro":"报告厅106大门"}, #核磁室600M门
            }

class EntranceGuard:
    """
    operation the entrance guard of HF NMR, get the info from School Service,
    create and delete the user from School Service web.
    """
    def __init__(self):

        self.handle = login()

    def getEntranceUsers( self, door ):
        door = door_dict[door]["search"]
        s = searchEntranceUsers( self.handle, door )
        start = 1
        all_entrance_users= []
        while 1:
            f = getEntranceUsersInfo( s, start ).decode('gbk')
            isend, users = parseEntranceUsersInfo( f )
            if not users: break
            all_entrance_users = all_entrance_users +  users
            if isend: break
            start = start + 1

        return all_entrance_users # dist of identify, name, department, and jj

    def getEntranceRecords( self, door, startdate, enddate, starttime, endtime ):
        door = door_dict[door]["search"]
        s = searchEntranceRecord( self.handle, door, startdate, enddate, starttime, endtime )
        start = 1
        all_entrance_user_records = []
        while 1:
            f = getEntranceRecordInfo( s, start ).decode('gbk')
            isend, users = parseEntranceRecordInfo( f )
            if not users: break
            all_entrance_user_records = all_entrance_user_records +  users
            if isend: break
            start = start + 1

        return all_entrance_user_records # dict include identify, datetime, door

    def doEntranceUserDeleted( self, identify, door ):
        #s = searchEntranceUsers( self.handle,  door, identify, name )
        #f = getEntranceUsersInfo( s, '1').decode('gbk')
        #isend, user = parseEntranceUsersInfo( f )
        #if user:
        door = door_dict[door]['delete']
        cmd = '{0}|{1}'.format(door, identify)
        success = deleteEntranceUser( self.handle, cmd )
        return success

    def doEntranceUserCreated( self, identify, door ):
        door = door_dict[door]["add"]
        #f = searchUser( self.handle, identify, name ).decode('gbk')
        #isend, user = parseUsersInfo( f )
        #if user:
        success = addEntranceUser( self.handle, identify, door )
        return success
   
if __name__ == "__main__":

    #eguard = EntranceGuard()
    #users = eguard.getEntranceRecords( door_dict["B"][0], "2016-2-18", "2016-2-19", "00:00:00", "23:59:59" )
    #users = eguard.getEntranceUsers( "D102" )
    #for user in users:
    #    print( "{0}\t {1}".format( user['name'], user['identify'] ) )
    #print eguard.doEntranceUserCreated( ["15720111151868", "20620078101155"], "D102" )
    #for i, d in zip( ["20620078101155"], ["D500"] ):
    #    eguard.doEntranceUserDeleted( i, d )
    #for i, d in zip( ["20620078101155", "20620078101155", "15720111151868"], ["D102","D500", "D500"] ):
    #    print eguard.doEntranceUserCreated( i, d )
    #print( checkUserExist( '冯柳宾'.encode('gbk'), '2013100213' ))
    print( checkUserExist( '陈玥莹'.encode('gbk'), '26920161152886' ))
