import threading
import time
from datetime import datetime

import self as self
import traci
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class UpdateDB:
    def __init__(self, c_delay):
        self.i = None
        self.simu_id = 1
        self.list = None
        self.start_time = '1970-01-01T00:00:00Z'
        self.end_time = '2099-12-31T23:59:59Z'
        with InfluxDBClient.from_config_file("creds.toml") as self.client:
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
            self.delete_api = self.client.delete_api()
        self.delay = c_delay
        my_thread = threading.Thread(target=self.update)
        my_thread.start()

    def update(self):
        self.i = 1
        while traci.simulation.getMinExpectedNumber() > 0:
            self.insertDB()
            self.insertvehicles()
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

    def insertvehicles(self):
        if self.list != traci.vehicle.getIDList():
            self.delete_api.delete(start=self.start_time, stop=self.end_time,
                                   predicate='_measurement="{}"'.format("vehicles"), bucket="db", org="ERENA")
            data_point = Point("vehicles") \
                .tag("vehlist", str(traci.vehicle.getIDList())) \
                .field("test", 0) \
                .time(datetime.utcnow())
            self.write_api.write(bucket="db", record=data_point)
            self.list = traci.vehicle.getIDList()
            print(traci.vehicle.getIDList())
