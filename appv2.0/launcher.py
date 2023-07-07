import threading
import random

import traci
from sumolib import checkBinary

sumoBinary = checkBinary('sumo-gui')


class Vehicle:
    number_vehicles = 0

    def __init__(self):
        pass


class Launcher:
    def __init__(self, c_delay):
        self.delay = c_delay
        print("Simulation created")
        traci.start(
            [
                sumoBinary,
                '-c', '../sumo/sumo.cfg',
                '--delay', str(self.delay),
                '--start'
            ]
        )
        my_thread = threading.Thread(target=self.start)
        my_thread.start()

    def start(self):
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
        traci.close()

    def update(self):
        pass

    def insert(self):
        pass

    def addVehicle(self, vehicle):
        pass

    def removeVehicle(self, vehicle):
        pass
