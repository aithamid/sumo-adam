import threading
import random

import traci
from influxdb_client import InfluxDBClient
from sumolib import checkBinary

sumoBinary = checkBinary('sumo-gui')


class Vehicle:
    number_vehicles = 0

    def __init__(self):
        pass


class Launcher:
    def __init__(self, c_delay):
        with InfluxDBClient.from_config_file("creds.toml") as self.client:
            self.query_api = self.client.query_api()
            self.write_api = self.client.write_api()
            self.delete_api = self.client.delete_api()
        self.delay = c_delay
        self.port = 51845
        print("Simulation created")
        # traci.start(
        #     port=self.port,
        #     cmd=[
        #         sumoBinary,
        #         '-c', '../sumo/sumo.cfg',
        #         '--delay', str(self.delay),
        #         '--start','--num-clients','2'
        #     ]
        # )
        traci.init(port=8813)
        my_thread = threading.Thread(target=self.start)
        my_thread.start()

    def start(self):
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
        traci.close()
