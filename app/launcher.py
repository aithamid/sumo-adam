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
        self.delay = c_delay
        print("Simulation created")
        traci.start(
            [
                sumoBinary,
                '-c', '../sumo/sumo.cfg',
                '--delay', str(self.delay),
                '--start'
            ]
        )
        my_thread = threading.Thread(target=self.start)
        my_thread.start()

    def start(self):
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            self.check_too_add()
        traci.close()

    def update(self):
        pass

    def check_too_add(self):
        result = self.query_api.query("""
                                from(bucket: "db")
  |> range(start: 0)
  |> filter(fn: (r) => r["_measurement"] == "toadd")
  |> filter(fn: (r) => r["_field"] == "vehicle_id")
  |> yield(name: "mean")
                    """)
        if len(result) == 0:
            myjson = result.to_json()
            print(myjson)


    def insert(self):
        pass

    def addVehicle(self, vehicle):
        pass

    def removeVehicle(self, vehicle):
        pass
