import traci

def main():
    remote_host = 'localhost'
    port = 51845  # Le port sur lequel SUMO écoute pour les connexions TraCI

    # Se connecter au simulateur SUMO distant
    traci.connect(host=remote_host)

    # Exemple d'utilisation de TraCI pour récupérer la position d'un véhicule
    vehicle_id = 'veh1'
    position = traci.vehicle.getPosition(vehicle_id)
    print(f"Position du véhicule {vehicle_id} : {position}")

    # Fermer la connexion TraCI
    traci.close()


if __name__ == "__main__":
    main()