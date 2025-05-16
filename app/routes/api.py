from flask import Blueprint, request, jsonify
from datetime import datetime

device_bp = Blueprint('device', __name__, url_prefix='/api/v0')

device = {
    "status": "CLOSED",
    "updated_on": None
}

# Simulated sensor data
sensor_data = {
    "temperature_c": 22.5,
    "soil_moisture_percent": 55,
    "humidity_percent": 60,
    "timestamp": datetime.utcnow().isoformat()
}

# Watering schedules
schedules = []

@device_bp.route('/device/valve', methods=['PATCH'])
def update_valve():
    data = request.get_json()
    if not data or data.get("status") not in ["OPEN", "CLOSED"]:
        return jsonify({"error": "Invalid status"}), 400

    # Send signal to open or close valve here

    device["status"] = data["status"]
    device["updated_on"] = datetime.utcnow().isoformat()
    return jsonify({
        "status": device["status"],
        "updated_on": device["updated_on"]
    }), 200

@device_bp.route('/device/status', methods=['GET'])
def get_device_status():

    # Retrieve device status data and update

    return jsonify({
        "status": device["status"],
        "updated_on": device["updated_on"]
    }), 200

@device_bp.route('/data', methods=['GET'])
def get_sensor_data():

    # Retrive device sensor data here

    sensor_data["timestamp"] = datetime.utcnow().isoformat()
    return jsonify(sensor_data), 200

@device_bp.route('/schedule', methods=['GET'])
def get_schedules():
    return jsonify(schedules), 200

@device_bp.route('/schedule', methods=['POST'])
def add_schedule():
    data = request.get_json()

    if not data or "start_time" not in data or "duration_minutes" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    schedule = {
        "id": len(schedules) + 1,
        "start_time": data["start_time"],  
        "duration_minutes": data["duration_minutes"],
        "created_on": datetime.utcnow().isoformat()
    }

    schedules.append(schedule)
    return jsonify(schedule), 201