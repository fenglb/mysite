import requests
from bs4 import BeautifulSoup

class ConnectionError(Exception):
    def __inti__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

search_user_link = "http://121.192.191.146/lims/!people/list"
headers = {'content-type':'application/x-www-form-urlencoded', 
           'User-Agent':'Mozilla/5.0(X11;Ubuntu;Linux x86_64;rv:37.0) Gecko/20100101 Firefox/37.0'}

def getUserInfo( s, linker ):
    r = s.get( linker, headers=headers )
    return r.content

def searchUserInfo( s, name ):
    data = {'root_id': 1,
            'group_id': 1,
            'member_type': 2,
            'name': name,
            'search': '查询',
    }
    r = s.post( search_user_link, data=data, headers=headers)
    return r.content

def login( ):
    admin_id = '2013100213'
    admin_password = 'xmu3.14159'
    login_link = "http://121.192.191.146/lims/login"


    s = requests.session()
    login_data = {'token': admin_id,
                    'token_backend': 'database',
                    'password': admin_password, 
                    'submit':'登录',
                    }
    r = s.post(login_link, data=login_data, headers=headers)
    return s


def parseUserInfo( text ):

    soup = BeautifulSoup( text, 'lxml' )
    lists = soup.table.table.tbody.select('tr')
    user = {}

    try:
        items = lists[0].select('td')
        user['name'] = items[1].a.string
    except IndexError:
        return ''

    user['linker'] = items[1].a.attrs['href']
    try:
        user['phone_number'] = items[3].select('div.phone')[0].string
        user['email'] = items[3].select('div.email')[0].string
    except IndexError:
        user['phone_number'] = '05921234567'
        user['email'] = 'unkown@xmu.edu.cn'
    user['group'] = items[4].string
    
    return user

def parseProfileInfo( text ):
    soup = BeautifulSoup( text, 'lxml' )
    content = soup.table.table.tr
    items = content.select('td')[1].select('p')
    user = {}
    user['isPI'] = 'PI' in items[1].get_text()
    user['department'] = items[3].select('a')[1].string
    return user
    
if __name__ == "__main__":
    s = login()
    f = searchUserInfo( s, '候睿' )
    user = parseUserInfo( f )
    if user:
        f = getUserInfo(s, user['linker'] )
        print parseProfileInfo( f )
