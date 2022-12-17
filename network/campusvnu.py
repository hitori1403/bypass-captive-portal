import requests
import re


class CampusVNU:
    def __init__(self, username=''):
        self.name = 'CampusVNU'
        self.url = 'http://campusvnu.vn'
        self.username = username
        self.etr = ''
    
    def get_info(self):
        r = requests.get(self.url + '/status')
        r.encoding = 'utf-8'

        if not 'Thông Tin Tài Khoản' in r.text:
            return False
        
        self.username = re.search('"username":"(.*?)"', r.text)[1]
        self.etr = re.search('"session-time-left":"(.*?)"', r.text)[1]
        return True

    def login(self):
        r = requests.post('https://campusvnu.vn/login', {
            'username': self.username 
        })
        r.encoding = 'utf8'
        return 'Đăng Nhập Thành Công' in r.text
        
    def logout(self):
        requests.get(self.url + '/logout')

    def print_info(self):
        print('[+] Username:', self.username)
        print('[+] Time remaining:', self.etr)