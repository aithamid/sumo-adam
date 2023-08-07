from flask import Blueprint, jsonify, request
from api.services.edit_service import EditService

edits_bp = Blueprint('edits', __name__)
edit_service = EditService()


@edits_bp.route('/cars/list', methods=['GET'])
def get_list_cars():
    """
    When the user make /cars/list with GET. This function will check in the database the list of cars that are active.
    :return: Tuple
    """
    edit_service.list = edit_service.get_list_cars()
    return f"List {edit_service.list}"


@edits_bp.route('/cars/<vehicle>/add', methods=['POST'])
def add_car(vehicle):
    """
    This function will add a vehicle in the sumo simulation
    :param vehicle:
    :return:
    """
    edit_service.get_list_cars()
    if vehicle in edit_service.list:
        return f"Car {vehicle} is in activity"
    else:
        edit_service.add_car(vehicle)
        return f"Car {vehicle} added"


@edits_bp.route('/cars/<vehicle>/remove', methods=['DELETE'])
def remove_car(vehicle):
    """
    This function will remove a vehicle in the sumo simulation
    :param vehicle:
    :return:
    """
    edit_service.get_list_cars()
    if vehicle not in edit_service.list:
        return f"Car {vehicle} not founded"
    else:
        edit_service.remove_car(vehicle)
        return f"Car {vehicle} removed"
