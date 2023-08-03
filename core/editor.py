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
        self.run = True
        self.query = """from(bucket: "db")
        |> range(start: 0)
        |> filter(fn: (r) => r["_measurement"] == "{}")
        |> filter(fn: (r) => r["_field"] == "vehicle_id")
        |> yield(name: "mean")
                      """

        self.influxdb()

        self.reset_data()

        self.thread = threading.Thread(target=self.loop)
        self.thread.start()

    def reset_data(self):
        """
        This method will reset all the data to make sure that the program will take only the decision that are made during the simulation.
        :return:
        """
        self.delete_api.delete(start=self.start_time, stop=self.end_time,
                               predicate='_measurement="{}"'.format("toadd"), bucket="db", org="ERENA")
        self.delete_api.delete(start=self.start_time, stop=self.end_time,
                               predicate='_measurement="{}"'.format("toremove"), bucket="db", org="ERENA")

    def influxdb(self):
        """
        This method will connect to the influx database thanks to creds.toml and gonna prepare API for get, write and remove data.
        :return:
        """
        with InfluxDBClient.from_config_file("../core/creds.toml") as self.client:
            self.query_api = self.client.query_api()
            self.write_api = self.client.write_api()
            self.delete_api = self.client.delete_api()

    def loop(self):
        while self.run and traci.simulation.getMinExpectedNumber() > 0:
            self.check_toadd()
            self.check_toremove()
            time.sleep(self.delay / 1000)

    def check_toremove(self):
        """This method will check if there is a car to remove from the cars that are in activity"""
        result = self.query_api.query(self.query.format("toremove"))
        self.toremove = result
        if len(result) != 0:
            self.remove_vehicles()

    def check_toadd(self):
        """This method will check if there is a car to add"""
        result = self.query_api.query(self.query.format("toadd"))
        self.toadd = result
        if len(result) != 0:
            self.insert_vehicles()

    def insert_vehicles(self):
        """This method will read self.toadd all the vehicles to add and will add it with thanks to
        'traci.vehicle.add'"""
        measurement = "toadd"
        for table in self.toadd:
            for record in table.records:
                print("toadd:" + record['_value'])
                print(traci.vehicle.getIDList())
                if record['_value'] not in traci.vehicle.getIDList():
                    traci.vehicle.add(vehID=record['_value'], routeID=random.choice(traci.route.getIDList()), depart=traci.simulation.getTime())
        self.delete_api.delete(start=self.start_time, stop=self.end_time,predicate='_measurement="{}"'.format(measurement), bucket="db", org="ERENA")

    def remove_vehicles(self):
        """This method will read self.toremove all the vehicles to remove and will add thanks to
        'traci.vehicle.remove'"""
        measurement = "toremove"
        for table in self.toremove:
            for record in table.records:
                print("toremove:" + record['_value'])
                print(traci.vehicle.getIDList())
                if record['_value'] in traci.vehicle.getIDList():
                    traci.vehicle.remove(vehID=record['_value'])
        self.delete_api.delete(start=self.start_time, stop=self.end_time, predicate='_measurement="{}"'.format(measurement), bucket="db", org="ERENA")

    def stop(self):
        self.run = False
        self.thread.join()