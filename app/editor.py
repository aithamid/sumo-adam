import threading

import traci
from influxdb_client import InfluxDBClient, Point


class Editor:
    def __init__(self):
        self.points = None
        with InfluxDBClient.from_config_file("../app/creds.toml") as self.client:
            self.query_api = self.client.query_api()
            self.write_api = self.client.write_api()
        my_thread = threading.Thread(target=self.loop)
        my_thread.start()

    def loop(self):
        while traci.simulation.getMinExpectedNumber() > 0:
            self.check_too_add()
        traci.close()

    def check_too_add(self):
        result = self.query_api.query("""
                                  from(bucket: "db")
        |> range(start: 0)
        |> filter(fn: (r) => r["_measurement"] == "toadd")
        |> filter(fn: (r) => r["_field"] == "vehicle_id")
        |> yield(name: "mean")
                      """)
        self.points = result.get_points()
        if len(result) != 0:
            self.insert_vehicles(result.get_points())

    def insert_vehicles(self):
        for point in self.points:
            # traci.vehicle.add()
            print(point["vehicle_id"])
            self.client.delete_points([point])