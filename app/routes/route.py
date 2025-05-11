from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models.device import Device, Command

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    
    if not data or 'device_id' not in data:
        return jsonify({'error': 'Missing device_id'}), 400
    
    device = Device.query.filter_by(device_id=data['device_id']).first()
    if not device:
        device = Device(device_id=data['device_id'])
        db.session.add(device)
    
    device.last_seen = datetime.utcnow()
    device.is_online = True
    
    if 'temperature' in data:
        device.temperature = float(data['temperature'])
    if 'moisture' in data:
        device.moisture = float(data['moisture'])
    
    db.session.commit()
    return jsonify({'status': 'success'}), 200

@api_bp.route('/command', methods=['GET'])
def get_command():
    device_id = request.args.get('device_id')
    if not device_id:
        return jsonify({'error': 'Missing device_id'}), 400
    
    # Get the oldest pending command for the device
    command = Command.query.filter_by(
        device_id=device_id,
        status='pending'
    ).order_by(Command.created_at.asc()).first()
    
    if not command:
        return jsonify({'command': None}), 200
    
    command.status = 'sent'
    command.sent_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'command': command.command,
        'command_id': command.id
    }), 200

@api_bp.route('/status', methods=['POST'])
def update_status():
    data = request.get_json()
    
    if not data or 'device_id' not in data:
        return jsonify({'error': 'Missing device_id'}), 400
    
    device = Device.query.filter_by(device_id=data['device_id']).first()
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    device.last_seen = datetime.utcnow()
    device.is_online = True
    
    if 'command_id' in data:
        command = Command.query.get(data['command_id'])
        if command and command.device_id == data['device_id']:
            command.status = 'completed'
            command.completed_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify({'status': 'success'}), 200 
