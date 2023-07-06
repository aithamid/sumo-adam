import traci
import time

host = '127.0.0.1'  # Remplacez par l'adresse IP de l'ordinateur hôte
port = 8813  # Remplacez par le port sur lequel SUMO est en écoute

# Connexion à l'ordinateur hôte où la simulation SUMO est en cours d'exécution
traci.init(port)

time_step = 0.005

# Main simulation loop
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

    # Perform control actions as needed

    # Slow down the simulation speed by adding a delay
    time.sleep(time_step)

# Terminate the TraCI connection
traci.close()
