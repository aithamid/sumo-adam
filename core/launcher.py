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
        self.running_flag = True
        self.error = False
        with InfluxDBClient.from_config_file("creds.toml") as self.client:
            self.query_api = self.client.query_api()
            self.write_api = self.client.write_api()
            self.delete_api = self.client.delete_api()

        if state == "connect":
            self.ip = ip
            self.port = port
            try:
                traci.init(port=int(self.port), host=self.ip, numRetries=0)
                self.thread = threading.Thread(target=self.connect)
                self.thread.start()
            except traci.FatalTraCIError as e:
                print(f"Error occurred during TraCI communication: {e}")
                self.error = True
            except Exception as e:
                print(f"Unexpected error occurred: {e}")
                self.error = True
        elif state == "start":
            self.port = port
            self.delay = delay
            traci.start(
                port=self.port,
                cmd=[
                    sumoBinary,
                    '-c', 'sumo/sumo.cfg',
                    '--delay', str(self.delay),
                    '--start'
                ]
            )
            self.thread = threading.Thread(target=self.start)
            self.thread.start()
        elif state == "stop":
            self.stop()

    def start(self):
        while self.running_flag:
            traci.simulationStep()
        traci.close()

    def connect(self):
        while self.running_flag:
            traci.simulationStep()
        traci.close()


    def stop(self):
        self.running_flag = False
