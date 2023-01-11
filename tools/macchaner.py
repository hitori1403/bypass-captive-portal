from subprocess import DEVNULL, Popen

from .ip import Ip
from .networkmanager import NetworkManager


class Macchanger:
    def __init__(self, interface):
        self.interface = interface

    def run(self, options):
        NetworkManager.stop()
        Ip.down(self.interface)

        self.cmd = ["macchanger"] + options + [self.interface]
        p = Popen(self.cmd + options, stdout=DEVNULL)
        p.wait()

        Ip.up(self.interface)
        NetworkManager.start()

    def random(self):
        self.run(["-r"])

    def reset(self):
        self.run(["-p"])

    def change(self, mac):
        self.run(["-m", mac])
