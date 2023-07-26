import traci

def connect_to_sumo():
    try:
        traci.init(port=8813)
        traci.simulationStep()

        # Your TraCI client 1 logic here

        traci.close()
    except Exception as e:
        print(f"Error connecting to SUMO: {e}")

if __name__ == "__main__":
    connect_to_sumo()
