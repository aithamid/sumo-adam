import threading
import random
import ast
import time
import traci
from influxdb_client import InfluxDBClient
from sumolib import checkBinary
import json

from app.launcher import Launcher

class Manager:
    def __init__(self):
        self.state = None
        self.data = None
        self.run = False
        with InfluxDBClient.from_config_file("creds.toml") as self.client:
            self.query_api = self.client.query_api()
            self.write_api = self.client.write_api()
            self.delete_api = self.client.delete_api()
        self.start_time = '1970-01-01T00:00:00Z'
        self.end_time = '2099-12-31T23:59:59Z'
        self.port = 51845
        print("API Launched")
        self.thread = threading.Thread(target=self.start)
        self.thread.start()

    def start(self):
        self.reset_database()
        launcher = None
        while True:
            if self.get_last_state():
                if not self.run and self.state == "start":
                    print("enter")
                    self.run = True
                    launcher = Launcher(state=self.state, delay=self.data["delay"], port=int(self.data["port"]))
                    print(self.state)
                    print(self.data)
                elif not self.run and self.state == "connect":
                    self.run = True
                    launcher = Launcher(state=self.state, ip=self.data["ip"], port=int(self.data["port"]))
                    if launcher.error:
                        print("failed")
                    print(self.state)
                    print(self.data)
                elif self.run and self.state == "stop":
                    self.run = False
                    launcher.stop()
                    launcher.thread.join()
                    launcher = None
                    print(self.state)
                    print(self.data)


                time.sleep(1)
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

    def reset_database(self):
        self.delete_api.delete(start=self.start_time, stop=self.end_time,
                               predicate='_measurement="{}"'.format("launcher"), bucket="db", org="ERENA")

if __name__ == "__main__":
    Manager()
