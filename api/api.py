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
        self.run = False
        self.ip = None
        self.port = None
        self.delay = None
        with InfluxDBClient.from_config_file("creds.toml") as self.client:
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
            tmp = values_list[len(values_list) - 1][8]
            self.list = ast.literal_eval(tmp)
            print(self.list)
        else:
            print("No data available.")
        return tmp

    def query_builder(self, vehicle=None):
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

    def get_car_manager(self, query):
        if query == -1:
            return """There is no car in activity"""
        elif query == -2:
            return """This car is not car in activity"""
        else:
            result = self.query_api.query(query)
            myjson = result.to_json()
            return myjson

    def get_all_cars(self):
        return self.get_car_manager(self.query_builder())

    def get_car(self, vehicle):
        return self.get_car_manager(self.query_builder(vehicle))

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

    def start_simu(self):
        data = {"port": self.port, "delay": self.delay}
        data_point = Point("launcher") \
            .field("state", "start") \
            .field("data", str(data)) \
            .time(datetime.utcnow())
        self.write_api.write(bucket="db", record=data_point)

    def stop_simu(self):
        data = None
        data_point = Point("launcher") \
            .field("state", "stop") \
            .field("data", str(data)) \
            .time(datetime.utcnow())
        self.write_api.write(bucket="db", record=data_point)

    def connect_simu(self):
        data = {"ip": self.ip, "port": self.port}
        data_point = Point("launcher") \
            .field("state", "connect") \
            .field("data", str(data)) \
            .time(datetime.utcnow())
        self.write_api.write(bucket="db", record=data_point)

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
    sumo_api.get_list_cars()
    if vehicle in sumo_api.list:
        return f"Car {vehicle} is in activity"
    else:
        sumo_api.add_car(vehicle)
        return f"Car {vehicle} added"


@sumo_api.app.route('/cars/<vehicle>/remove', methods=['DELETE'])
def remove_car(vehicle):
    sumo_api.get_list_cars()
    if vehicle not in sumo_api.list:
        return f"Car {vehicle} not founded"
    else:
        sumo_api.remove_car(vehicle)
        return f"Car {vehicle} removed"


@sumo_api.app.route('/simulation/start', methods=['POST'])
def start_simu():
    if sumo_api.run:
        return jsonify({"message": "Simulation already launched."}), 400
    sumo_api.ip = request.args.get('ip')
    sumo_api.port = request.args.get('port')
    sumo_api.delay = request.args.get('delay')

    if not sumo_api.ip or not sumo_api.port or not sumo_api.delay:
        return jsonify({"error": "IP, Port and Delay (in ms) parameters are required."}), 400
    response = {
        "message": f"Simulating start to IP: {sumo_api.ip}, Port: {sumo_api.port} with a delay of {sumo_api.delay}"}
    sumo_api.run = True
    sumo_api.start_simu()
    return jsonify(response), 200


@sumo_api.app.route('/simulation/connect', methods=['POST'])
def connect_simu():
    if sumo_api.run:
        return jsonify({"message": "Simulation already launched."}), 400
    sumo_api.ip = request.args.get('ip')
    sumo_api.port = request.args.get('port')
    if not sumo_api.ip or not sumo_api.port:
        return jsonify({"error": "IP and Port parameters are required."}), 400
    response = {
        "message": f"Simulating connection to IP: {sumo_api.ip}, Port: {sumo_api.port}"}
    sumo_api.run = True
    sumo_api.connect_simu()
    return jsonify(response), 200


@sumo_api.app.route('/simulation/stop', methods=['POST'])
def stop_simu():
    if not sumo_api.run:
        return jsonify({"message": "Simulation already stopped."}), 400
    response = {"message": f"Simulation IP: {sumo_api.ip}, Port: {sumo_api.port} stopped"}
    sumo_api.run = False
    sumo_api.stop_simu()
    return jsonify(response), 200


if __name__ == '__main__':
    sumo_api.app.run()
