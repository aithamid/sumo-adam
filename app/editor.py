import threading
import time
import random
import traci
from influxdb_client import InfluxDBClient, Point


class Editor:
    def __init__(self, c_delay = 1000):
        self.delay = c_delay
        self.toremove = None
        self.toadd = None
        self.start_time = '1970-01-01T00:00:00Z'
        self.end_time = '2099-12-31T23:59:59Z'
        self.query = """from(bucket: "db")
        |> range(start: 0)
        |> filter(fn: (r) => r["_measurement"] == "{}")
        |> filter(fn: (r) => r["_field"] == "vehicle_id")
        |> yield(name: "mean")
                      """

        with InfluxDBClient.from_config_file("../app/creds.toml") as self.client:
            self.query_api = self.client.query_api()
            self.write_api = self.client.write_api()
            self.delete_api = self.client.delete_api()

        self.delete_api.delete(start=self.start_time, stop=self.end_time,
                               predicate='_measurement="{}"'.format("toadd"), bucket="db", org="ERENA")
        self.delete_api.delete(start=self.start_time, stop=self.end_time,
                               predicate='_measurement="{}"'.format("toremove"), bucket="db", org="ERENA")

        my_thread = threading.Thread(target=self.loop)
        my_thread.start()

    def loop(self):
        while traci.simulation.getMinExpectedNumber() > 0:
            self.check_toadd()
            self.check_toremove()
            time.sleep(self.delay / 1000)

    def check_toremove(self):
        result = self.query_api.query(self.query.format("toremove"))
        self.toremove = result
        if len(result) != 0:
            self.remove_vehicles()

    def check_toadd(self):
        result = self.query_api.query(self.query.format("toadd"))
        self.toadd = result
        if len(result) != 0:
            self.insert_vehicles()

    def insert_vehicles(self):
        measurement = "toadd"
        for table in self.toadd:
            for record in table.records:
                print("toadd:" + record['_value'])
                print(traci.vehicle.getIDList())
                if record['_value'] not in traci.vehicle.getIDList():
                    traci.vehicle.add(vehID=record['_value'], routeID=random.choice(traci.route.getIDList()), depart=traci.simulation.getTime())
        self.delete_api.delete(start=self.start_time, stop=self.end_time,predicate='_measurement="{}"'.format(measurement), bucket="db", org="ERENA")

    def remove_vehicles(self):
        measurement = "toremove"
        for table in self.toremove:
            for record in table.records:
                print("toremove:" + record['_value'])
                print(traci.vehicle.getIDList())
                if record['_value'] in traci.vehicle.getIDList():
                    traci.vehicle.remove(vehID=record['_value'])
        self.delete_api.delete(start=self.start_time, stop=self.end_time, predicate='_measurement="{}"'.format(measurement), bucket="db", org="ERENA")

