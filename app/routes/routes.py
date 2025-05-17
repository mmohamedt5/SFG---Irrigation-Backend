from flask import Blueprint, request, jsonify, render_template
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Device state
device = {
    "status": "CLOSED",
    "temperature": 0.0,
    "updated_on": None
}

command_queue = None  # Simple command storage

@api_bp.route('/device/command', methods=['GET', 'PATCH'])
def handle_command():
    global command_queue
    
    if request.method == 'PATCH':
        data = request.get_json()
        if not data or data.get("command") not in [1, 2]:
            return jsonify({"error": "Invalid command"}), 400
        
        command_queue = data["command"]
        return jsonify({"message": f"Command {command_queue} queued"})
    
    # New GET method to allow Arduino to retrieve queued commands
    elif request.method == 'GET':
        if command_queue is not None:
            response = jsonify({"command": command_queue})
            # Reset the command after it's been retrieved
            command_queue = None
            return response
        else:
            return jsonify({"message": "No commands in queue"})


@api_bp.route('/v0/device/status', methods=['GET', 'PATCH'])
def handle_device_status():
    if request.method == 'PATCH':
        data = request.get_json()
        if not data or data.get("status") not in ["OPEN", "CLOSED"]:
            return jsonify({"error": "Invalid status"}), 400

        device["status"] = data["status"]
        device["temperature"] = data.get("temperature", device["temperature"])
        device["updated_on"] = datetime.utcnow().isoformat()
        
        print(f"Received status update: {data}")
        return jsonify({
            "status": device["status"],
            "temperature": device["temperature"],
            "updated_on": device["updated_on"],
            "message": "Status updated successfully"
        })
    
    # GET request handling
    return jsonify({
        "status": device["status"],
        "temperature": device["temperature"],
        "updated_on": device["updated_on"]
    })

@api_bp.route('/valve-status')
def valve_status_page():
    return render_template('valve_status.html', 
                         status=device["status"],
                         temperature=device["temperature"],
                         last_updated=device["updated_on"])