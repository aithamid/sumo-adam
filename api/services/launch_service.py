import ast
import json
from datetime import datetime

from flask import Flask, request, jsonify
from influxdb_client import InfluxDBClient, Point


class LaunchService:
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

    def start_simu(self):
        """This method will send to the database that the user want to start a new simulation
                        """
        data = {"port": self.port, "delay": self.delay}
        data_point = Point("launcher") \
            .field("state", "start") \
            .field("data", str(data)) \
            .time(datetime.utcnow())
        self.write_api.write(bucket="db", record=data_point)

    def stop_simu(self):
        """This method will send to the database that the user want to stop simulation
                        """
        data = None
        data_point = Point("launcher") \
            .field("state", "stop") \
            .field("data", str(data)) \
            .time(datetime.utcnow())
        self.write_api.write(bucket="db", record=data_point)

    def connect_simu(self):
        """This method will send to the database that the user want to connect to an existing simulation
                """
        data = {"ip": self.ip, "port": self.port}
        data_point = Point("launcher") \
            .field("state", "connect") \
            .field("data", str(data)) \
            .time(datetime.utcnow())
        self.write_api.write(bucket="db", record=data_point)