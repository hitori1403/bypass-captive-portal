import re

import requests

from ..network import Network


class CampusVNU(Network):
    name = "CampusVNU"
    url = "http://campusvnu.vn"

    def get_creddentials(self):
        r = requests.get(self.url + "/status")
        r.encoding = "utf-8"

        if "Thông Tin Tài Khoản" not in r.text:
            return False

        self.username = re.search('"username":"(.*?)"', r.text)[1].lower()
        self.etr = re.search('"session-time-left":"(.*?)"', r.text)[1]
        return True

    def login(self):
        r = requests.post("https://campusvnu.vn/login", {"username": self.username})
        r.encoding = "utf8"
        if "Expired prepaid card!" in r.text:
            self.etr = 0
            return False
        return "Đăng Nhập Thành Công" in r.text

    def logout(self):
        requests.get(self.url + "/logout")
