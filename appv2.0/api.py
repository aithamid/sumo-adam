from flask import Flask, request

app = Flask(__name__)


class SumoAPI:
    def __init__(self):
        self.cars = []

    def get_all_cars(self):
        # TODO: Implémentez la logique pour récupérer les données de toutes les voitures
        pass

    def get_car(self, vehicle):
        # TODO: Implémentez la logique pour récupérer les données d'une seule voiture
        pass

    def add_car(self):
        # TODO: Implémentez la logique pour ajouter une voiture
        pass


sumo_api = SumoAPI()


@app.route('/cars', methods=['GET'])
def get_all_cars():
    cars = sumo_api.get_all_cars()
    # TODO: Convertissez les données des voitures en une réponse JSON
    return "GET all cars"


@app.route('/cars/<vehicle>', methods=['GET'])
def get_car(vehicle):
    car = sumo_api.get_car(vehicle)
    # TODO: Convertissez les données de la voiture en une réponse JSON
    return f"GET car: {vehicle}"


@app.route('/cars/<vehicle>', methods=['POST'])
def add_car(vehicle):
    # TODO: Récupérez les données de la voiture depuis la requête POST
    sumo_api.add_car()
    return f"Car {vehicle} added"


if __name__ == '__main__':
    app.run()
