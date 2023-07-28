import threading
import random
import ast
import time
import traci
from influxdb_client import InfluxDBClient
from sumolib import checkBinary
import json

from app.editor import Editor
from app.launcher import Launcher
from app.updatedb import UpdateDB


class Manager:
    def __init__(self):
        self.delete_api = None
        self.query_api = None
        self.write_api = None
        self.state = None
        self.data = None
        self.run = False
        self.launcher = None
        self.updatedb = None
        self.editor = None
        self.influxdb()
        self.reset_database("sumo")
        self.reset_database("vehicles")
        print("API Launched")
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()

    def loop(self):
        self.reset_database("launcher")
        while True:
            self.manager()

    def manager(self):
        if self.get_last_state():
            if not self.run and self.state == "start":
                self.start_simulation()
            elif not self.run and self.state == "connect":
                self.connect_simulation()
            elif self.run and self.state == "stop":
                self.stop_simulation()
            time.sleep(1)

    def start_simulation(self):
        print("enter")
        self.run = True
        self.launcher = Launcher(state=self.state, delay=self.data["delay"], port=int(self.data["port"]))
        self.updatedb = UpdateDB(1000)
        self.editor = Editor(1000)
        print(self.state)
        print(self.data)

    def connect_simulation(self):
        self.run = True
        self.launcher = Launcher(state=self.state, ip=self.data["ip"], port=int(self.data["port"]))
        self.updatedb = UpdateDB(1000)
        self.editor = Editor(1000)
        if self.launcher.error:
            print("failed")
        print(self.state)
        print(self.data)

    def stop_simulation(self):
        self.run = False
        self.editor.stop()
        self.updatedb.stop()
        self.launcher.stop()
        self.launcher.thread.join()
        launcher = None
        print(self.state)
        print(self.data)

    def get_last_state(self):
        result = self.query_api.query("""
          from(bucket: "db")
    |> range(start: 0)
    |> filter(fn: (r) => r["_measurement"] == "launcher" and (r["_field"] == "data" or r["_field"] == "state"))
    |> last()
    |> keep(columns: ["_time", "_field", "_value"])
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> yield(name: "mean")
          """)
        values = result.to_values()
        values_list = [list(item) for item in values]
        if values_list:
            self.state = values_list[len(values_list) - 1][4]
            self.data = ast.literal_eval(values_list[len(values_list) - 1][3])
            return True
        else:
            self.state = None
            self.data = None
            return False

    def reset_database(self, measurement):
        self.start_time = '1970-01-01T00:00:00Z'
        self.end_time = '2099-12-31T23:59:59Z'
        self.delete_api.delete(start=self.start_time, stop=self.end_time,
                               predicate='_measurement="{}"'.format(measurement), bucket="db", org="ERENA")

    def influxdb(self):
        with InfluxDBClient.from_config_file("creds.toml") as self.client:
            self.query_api = self.client.query_api()
            self.write_api = self.client.write_api()
            self.delete_api = self.client.delete_api()


if __name__ == "__main__":
    Manager()
