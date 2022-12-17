from subprocess import Popen

class Airmon:
    @classmethod
    def run(cls, options):
        cmd = ['airmon-ng'] + options
        p = Popen(cmd)
        p.wait()
    
    @classmethod
    def start(cls, interface):
        cls.run(['start', interface])
        return interface + 'mon'
    
    @classmethod
    def stop(cls, interface):
        cls.run(['stop', interface])
        return interface[:-3]