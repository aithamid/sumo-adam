from sumolib import checkBinary
import traci
from influxdb_client import InfluxDBClient, Point
from datetime import datetime
import time

sumoBinary = checkBinary('sumo-gui')

WHITE = [255, 255, 255]
EDGE_ID = 'closed'
VEHICLES = ['1', '4', '8']
token = "hHSXQ4ARF4YYcQcDHaqZWZzjtGerYEmj0PK_yaV03yHcuiCP9o01MOdU2MrU36YUMrTcsOnG5QWIpfyF1AJ98g=="
org = "ERENA"
url = "http://localhost:8086"
bucket = "db"


def main():
    startSim()
    i = 0

    while shouldContinueSim():
        for vehId in getOurDeparted(VEHICLES):
            setVehColor(vehId, WHITE)
            avoidEdge(vehId, EDGE_ID)
        for vehId in traci.vehicle.getIDList():
            position = traci.vehicle.getPosition(vehId)
            x, y = traci.vehicle.getPosition(vehId)
            speed = traci.vehicle.getSpeed(vehId)
            lon,lat = traci.simulation.convertGeo(x,y)
            co2_emission = traci.vehicle.getCO2Emission(vehId)
            print("CO2 Emission:", co2_emission)
            print("Position ID[{}] : ({}, {})".format(vehId,x, y))
            print("Speed ID[{}] : {} m/s".format(vehId, speed))
            print("Longitude:", lon)
            print("Latitude:", lat)
            client = InfluxDBClient(url=url, token=token)

            # Create a new data point with tags
            data_point = Point("sumo") \
                .tag("vehicle_id", vehId) \
                .tag("simu_id", "1") \
                .tag("iteration_id", i) \
                .field("value", 25.5) \
                .field("longitude", lon) \
                .field("latitude", lat) \
                .field("co2", co2_emission) \
                .field("speed", speed) \
                .time(datetime.utcnow())

            # Write the data point to InfluxDB
            client.write_api().write(bucket=bucket, org=org, record=data_point)
        i = i + 1
        print(i)
        traci.simulationStep()
    traci.close()


def startSim():
    """Starts the simulation."""
    traci.start(
        [
            sumoBinary,
            '-c', 'network/network.sumocfg',
            '--delay', '200',
            '--start'

        ])


def shouldContinueSim():
    """Checks that the simulation should continue running.
    Returns:
        bool: `True` if vehicles exist on network. `False` otherwise.
    """
    numVehicles = traci.simulation.getMinExpectedNumber()
    return True if numVehicles > 0 else False


def setVehColor(vehId, color):
    """Changes a vehicle's color.
    Args:
        vehId (String): The vehicle to color.
        color ([Int, Int, Int]): The RGB color to apply.
    """
    traci.vehicle.setColor(vehId, color)


def avoidEdge(vehId, edgeId):
    """Sets an edge's travel time for a vehicle infinitely high, and reroutes the vehicle based on travel time.
    Args:
        vehId (Str): The ID of the vehicle to reroute.
        edgeId (Str): The ID of the edge to avoid.
    """
    traci.vehicle.setAdaptedTraveltime(
        vehId, edgeId, float('inf'))
    traci.vehicle.rerouteTraveltime(vehId)


def getOurDeparted(filterIds=[]):
    """Returns a set of filtered vehicle IDs that departed onto the network during this simulation step.
    Args:
        filterIds ([String]): The set of vehicle IDs to filter for.
    Returns:
        [String]: A set of vehicle IDs.
    """
    newlyDepartedIds = traci.simulation.getDepartedIDList()
    filteredDepartedIds = newlyDepartedIds if len(
        filterIds) == 0 else set(newlyDepartedIds).intersection(filterIds)
    return filteredDepartedIds


if __name__ == "__main__":
    main()
