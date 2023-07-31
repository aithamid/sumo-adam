import ast
import json
from datetime import datetime

from flask import Flask, request, jsonify
from influxdb_client import InfluxDBClient, Point


class CarService:
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

    def get_car_manager(self, query):
        """This method will take a "query" as parameter
            Return a json."""
        if query == -1:
            return """There is no car in activity"""
        elif query == -2:
            return """This car is not car in activity"""
        else:
            result = self.query_api.query(query)
            myjson = result.to_json()
            return myjson

    def get_all_cars(self):
        """This method will return information for all the cars that are active
                                        """
        return self.get_car_manager(self.query_builder())

    def get_car(self, vehicle):
        """This method will return information about a car in JSON format
                                        """
        return self.get_car_manager(self.query_builder(vehicle))

    def query_builder(self, vehicle=None):
        """This method build queries for influx database,
                if you add the "vehicle" parameter it builds a query to get info about a specific vehicle.
                if you don't, it returns a query to get all the information about all vehicles
        """
        self.get_list_cars()
        condition = ""
        vehicle_condition = ""

        # build the condition where he displays only vehicle
        if len(self.list) > 1:
            condition = "|> filter(fn: (r) => "
            for i, car in enumerate(self.list):
                if i == len(self.list) - 1:
                    condition = condition + f"""r["vehicle_id"] == "{car}" """
                else:
                    condition = condition + f"""r["vehicle_id"] == "{car}" or """
            condition = condition + ")"
            query = f"""
                                        from(bucket: "db")
                                              |> range(start: 0)
                                              |> filter(fn: (r) => r["_measurement"] == "sumo")
                                              |> filter(fn: (r) => r["_field"] == "co2" or r["_field"] == "latitude" or r["_field"] == "longitude" or r["_field"] == "speed" or  r["_field"] == "simu_id")
                                              {condition}
                                              """
            print(condition)

        else:
            return -1

        # build the unique vehicle condition
        if vehicle is not None:
            if vehicle in self.list:
                vehicle_condition = f"""|> filter(fn: (r) => r["vehicle_id"] == "{vehicle}")"""
                query = query + f"""{vehicle_condition}
                """
            else:
                return -2

        query = query + """       |> group(columns: ["_field",  "vehicle_id"])
                                  |> last()
                                  |> pivot(rowKey:["_time"], columnKey:["_field"], valueColumn:"_value")
                                  |> yield(name: "last_result")
            """
        return query
