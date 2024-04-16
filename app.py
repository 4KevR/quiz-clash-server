import random
import string
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room
from models import Room, User, GameCategory, Category, Question, QuestionOption
from database.Base import db_session
from sqlalchemy.sql.expression import func

app = Flask(__name__)
socketio = SocketIO(app)

CATEGORIES_PER_USER = 4


def generate_unique_room_code():
    room_code = ""
    unique_code = False
    while not unique_code:
        room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        unique_code = Room.query.filter_by(code=room_code).first() is None
    return room_code


def fetch_players_of_game(room_id):
    game_users: list[User] = User.query.filter_by(room_id=room_id).all()
    players = []
    for user in game_users:
        players.append(user.name)
    return {"players": players}


def fetch_categories_of_game(room_id):
    game_categories: list[GameCategory] = GameCategory.query.filter_by(room_id=room_id).order_by(GameCategory.id).all()
    categories = []
    for game_category in game_categories:
        game_category_question: Question = game_category.question
        game_category_question_options: list[QuestionOption] = game_category_question.question_options
        question_options = []
        for question_option in game_category_question_options:
            question_options.append({
                "questionOption": question_option.question_option,
                "isRight": question_option.is_right
            })
        questions = [{
            "id": game_category_question.id,
            "question": game_category_question.question,
            "questionOptions": question_options
        }]
        json_category = {
            "id": game_category.category_id,
            "categoryName": game_category.category.category_name,
            "questions": questions
        }
        categories.append(json_category)
    return categories


@app.route('/room', methods=['POST'])
def create_room():
    room_name = request.json['room_name']
    amount_of_players = request.json['amount_of_players']
    new_room_code = generate_unique_room_code()
    new_room = Room(name=room_name, amount_of_players=amount_of_players, code=new_room_code, active=False)
    db_session.add(new_room)
    db_session.commit()
    game_category_id_list = Category.query.order_by(func.random()).limit(CATEGORIES_PER_USER*amount_of_players).all()
    for game_category in game_category_id_list:
        random_question = Question.query.filter_by(category_id=game_category.id).order_by(func.random()).first()
        new_category_set = GameCategory(category_id=game_category.id,
                                        room_id=new_room.id,
                                        question_id=random_question.id)
        db_session.add(new_category_set)
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
    categories_of_game = fetch_categories_of_game(game_room.id)
    joined_room_payload = {"room_name": game_room.name, "categories": categories_of_game}
    emit("joined room", joined_room_payload)
    if len(game_room.users) != 1:
        emit("show players", players_of_game, room=game_room.code)
    if len(game_room.users) == game_room.amount_of_players:
        emit("game start", room=game_room.code)
    return {"message": "Ok"}


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
