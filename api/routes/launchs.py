from flask import Blueprint, jsonify, request
from api.services.launch_service import LaunchService

launchs_bp = Blueprint('launchs', __name__)
launch_service = LaunchService()


@launchs_bp.route('/simulation/start', methods=['POST'])
def start_simu():
    """
        This function will start a new sumo simulation
        """
    if launch_service.run:
        return jsonify({"message": "Simulation already launched."}), 400
    launch_service.port = request.args.get('port')
    launch_service.delay = request.args.get('delay')

    if not launch_service.port or not launch_service.delay:
        return jsonify({"error": "IP, Port and Delay (in ms) parameters are required."}), 400
    response = {
        "message": f"Simulating start to IP: {launch_service.ip}, Port: {launch_service.port} with a delay of {launch_service.delay}"}
    launch_service.run = True
    launch_service.start_simu()
    return jsonify(response), 200


@launchs_bp.route('/simulation/connect', methods=['POST'])
def connect_simu():
    """
    This function will connect the program to the sumo simulation
    """
    if launch_service.run:
        return jsonify({"message": "Simulation already launched."}), 400
    launch_service.ip = request.args.get('ip')
    launch_service.port = request.args.get('port')
    if not launch_service.ip or not launch_service.port:
        return jsonify({"error": "IP and Port parameters are required."}), 400
    response = {
        "message": f"Simulating connection to IP: {launch_service.ip}, Port: {launch_service.port}"}
    launch_service.run = True
    launch_service.connect_simu()
    return jsonify(response), 200


@launchs_bp.route('/simulation/stop', methods=['POST'])
def stop_simu():
    """
        This function will stop the running sumo simulation
        """
    if not launch_service.run:
        return jsonify({"message": "Simulation already stopped."}), 400
    response = {"message": f"Simulation IP: {launch_service.ip}, Port: {launch_service.port} stopped"}
    launch_service.run = False
    launch_service.stop_simu()
    return jsonify(response), 200
