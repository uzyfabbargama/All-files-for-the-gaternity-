# app.py
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

# Crea la instancia de la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-goes-here' # Cambia esto por una clave secreta segura
socketio = SocketIO(app)

# Esta variable almacenará el estado actual de los valores
current_state = {
    "bondad": 10,
    "hostilidad": 10,
    "logica": 10
}

# ----------------- Rutas de la aplicación -----------------

# Ruta para la interfaz del amigo (el usuario del chat)
@app.route('/')
def index():
    # Renderiza la plantilla HTML para el usuario
    return render_template('index.html')

# Ruta para tu interfaz de administrador
@app.route('/admin')
def admin():
    # Renderiza la plantilla HTML para el administrador
    return render_template('admin.html')

# ----------------- Manejo de WebSockets -----------------

# Evento que se dispara cuando un cliente se conecta
@socketio.on('connect')
def handle_connect():
    print('Un cliente se ha conectado.')

# Evento que maneja los mensajes enviados por el amigo (el usuario)
@socketio.on('message_from_client')
def handle_client_message(data):
    global current_state
    
    # Actualiza los valores con los que el amigo ajustó los deslizadores
    current_state["bondad"] = data.get("bondad")
    current_state["hostilidad"] = data.get("hostilidad")
    current_state["logica"] = data.get("logica")
    
    # Imprime el mensaje y los valores en la consola del servidor para referencia
    print(f"Nuevo mensaje del cliente: '{data['message']}'")
    print(f"Valores actuales: Bondad={current_state['bondad']}, Hostilidad={current_state['hostilidad']}, Lógica={current_state['logica']}")
    
    # Envía el mensaje y los valores a la interfaz del administrador
    emit('message_for_human', {'message': data['message'], 'state': current_state}, broadcast=True)

# Evento que maneja las respuestas enviadas por ti (el humano)
@socketio.on('message_from_human')
def handle_human_message(data):
    # Imprime la respuesta en la consola del servidor
    print(f"Respuesta del humano: '{data['message']}'")
    
    # Envía la respuesta a la interfaz del amigo (el usuario)
    emit('message_for_client', {'message': data['message']}, broadcast=True)

if __name__ == '__main__':
    # Ejecuta la aplicación. El debug=True es útil para el desarrollo
    # Asegúrate de usar `socketio.run()` en lugar de `app.run()`
    socketio.run(app, debug=True)
