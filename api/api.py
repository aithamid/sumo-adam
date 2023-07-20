import ast
import json
from datetime import datetime

from flask import Flask, request, jsonify
from influxdb_client import InfluxDBClient, Point


class SumoAPI:
    def __init__(self):
        self.cars = []
        self.app = Flask(__name__)
        self.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
        self.list = None
        with InfluxDBClient.from_config_file("../app/creds.toml") as self.client:
            self.query_api = self.client.query_api()
            self.write_api = self.client.write_api()

    def get_list_cars(self):
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
            tmp = values_list[0][8]
            self.list = ast.literal_eval(tmp)
            print(self.list)
        else:
            print("No data available.")
        return tmp

    def get_all_cars(self):
        self.get_list_cars()
        condition = ""
        for car in self.list:
            condition = condition + f"""r["vehicle_id"] == "{car}" or """
        print(condition)
        result = self.query_api.query(f"""
                            from(bucket: "db")
                                  |> range(start: 0)
                                  |> filter(fn: (r) => r["_measurement"] == "sumo")
                                  |> filter(fn: (r) => r["_field"] == "co2" or r["_field"] == "latitude" or r["_field"] == "longitude" or r["_field"] == "speed" or  r["_field"] == "simu_id")
                                  |> group(columns: ["_field",  "vehicle_id"])
                                  |> last()
                                  |> pivot(rowKey:["_time"], columnKey:["_field"], valueColumn:"_value")
                                  |> yield(name: "last_result")
            """)
        myjson = result.to_json()
        return myjson

    def get_car(self, vehicle):
        result = self.query_api.query(f"""
                        from(bucket: "db")
                              |> range(start: 0)
                              |> filter(fn: (r) => r["_measurement"] == "sumo")
                              |> filter(fn: (r) => r["_field"] == "co2" or r["_field"] == "latitude" or r["_field"] == "longitude" or r["_field"] == "speed" or  r["_field"] == "simu_id")
                              |> group(columns: ["_field",  "vehicle_id"])
                              |> last()
                              |> filter(fn: (r) => r["vehicle_id"] == "{vehicle}")
                              |> pivot(rowKey:["_time"], columnKey:["_field"], valueColumn:"_value")
                              |> yield(name: "last_result")
                    """)
        myjson = result.to_json()
        return myjson

    def add_car(self, vehicle):
        data_point = Point("toadd") \
            .field("vehicle_id", vehicle) \
            .time(datetime.utcnow())
        self.write_api.write(bucket="db", record=data_point)

    def remove_car(self, vehicle):
        data_point = Point("toremove") \
            .field("vehicle_id", vehicle) \
            .time(datetime.utcnow())
        self.write_api.write(bucket="db", record=data_point)

    def get_cars_list(self):
        pass


sumo_api = SumoAPI()


@sumo_api.app.route('/cars', methods=['GET'])
def get_all_cars():
    cars = sumo_api.get_all_cars()
    return cars


@sumo_api.app.route('/cars/list', methods=['GET'])
def get_list_cars():
    sumo_api.list = sumo_api.get_list_cars()
    return f"List {sumo_api.list}"


@sumo_api.app.route('/cars/<vehicle>', methods=['GET'])
def get_car(vehicle):
    car = sumo_api.get_car(vehicle)
    return car


@sumo_api.app.route('/cars/<vehicle>/add', methods=['POST'])
def add_car(vehicle):
    sumo_api.add_car(vehicle)
    return f"Car {vehicle} added"


@sumo_api.app.route('/cars/<vehicle>/remove', methods=['DELETE'])
def remove_car(vehicle):
    sumo_api.remove_car(vehicle)
    return f"Car {vehicle} removed"


if __name__ == '__main__':
    sumo_api.app.run()
