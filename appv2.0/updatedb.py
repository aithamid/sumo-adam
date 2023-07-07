import threading
import time
import traci


class UpdateDB:
    def __init__(self, c_delay):
        self.delay = c_delay
        my_thread = threading.Thread(target=self.update)
        my_thread.start()

    def update(self):
        while traci.simulation.getMinExpectedNumber() > 0:
            print("ça marche")
            time.sleep(self.delay / 1000)
        traci.close()
