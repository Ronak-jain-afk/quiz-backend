from flask import Flask, jsonify, request
import random
import string
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# In-memory quiz questions
questions = [
    {"id": 1, "question": "What is Python?", 
     "options": ["Snake", "Programming Language", "Car"], "answer": "Programming Language"},
    {"id": 2, "question": "Which framework is this?", 
     "options": ["Django", "Flask", "FastAPI"], "answer": "Flask"}
]

# In-memory rooms and players
rooms = {}  # room_code: {"players": {username: {"answers": {}, "score": 0}}, "started": False}

def generate_room_code(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@app.route("/")
def home():
    return "Quiz Backend is running with Flask 🚀"

# Create a new room
@app.route("/room", methods=["POST"])
def create_room():
    room_code = generate_room_code()
    rooms[room_code] = {"players": {}, "started": False}
    return jsonify({"room_code": room_code})

# Join a room
@app.route("/room/<room_code>/join", methods=["POST"])
def join_room(room_code):
    data = request.json
    username = data.get("user")
    if room_code not in rooms:
        return jsonify({"error": "Room not found"}), 404
    if username in rooms[room_code]["players"]:
        return jsonify({"error": "User already in room"}), 400
    rooms[room_code]["players"][username] = {"answers": {}, "score": 0}
    return jsonify({"message": f"{username} joined room {room_code}"})

# Get quiz questions for a room
@app.route("/room/<room_code>/quiz", methods=["GET"])
def get_room_quiz(room_code):
    if room_code not in rooms:
        return jsonify({"error": "Room not found"}), 404
    return jsonify(questions)

# Submit answers for a player in a room
@app.route("/room/<room_code>/submit", methods=["POST"])
def submit_room_answers(room_code):
    data = request.json
    username = data.get("user")
    answers = data.get("answers", {})
    if room_code not in rooms or username not in rooms[room_code]["players"]:
        return jsonify({"error": "Room or user not found"}), 404
    # Score calculation
    score = 0
    for q in questions:
        qid = q["id"]
        if str(qid) in answers and answers[str(qid)] == q["answer"]:
            score += 1
    rooms[room_code]["players"][username]["answers"] = answers
    rooms[room_code]["players"][username]["score"] = score
    return jsonify({"user": username, "score": score, "total": len(questions)})

# Get all players and their scores in a room
@app.route("/room/<room_code>/players", methods=["GET"])
def get_room_players(room_code):
    if room_code not in rooms:
        return jsonify({"error": "Room not found"}), 404
    players = [
        {"user": user, "score": info["score"]}
        for user, info in rooms[room_code]["players"].items()
    ]
    return jsonify(players)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
