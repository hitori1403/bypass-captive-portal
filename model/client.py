class Client:
    def __init__(self, fields):
        # ['Station MAC', 'First time seen', 'Last time seen', 'Power',
        #  '# packets', 'BSSID', 'Probed ESSIDs']
        fields = [x.strip() for x in fields]

        self.station = fields[0]
        self.power = int(fields[3])
        self.packets = int(fields[4])
        self.bssid = fields[5]
        self.probed_essids = fields[6]

