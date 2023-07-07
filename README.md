# ADAM - API for Data-driven Autonomous Mobility

ADAM is an API (Application Programming Interface) designed for Data-driven Autonomous Mobility. It provides a platform for integrating data-driven solutions into autonomous vehicles. This README file provides an overview of the ADAM project, its structure, and instructions on how to launch and use the API using SUMO and Docker Compose.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
  - [Using Docker Compose](#using-docker-compose)
  - [Without Docker Compose](#without-docker-compose)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Introduction

ADAM aims to facilitate the integration of data-driven algorithms and models into autonomous vehicles. It provides a robust and flexible API that enables developers to interact with autonomous systems, retrieve vehicle data, and execute various operations related to autonomous mobility.

## Features

- Access vehicle data: Retrieve data from sensors, GPS, accelerometers, etc.
- Execute autonomous operations: Control vehicle movements, navigate routes, etc.
- Data-driven algorithms integration: Incorporate machine learning models, AI algorithms, etc.
- Real-time updates: Receive live data updates from vehicles.
- Logging and analytics: Capture and analyze vehicle data for further insights.

## Installation

### Using Docker Compose

To install and set up the ADAM API with SUMO using Docker Compose, follow these steps:

1. Clone the ADAM repository from GitHub:

   ```shell
   git clone https://github.com/username/ADAM.git
   ```

2. Change to the project directory:

   ```shell
   cd ADAM
   ```

3. Update the necessary configurations in the `docker-compose.yml` file, such as ports, volumes, etc.

4. Build and launch the ADAM API with SUMO using Docker Compose:

   ```shell
   docker-compose up -d
   ```

   The API will be accessible at `http://localhost:5000`.

### Without Docker Compose

To install and set up the ADAM API without using Docker Compose, follow these steps:

1. Clone the ADAM repository from GitHub:

   ```shell
   git clone https://github.com/username/ADAM.git
   ```

2. Change to the project directory:

   ```shell
   cd ADAM
   ```

3. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

4. Install SUMO (Simulation of Urban MObility) following the official SUMO installation instructions for your operating system.

5. Launch SUMO and import the necessary road network and simulation files.

6. Configure the API settings, such as SUMO connection details and database connection details, in the `config.py` file.

7. Launch the ADAM API:

   ```shell
   python app.py
   ```

   The API will be accessible at `http://localhost:5000`.

## Usage

To use the ADAM API, you can interact with its various endpoints using HTTP requests. You can integrate the API into your own applications or use tools like Postman to test and explore the available endpoints.

Ensure that the ADAM API and SUMO are running before making requests.

## API Endpoints

The ADAM API exposes the following endpoints:

- `GET /vehicles`: Retrieve data for all vehicles.
- `GET /vehicles/{id}`: Retrieve data for a specific vehicle.
- `POST /vehicles`: Add a new vehicle to the system.
- `PUT /vehicles/{id}`: Update the information of a specific vehicle.
- `DELETE /vehicles/{id}`: Remove a vehicle from the system.

Please refer to the API documentation or the source code for more details on the available endpoints, their request/response formats, and any additional parameters.

## Contributing

Contributions to the ADAM project are welcome! If you encounter any issues, have suggestions for improvements, or would like to contribute new features, please open an issue or submit a pull request on the project's GitHub repository.

## License

The ADAM project is licensed under the MIT License. Please see the [LICENSE](LICENSE) file for more details.

Feel free to update the sections and content as needed to reflect the specific details and structure of your ADAM project, including the integration with SUMO and Docker Compose.