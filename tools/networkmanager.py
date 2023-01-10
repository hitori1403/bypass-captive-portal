import time
from subprocess import PIPE, Popen, DEVNULL

from pwn import log


class NetworkManager:
    @classmethod
    def run(cls, cmd):
        while True:
            p = Popen(cmd, stdout=DEVNULL, stderr=PIPE)
            p.wait()

            if p.returncode:
                log.warn(p.stderr)
                log.warn("Rerun NetworkManager after 5s...")
                time.sleep(5)
            else:
                break

    @classmethod
    def start(cls):
        cls.run(["systemctl", "start", "NetworkManager"])

    @classmethod
    def stop(cls):
        cls.run(["systemctl", "stop", "NetworkManager"])

    @classmethod
    def connect2wifi(cls, ssid):
        cls.run(["nmcli", "d", "wifi", "connect", ssid])
