from __main__ import app, db
from flask import make_response, jsonify, request
from flask_cors import CORS, cross_origin
from bson.objectid import ObjectId
import random
import math

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def make_json(joke):
    joke['_id'] = str(joke['_id'])
    return make_response(jsonify(joke), 200)

@app.route("/")
def home_page():
   return "Hello World"

@app.route("/random")
@cross_origin()
def random_joke():
    rand = random.random()
    count = db.jokes.count()
    cursor = db.jokes.find().limit(1).skip(math.floor(rand*count))
    for doc in cursor:
        joke = doc
    print(joke)
    return make_json(joke)

@app.route("/<id>")
@cross_origin()
def get_joke(id):
    joke = db.jokes.find_one_or_404({'_id': ObjectId(id)})
    print(joke)
    return make_json(joke)

@app.route('/add', methods=['POST'])
@cross_origin()
def add_joke():
    new_joke = {
        "joke": request.json['joke'],
        "answer": request.json['answer'],
        "userId": request.json['userId']
    }
    if request.json['joke'] == '':
        print("Empty joke")
        return make_response(jsonify({"error" : "joke not set"}), 400)
    else:
        print(new_joke)
        db.jokes.insert_one(new_joke)
        return make_json(new_joke)

@app.route('/like/<id>', methods=['POST'])    
@cross_origin()
def add_like(id):
    joke = db.jokes.find_one_or_404({'_id': ObjectId(id)})
    current_likes = 0
    if 'likes' in joke:
        current_likes = joke['likes']        
    joke['likes'] = current_likes + 1
    print(joke)
    db.jokes.save(joke)
    return make_json(joke)        