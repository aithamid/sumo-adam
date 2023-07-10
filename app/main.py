import traci
import random
from launcher import Launcher
from updatedb import UpdateDB

def main():
    new_simulation = Launcher(200) # delay en parametre en ms
    UpdateDB(1000) # insertion information des véhicules dans influxdb


    # vehicle_test = Vehicle(1, "U6", "car")
    depart_time = traci.simulation.getTime()
    routelist = traci.route.getIDList()
    r_route = random.choice(routelist)
    print(r_route)


if __name__ == "__main__":
    main()
