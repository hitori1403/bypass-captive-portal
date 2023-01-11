import re
from subprocess import PIPE, Popen


class Ip:
    @classmethod
    def run(cls, options):
        cmd = ["ip"] + options
        p = Popen(cmd, stdout=PIPE)
        p.wait()
        return p.communicate()

    @classmethod
    def up(cls, interface):
        cls.run(["link", "set", "dev", interface, "up"])

    @classmethod
    def down(cls, interface):
        cls.run(["link", "set", "dev", interface, "down"])

    @classmethod
    def get_interfaces(cls):
        out = cls.run(["link", "show"])[0]
        return re.findall(b": (.*):", out)
