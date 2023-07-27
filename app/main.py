import traci
import random
from launcher import Launcher
from updatedb import UpdateDB
from editor import Editor


def main():
    Launcher(200)  # delay en parametre en ms
    UpdateDB(1000)  # insertion information des véhicules dans influxdb
    Editor(1000)

    # # vehicle_test = Vehicle(1, "U6", "car")
    # depart_time = traci.simulation.getTime()
    # r_route = random.choice(traci.route.getIDList())
    # print(r_route)


if __name__ == "__main__":
    main()
