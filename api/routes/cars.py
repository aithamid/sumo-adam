from flask import Blueprint, jsonify, request
from api.services.car_service import CarService

cars_bp = Blueprint('cars', __name__)
car_service = CarService()


@cars_bp.route('/cars', methods=['GET'])
def get_all_cars():
    """
    When the user make /cars with GET. This function will check in the database the last infos about the cars that are active.
    :return: JSON File with all vehicles infos
    """
    cars = car_service.get_all_cars()
    return cars


@cars_bp.route('/cars/list', methods=['GET'])
def get_list_cars():
    """
    When the user make /cars/list with GET. This function will check in the database the list of cars that are active.
    :return: Tuple
    """
    car_service.list = car_service.get_list_cars()
    return f"List {car_service.list}"


@cars_bp.route('/cars/<vehicle>', methods=['GET'])
def get_car(vehicle):
    """
    When the user make /cars/nameofvehicle with GET. This function will check in the database the last infos about
    the car that you put in parameter.
    :param vehicle
    :return: JSON File with all vehicles infos
    """
    car = car_service.get_car(vehicle)
    return car
