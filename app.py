import random
import string
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room
from models import Room, User
from database.Base import db_session

app = Flask(__name__)
socketio = SocketIO(app)


def generate_unique_room_code():
    room_code = ""
    unique_code = False
    while not unique_code:
        room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        unique_code = Room.query.filter_by(code=room_code).first() is None
    return room_code


def fetch_players_of_game(room_id):
    game_users: list[User] = User.query.filter_by(room_id=room_id).all()
    players = {}
    for user in game_users:
        players[user.name] = user.ready
    return players


@app.route('/room', methods=['POST'])
def create_room():
    room_name = request.json['room_name']
    new_room_code = generate_unique_room_code()
    db_session.add(Room(name=room_name, code=new_room_code, active=False))
    db_session.commit()
    return new_room_code, 201


@socketio.on('connect')
def on_connect():
    user_sid = request.sid
    print(f'Client with sid {user_sid} connected')


@socketio.on("join")
def on_join(data):
    user_sid = request.sid
    user_name = data['user_name']
    requested_room_code = data['room_code']
    game_room: Room = Room.query.filter_by(code=requested_room_code).first()
    if game_room is None:
        return {"message": "Invalid room"}
    if game_room.active is True:
        return {"message": "Game already started"}
    if User.query.filter_by(sid=user_sid).first():
        return {"message": "User already in a room"}
    new_user = User(name=user_name, sid=user_sid, room_id=game_room.id)
    db_session.add(new_user)
    db_session.commit()
    join_room(game_room.code)
    players_of_game = fetch_players_of_game(game_room.id)
    emit("show players", players_of_game, room=game_room.code)
    return {"message": "Ok"}


@socketio.on("ready")
def on_ready():
    user_sid = request.sid
    user_to_modify: User = User.query.filter_by(sid=user_sid).first()
    if user_to_modify:
        user_to_modify.ready = True
        db_session.merge(user_to_modify)
        db_session.commit()


@socketio.on("get room name")
def on_get_room_name():
    user_sid = request.sid
    user_to_read: User = User.query.filter_by(sid=user_sid).first()
    if user_to_read:
        emit("receive room name", {"room_name": user_to_read.room.name})


@socketio.on("disconnect")
def on_disconnect():
    user_sid = request.sid
    user_to_delete = User.query.filter_by(sid=user_sid).first()
    if user_to_delete:
        db_session.delete(user_to_delete)
        db_session.commit()
        print(f'Client with sid {user_sid} disconnected and deleted')


if __name__ == '__main__':
    socketio.run(app, "127.0.0.1", 7000)
