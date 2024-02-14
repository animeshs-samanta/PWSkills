# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# This is the data that will be updated in real-time
data = {'value': 0}

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html', data=data)

# WebSocket event handler to update data
@socketio.on('update_data')
def handle_message(message):
    global data
    data['value'] += 1
    # Emit the updated data to all clients
    socketio.emit('data_updated', data)

if __name__ == '__main__':
    # Run the Flask app with SocketIO
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
