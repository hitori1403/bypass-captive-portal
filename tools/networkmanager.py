from subprocess import Popen
import time

class NetworkManager:
    @classmethod
    def run(cls, cmd):
        while True:
            p = Popen(cmd)
            p.wait()
            
            if p.returncode:
                print('[!] Rerun NetworkManager after 5s...')
                time.sleep(5)
            else:
                break

    @classmethod
    def start(cls):
        cls.run(['systemctl', 'start', 'NetworkManager'])
    
    @classmethod
    def stop(cls):
        cls.run(['systemctl', 'stop', 'NetworkManager'])

    @classmethod
    def connect2wifi(cls, ssid):
        cls.run(['nmcli', 'd', 'wifi', 'connect', ssid])