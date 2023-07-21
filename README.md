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
3. Once the containers are up and running, you can access the API through Postman by navigating to [http://localhost:5000](http://localhost:5000/).

## Documentation

### Sumo

The main program [`main.py`](http://main.py) orchestrates three essential classes:

- `Launcher` from `launcher.py`: Responsible for launching Sumo simulation with a specified configuration delay.
- `UpdateDB` from `updatedb.py`: Handles the updating of the InfluxDB with vehicle data at a configurable delay.
- `Editor` from `editor.py`: Manages scenario editing, including adding and removing vehicles in the simulation at a configurable delay.

Each function call within the program creates a thread to ensure efficient and concurrent execution.

```python
def main():
    Launcher(200)  
    UpdateDB(1000) 
    Editor(1000)
```

### API

The API is developed using Flask and provides the following endpoints:

- **GET /cars**: Retrieves all information about the vehicles currently on the road.
- **GET /cars/list**: Retrieves a list of vehicle names currently on the road.
- **GET /cars/<vehicle>**: Retrieves detailed information about a specific vehicle.
- **POST /cars/<vehicle>/add**: Adds a new vehicle to the simulation.
- **DELETE /cars/<vehicle>/remove**: Removes a vehicle from the simulation.

### Postman

For ease of testing, the following endpoints are available in Postman:

#### GET

- [http://localhost:5000/cars](http://localhost:5000/cars): To get all the information about the vehicles on the road.
- [http://localhost:5000/cars/list](http://localhost:5000/cars/list): To get the list of vehicles on the road (only the names of the vehicles).
- [http://localhost:5000/cars/nameofvehicle](http://localhost:5000/cars/nameofvehicle): To get all the information about a specific vehicle.

#### POST

- [http://localhost:5000/cars/nameofvehicle/add](http://localhost:5000/cars/nameofvehicle/add): To add a new vehicle to the simulation.

#### DELETE

- [http://localhost:5000/cars/nameofvehicle/remove](http://localhost:5000/cars/nameofvehicle/remove): To remove a vehicle from the simulation.

With this documentation, users can easily interact with the ADAM API and utilize its functionalities for their data-driven autonomous mobility projects.