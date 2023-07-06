import subprocess
import time

# Launch the SUMO simulation on the host computer
sumo_cmd = ["sumo-gui", "-c", "sumo/sumo.cfg", "--remote-port", "8813", "--start"]
sumo_proc = subprocess.Popen(sumo_cmd)

# Wait for the simulation to start
# You can adjust the delay time as needed
# This gives enough time for SUMO to initialize
time.sleep(5)

# The simulation is running on the host computer
# and can be controlled remotely

# Keep the script running
input("Press Enter to exit...")

# Terminate the SUMO process
sumo_proc.terminate()