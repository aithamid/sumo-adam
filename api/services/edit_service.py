import ast
import json
from datetime import datetime

from flask import Flask, request, jsonify
from influxdb_client import InfluxDBClient, Point


class EditService:
    def __init__(self):
        self.cars = []
        self.list = None
        self.run = False
        self.ip = None
        self.port = None
        self.delay = None
        with InfluxDBClient.from_config_file("creds.toml") as self.client:
            self.query_api = self.client.query_api()
            self.write_api = self.client.write_api()

    def get_list_cars(self):
        """This method return a tuple of cars that are in activity."""
        result = self.query_api.query("""
        from(bucket: "db")
              |> range(start: 0)
              |> filter(fn: (r) => r["_measurement"] == "vehicles")
              |> filter(fn: (r) => r["_field"] == "test")
              |> last()
              |> yield(name: "mean")
        """)
        values = result.to_values()
        values_list = [list(item) for item in values]
        if values_list:
            tmp = values_list[len(values_list) - 1][8]
            self.list = ast.literal_eval(tmp)
            print(self.list)
        else:
            print("No data available.")
        return tmp

    def add_car(self, vehicle):
        """This method will send to the database that the user want to add a car
                                        """
        data_point = Point("toadd") \
            .field("vehicle_id", vehicle) \
            .time(datetime.utcnow())
        self.write_api.write(bucket="db", record=data_point)

    def remove_car(self, vehicle):
        """This method will send to the database that the user want to remove a car
                                """
        data_point = Point("toremove") \
            .field("vehicle_id", vehicle) \
            .time(datetime.utcnow())
        self.write_api.write(bucket="db", record=data_point)
