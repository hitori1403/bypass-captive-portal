from subprocess import Popen
from time import sleep

from .ip import Ip
from .networkmanager import NetworkManager

class Macchanger:
    def __init__(self, interface):
        self.interface = interface

    def run(self, options):
        NetworkManager.stop()
        Ip(self.interface).down()
        
        self.cmd = ['macchanger'] + options + [self.interface]
        p = Popen(self.cmd + options)
        p.wait()
        
        Ip(self.interface).up()
        NetworkManager.start()

    def random(self):
        self.run(['-r'])

    def reset(self):
        self.run(['-p'])
    
    def change(self, mac):
        self.run(['-m', mac])