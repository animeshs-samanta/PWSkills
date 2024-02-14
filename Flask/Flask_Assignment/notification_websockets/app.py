# app.py
from flask import Flask, render_template
from flask import request
import json

app = Flask(__name__)

# This is the data that will be updated in real-time
data = {'value': 0}

# Store WebSocket clients
clients = set()

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# WebSocket endpoint for updating data
@app.route('/update_data')
def update_data():
    def generate():
        while True:
            yield json.dumps(data) + '\n'
    return app.response_class(generate(), mimetype='application/json')

# WebSocket endpoint for receiving notifications
@app.route('/notify')
def notify():
    message = request.args.get('message')
    for client in clients:
        client.send(message)
    return '', 204

@app.route('/ws')
def ws():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        clients.add(ws)
        while True:
            message = ws.receive()
            if message is None:
                break
    clients.remove(ws)
    return ''

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
