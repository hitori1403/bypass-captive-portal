class Target:
    def __init__(self, fields):
        # ['BSSID', 'First time seen', 'Last time seen', 'channel', 'Speed',
        #  'Privacy', 'Cipher', 'Authentication', 'Power', '# beacons', '# IV',
        #  'LAN IP', 'ID-length', 'ESSID', 'Key']
        fields = [x.strip() for x in fields]

        self.bssid = fields[0]
        self.privacy = fields[5]
        self.power = int(fields[8])
        self.beacons = int(fields[9])
        self.essid = fields[13]
