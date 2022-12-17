from subprocess import Popen
import os

class Ip:
    def __init__(self, interface):
        self.interface = interface
    
    def run(self, options):
        cmd = ['ip', 'link', 'set', 'dev', self.interface] + options
        p = Popen(cmd)
        p.wait()

    def up(self):
        self.run(['up'])

    def down(self):
        self.run(['down'])