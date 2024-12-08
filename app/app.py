from flask import Flask, jsonify, request

app = Flask(__name__)
devices = [{'id':1, 'name':'Lampara salon', 'type':'luminaria', 'status':'on'}]

# Ruta principal para obtener todos los dispositivos (método GET)
@app.route('/', methods=['GET'])
def index():
    return jsonify({'Devices':devices})


# Ruta para añadir un nuevo dispositivo (método POST)
@app.route('/add_device', methods=['POST'])
def add_device():
    # Obtenemos los datos enviados por el cliente
    new_device = request.get_json()
    # Validación: comprobamos que todos los campos obligatorios están presentes
    if not new_device.get('id') or not new_device.get('name') or not new_device.get('type') or not new_device.get('status'):
        # Si falta algún campo, devolvemos un error (400 Bad Request)
        return jsonify({'error': 'Faltan campos obligatorios (id, name, type, status)'}), 400

    # Comprobamos que no haya duplicados en el ID
    for device in devices:
        if device['id'] == new_device['id']:
            # Si el ID ya existe, devolvemos un error
            return jsonify({'error': 'El ID ya existe'}), 400

    # Si todo está correcto, añadimos el nuevo dispositivo a la lista
    devices.append(new_device)
    # Devolvemos un mensaje de éxito con el estado 201 (Created)
    return jsonify({'message': 'Dispositivo añadido exitosamente', 'Devices': devices}), 201

#Ruta para actualizar un dispositivo con un ID determinado (método PUT)
@app.route('/update_device/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    updated_device = request.get_json()
    for device in devices:
        # Comprobamos que no haya duplicados en el ID
        if device['id'] == device_id:
            device.update(updated_device)  # Ahora usamos el JSON recibido correctamente
            return jsonify({'message': f'Dispositivo con ID {device_id} actualizado', 'Device': device}), 200
    return jsonify({'error': f'Dispositivo con ID {device_id} no encontrado'}), 404



# Ruta para eliminar un dispositivo por ID (método DELETE)
@app.route('/delete_device/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
   
    global devices  # Declaramos la lista como global para poder modificarla
    # Usamos una lista por compresión para filtrar y mantener solo los dispositivos con IDs diferentes al proporcionado
    devices = [device for device in devices if device['id'] != device_id]
    # Devolvemos un mensaje indicando que se eliminó el dispositivo
    return jsonify({'message': f'Dispositivo con ID {device_id} eliminado', 'Devices': devices}), 200


if __name__=="__main__":
    app.run(debug=True)