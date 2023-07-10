import threading
import time
from datetime import datetime

import traci
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class UpdateDB:
    def __init__(self, c_delay):
        self.i = None
        self.simu_id = 1
        with InfluxDBClient.from_config_file("creds.toml") as self.client:
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.delay = c_delay
        my_thread = threading.Thread(target=self.update)
        my_thread.start()

    def update(self):
        self.i = 1
        while traci.simulation.getMinExpectedNumber() > 0:
            print("ça marche")
            self.insertDB()
            time.sleep(self.delay / 1000)
        traci.close()

    def insertDB(self):
        for vehId in traci.vehicle.getIDList():
            x, y = traci.vehicle.getPosition(vehId)
            lon, lat = traci.simulation.convertGeo(x, y)
            data_point = Point("sumo") \
                .tag("vehicle_id", vehId) \
                .field("simu_id", self.simu_id) \
                .field("iteration_id", self.i) \
                .field("longitude", lon) \
                .field("latitude", lat) \
                .field("co2", traci.vehicle.getCO2Emission(vehId)) \
                .field("speed", traci.vehicle.getSpeed(vehId)) \
                .time(datetime.utcnow())
            self.write_api.write(bucket="db", record=data_point)
        self.i += 1
