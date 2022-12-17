from subprocess import Popen, DEVNULL, STDOUT
from shutil import rmtree
from tempfile import mkdtemp
import csv
import os 

from .airmon import Airmon
from model.client import Client
from model.target import Target

class Airodump:
    def __init__(self, interface, essid_regex=''):
        self.interface = interface
        self.essid_regex = essid_regex
        self.tmpdir = mkdtemp()
        self.csv_filename = ''

    def __enter__(self):
        cmd = [
            'airodump-ng', 
            self.interface,
            '-a',
            '-w', os.path.join(self.tmpdir, 'airodump'),
            '--write-interval', '1'
        ]

        if self.essid_regex:
            cmd.extend(['-R', self.essid_regex])

        self.p = Popen(cmd, stdout=DEVNULL, stderr=STDOUT)
        return self

    def __exit__(self, type, value, traceback):
        self.p.terminate()
        rmtree(self.tmpdir)

    def find_csv_file(self):
        if not self.csv_filename:
            files = os.listdir(self.tmpdir)
            for f in files:
                if f.endswith('.csv') and f.count('.') == 1:
                    self.csv_filename = f
                    break
        return self.csv_filename

    def parse_csv(self):
        self.targets = []
        self.clients = []

        self.find_csv_file()
        if not self.csv_filename:
            return

        with open(os.path.join(self.tmpdir, self.csv_filename), 'r') as f:
            csv_reader = csv.reader(f, skipinitialspace=True)
    
            hit_targets = False
            hit_clients = False
            for row in csv_reader:
                try:
                    if row[0] == 'BSSID':
                        hit_targets = True
                        continue
                    elif row[0] == 'Station MAC':
                        hit_targets = False
                        hit_clients = True
                        continue
                
                    if hit_targets:
                        if row[5] == 'OPN':
                            self.targets.append(Target(row))
                    elif hit_clients:
                        self.clients.append(Client(row))
                except:
                    pass

    def get_targets(self):
        self.parse_csv()
        return self.targets

    def get_clients(self):
        self.parse_csv()
        return self.clients