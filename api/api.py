from datetime import datetime

from flask import Flask, request, jsonify
from influxdb_client import InfluxDBClient, Point


class SumoAPI:
    def __init__(self):
        self.cars = []
        self.app = Flask(__name__)
        self.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
        with InfluxDBClient.from_config_file("../app/creds.toml") as self.client:
            self.query_api = self.client.query_api()
            self.write_api = self.client.write_api()

    def get_all_cars(self):
        result = self.query_api.query("""
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
        print("OK")

    def get_cars_list(self):
        pass


sumo_api = SumoAPI()


@sumo_api.app.route('/cars', methods=['GET'])
def get_all_cars():
    cars = sumo_api.get_all_cars()
    return cars


@sumo_api.app.route('/cars/<vehicle>', methods=['GET'])
def get_car(vehicle):
    car = sumo_api.get_car(vehicle)
    return car


@sumo_api.app.route('/cars/<vehicle>', methods=['POST'])
def add_car(vehicle):
    sumo_api.add_car(vehicle)
    return f"Car {vehicle} added"


if __name__ == '__main__':
    sumo_api.app.run()
