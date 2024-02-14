from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, emit,  leave_room, send
import random 
import string

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecret"
socketio = SocketIO(app, cors_allowed_origins='https://salmon-salesmen-yygvx.pwskills.app:5001')


rooms = {}


def generateRoomCode(length: int, existing_codes: list) -> str :
    while True:
        code_char = [random.choice(string.ascii_letters) for _ in range(length)]
        code = ''.join(code_char)
        if code not in existing_codes:
            return code

@app.route('/', methods = ["GET","POST"])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get('name')
        create = request.form.get('create', False)
        code = request.form.get('code')
        join = request.form.get('join', False)

        if not name:
            return render_template('home.html', error = "Name is required", code = code)
        if create != False:
            room_code = generateRoomCode(6, list(rooms.keys()))
            new_room = {
                'member' : 0,
                'message' : []
            }
            rooms[room_code] = new_room

        if join != False:
            #no code
            if not code:
                return render_template('home.html', error = "Please enter a room code to enter a chta room", name = name)
            
            #Invalid code
            if code not in rooms:
                return render_template('home.html', error = "Please enter a valid code", name = name)
            
            room_code = code
        
        session['room'] = room_code
        session['name'] = name
        return redirect(url_for('room'))

    else:
        return render_template('home.html')
        


@app.route('/room')
def room():
    room = session.get('room')
    name = session.get('name')

    if name is None or room is None or room not in rooms:
        return redirect(url_for('home'))

    messages = rooms.get(room, {}).get('messages', [])
    return render_template('room.html', room = room, messages = messages)


@socketio.on('connect')
def connect_event():
    name = session.get('name')
    room = session.get('room')
    
    if name is None or room is None:
        return
    
    if room not in rooms:
        leave_room(room)
    
    join_room(room)

    message = {
        "sender": " ",
        "message": f"{name} has entered the chat"
    }

    emit('message', message, room=room)  # Using emit to send messages to a specific room
    rooms[room].setdefault("members", 0)
    rooms[room]["members"] += 1

    emit('update_members', {'members': rooms[room]['members']}, room=room)



@socketio.on('message')
def message_event(payload):
    name = session.get('name')
    room = session.get('room')
    
    if name is None or room is None:
        return

    message = {
        "sender": name,
        "message": payload["message"]
    }

    emit('message', message, room=room)

    # Ensure the 'messages' key is present in the 'rooms' dictionary
    rooms.setdefault(room, {}).setdefault("messages", [])
    rooms[room]["messages"].append(message)




@socketio.on('disconnect')
def disconnect_event():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1

        if rooms[room]["members"] <= 0:
            del rooms[room]

        message = {
            "message": f"{name} has left the chat",
            "sender": ""
        }
        emit('message', message, room=room)  # Use emit to send a message to a specific room
        emit('update_members', {'members': rooms.get(room, {}).get('members', 0)}, room=room)



if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5001)
