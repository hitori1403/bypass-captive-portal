import json
import os
import time
from abc import ABC, abstractmethod

from pwn import log, success

from tools.macchaner import Macchanger
from tools.networkmanager import NetworkManager


class Network(ABC):
    def __init__(self, client):
        self.name = ""
        self.username = ""
        self.password = ""
        self.etr = ""
        self.essid = client.essid
        self.stations = [client.station]
        self.get_station = self.stations_generator()

    @abstractmethod
    def get_creddentials(self):
        pass

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def logout(self):
        pass

    def stations_generator(self):
        for s in self.stations:
            yield s

    def spoof(self, interface):
        mac = next(self.get_station)
        p = log.progress(f"Spoof client {mac}")
        self.interface = interface

        p.status("Changing MAC")
        macchanger = Macchanger(interface)
        macchanger.change(mac)

        p.status("Sleeping 5s")
        time.sleep(5)

        p.status(f'Connecting to Wi-Fi "{self.essid}"')
        NetworkManager.connect2wifi(self.essid)

        p.success("Spoofed successfully!")

    def reset_mac(self):
        p = log.progress("Reset MAC")

        if not self.interface:
            log.error("Interface not found!")
        else:
            macchanger = Macchanger(self.interface)
            macchanger.reset()

            p.status(f"Connecting to Wi-Fi '{self.essid}'")
            NetworkManager.connect2wifi(self.essid)

            p.success("Reset successfully!")

    def print_info(self):
        if not self.username and not self.password:
            log.warn("No info!")
            return
        msg = ""
        if self.username:
            msg += f"Username: {self.username}\n"
        if self.password:
            msg += f"Password: {self.password}\n"
        if self.etr:
            msg += f"Time remaining: {self.etr}\n"
        success(msg)

    def store(self):
        p = log.progress("Save session")

        os.makedirs("sessions", exist_ok=True)
        sessions = {}

        try:
            with open(f"sessions/{self.name}.json", "r") as f:
                sessions = json.load(f)
        except Exception:
            pass

        if self.username in sessions:
            sessions[self.username]["etr"] = self.etr

            sessions[self.username]["stations"].extend(self.stations)
            sessions[self.username]["stations"] = list(
                set(sessions[self.username]["stations"])
            )
        else:
            sessions[self.username] = {"etr": self.etr, "stations": self.stations}

        with open(f"sessions/{self.name}.json", "w") as f:
            json.dump(sessions, f, indent=2)

        p.success("Session saved!")
