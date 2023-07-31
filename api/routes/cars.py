from flask import Blueprint, jsonify, request
from api.services.car_service import CarService

cars_bp = Blueprint('cars', __name__)
car_service = CarService()


@cars_bp.route('/cars', methods=['GET'])
def get_all_cars():
    cars = car_service.get_all_cars()
    return cars


@cars_bp.route('/cars/list', methods=['GET'])
def get_list_cars():
    car_service.list = car_service.get_list_cars()
    return f"List {car_service.list}"


@cars_bp.route('/cars/<vehicle>', methods=['GET'])
def get_car(vehicle):
    car = car_service.get_car(vehicle)
    return car
