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
        log.info("Spoofing client...")
        self.interface = interface
        mac = next(self.get_station)

        log.info(f"Changing current MAC to {mac}...")
        macchanger = Macchanger(interface)
        macchanger.change(mac)

        log.info("Sleeping 5s...")
        time.sleep(5)

        log.info(f'Connecting to Wi-Fi "{self.essid}"...')
        NetworkManager.connect2wifi(self.essid)

        log.info("Spoofed successfully!")

    def reset_mac(self):
        log.info("Reseting MAC...")

        if not self.interface:
            log.error("Interface not found!")
        else:
            macchanger = Macchanger(self.interface)
            macchanger.reset()

            log.info(f'Connecting to Wi-Fi "{self.essid}"...')
            NetworkManager.connect2wifi(self.essid)

            log.info("Reset successfully!")

    def print_info(self):
        if not self.username and not self.password:
            log.warn("No info!")
            return
        if self.username:
            success(f"Username: {self.username}")
        if self.password:
            success(f"Password: {self.password}")
        if self.etr:
            success(f"Time remaining: {self.etr}")

    def store(self):
        log.info("Saving session...")

        os.makedirs("sessions", exist_ok=True)
        sessions = {}

        try:
            with open(f"sessions/{self.name}.json", "r") as f:
                sessions = json.load(f)
        except:
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

        log.info("Session saved!")
