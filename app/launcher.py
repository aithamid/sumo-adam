import sys
import threading
import random

import traci
from influxdb_client import InfluxDBClient
from sumolib import checkBinary

sumoBinary = checkBinary('sumo-gui')


class Launcher:
    def __init__(self, state=None, delay=None, ip=None, port=None):
        self.ip = None
        with InfluxDBClient.from_config_file("creds.toml") as self.client:
            self.query_api = self.client.query_api()
            self.write_api = self.client.write_api()
            self.delete_api = self.client.delete_api()

        if state == "connect":
            self.ip = ip
            self.port = port
            self.thread = threading.Thread(target=self.connect)
            self.thread.start()
        elif state == "start":
            self.port = port
            self.delay = delay
            self.thread = threading.Thread(target=self.start)
            self.thread.start()
        elif state == "stop":
            self.stop()

    def start(self):
        traci.start(
            port=self.port,
            cmd=[
                sumoBinary,
                '-c', '../sumo/sumo.cfg',
                '--delay', str(self.delay),
                '--start', '--num-clients', '1'
            ]
        )
        while self.running_flag:
            # Your simulation steps here
            traci.simulationStep()
        traci.close()

    def connect(self):
        traci.init(port=int(self.port), host=self.ip)
        while self.running_flag:
            traci.simulationStep()
        traci.close()

    def stop(self):
        self.running_flag = False
