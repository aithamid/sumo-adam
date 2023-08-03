## Introduction

Welcome to ADAM - API for Data-driven Autonomous Mobility!

The primary objective of this project is to create a REST API that facilitates data retrieval for each vehicle. ADAM has been developed to support the NOMA Project at the Gustave Eiffel University laboratory ERENA. The API is designed to provide essential functionalities required for our research and is implemented primarily in Python due to its popularity and suitability for research applications. For seamless execution, the project is containerized using Docker-compose, ensuring a smooth deployment process while mitigating potential library conflicts.

## Architecture

The ADAM project consists of four main components:

1. **InfluxDB Container**: This container houses the database where vehicle data is stored.
2. **Sumo Container**: This container manages the Sumo simulation environment, which includes tasks like launching Sumo, editing scenarios by adding or removing vehicles, and updating the database with relevant information.
3. **API Container**: The core of ADAM, this container hosts the REST API developed using Flask. It enables users to interact with the data and perform various operations.
4. **Client**: The client interacts with the API, and for this purpose, Postman is used to facilitate testing and validation.

## Running the Project

To run the ADAM project, follow these steps:

1. Build the containers using the command: `docker-compose build`.
2. Start the containers using: `docker-compose up`.
3. Once the containers are up and running, you can access the API through Postman by navigating to [http://127.0.0.1:5000](http://127.0.0.1:5000/).

To run the ADAM project without using `docker-compose`, you can follow these steps:

1. Build and run the InfluxDB container:

```bash
docker run -d -p 8086:8086 --name=influxdb \
-e DOCKER_INFLUXDB_INIT_MODE=setup \
-e DOCKER_INFLUXDB_INIT_ORG=ERENA \
-e DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=I5Iyui0V6B-MLOX9Hm_GlcvC7ZqJVTMDF04fqfFsgDQjniavDldsZ4jhtfBOKKwi1l4ACjBarQXvDEFrYYZ6CQ== \
-e DOCKER_INFLUXDB_INIT_BUCKET=db \
-e DOCKER_INFLUXDB_INIT_USERNAME=erena \
-e DOCKER_INFLUXDB_INIT_PASSWORD=erena123 \
-v ./influxdb:/var/lib/influxdb influxdb
```

2. Run the Sumo program `main.py`:

```bash
python3 core.py
```

3. Run the Flask API `api.py`:

```bash
python3 api.py
```

With these steps, you should have InfluxDB, Sumo, and the ADAM API running on your system. You can now access the API endpoints using Postman or any other HTTP client.

Remember to install the required dependencies before running the `core.py` and `api.py` scripts by running the following command inside the respective directories:

```bash
pip3 install -r requirements.txt
```

Make sure you have Python, Docker, and Sumo installed on your system before proceeding with these steps. Additionally, ensure that the necessary configurations are set up correctly, such as the database initialization parameters for InfluxDB and the API endpoints in the Flask application.

## Documentation

### Sumo

```python
def start_simulation(self):
        print("enter")
        self.run = True
        self.launcher = Launcher(state=self.state, delay=self.data["delay"], port=int(self.data["port"]))
        self.updatedb = UpdateDB(self.updatedb_delay)
        self.editor = Editor(self.editor_delay)
```

In the `Manager` class, three essential classes are instantiated: `Launcher`, `UpdateDB`, and `Editor`. Each class serves a specific purpose in orchestrating the Sumo simulation environment and managing data updates in the database.

- `Launcher()`: The `Launcher` class is responsible for launching the Sumo simulation with a specified configuration. 

- `UpdateDB(delay)`: The `UpdateDB` class handles the updating of the InfluxDB with vehicle data. The delay of 1000 milliseconds (1 second) indicates that the database will be refreshed every second with the most recent vehicle information. This ensures that the data available in the database remains up-to-date and reflects real-time vehicle movements in the simulation.

- `Editor(delay)`: The `Editor` class manages scenario editing, including adding and removing vehicles in the simulation. With a delay of 1000 milliseconds (1 second), the editor continuously checks the database every second to determine if any modifications have been made to the simulation via the API. This enables real-time responsiveness to user interactions with the simulation, allowing them to make dynamic changes as needed.

By incorporating these delay values, the ADAM project optimizes the simulation execution, database updates, and user interactions, ensuring smooth and concurrent operations.
### API

The API is developed using Flask and provides the following endpoints:

- **GET /cars**: Retrieves all information about the vehicles currently on the road.
- **GET /cars/list**: Retrieves a list of vehicle names currently on the road.
- **GET /cars/vehicle**: Retrieves detailed information about a specific vehicle.
- **POST /cars/vehicle/add**: Adds a new vehicle to the simulation.
- **DELETE /cars/vehicle/remove**: Removes a vehicle from the simulation.

### Postman

For ease of testing, the following endpoints are available in Postman:

#### GET

- [http://127.0.0.1:5000/cars](http://127.0.0.1:5000/cars): To get all the information about the vehicles on the road.
- [http://127.0.0.1:5000/cars/list](http://127.0.0.1:5000/cars/list): To get the list of vehicles on the road (only the names of the vehicles).
- [http://127.0.0.1:5000/cars/nameofvehicle](http://127.0.0.1:5000/cars/nameofvehicle): To get all the information about a specific vehicle.

#### POST

- [http://127.0.0.1:5000/cars/nameofvehicle/add](http://127.0.0.1:5000/cars/nameofvehicle/add): To add a new vehicle to the simulation.
- http://localhost:5000/simulation/start?port=8080&delay=200: To start a new simulation.
- http://localhost:5000/simulation/connect?ip=localhost&port=8813: To connect to an existing simulation.
- http://localhost:5000/simulation/stop: To stop the current simulation.

#### DELETE

- [http://127.0.0.1:5000/cars/nameofvehicle/remove](http://127.0.0.1:5000/cars/nameofvehicle/remove): To remove a vehicle from the simulation.

With this documentation, users can easily interact with the ADAM API and utilize its functionalities for their data-driven autonomous mobility projects.