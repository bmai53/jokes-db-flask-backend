from flask import Flask, make_response, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
import random
import math

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ["MONGO_CONNECTION"]
db = PyMongo(app).db.jokes

def make_json(joke):
    joke['_id'] = str(joke['_id'])
    return make_response(jsonify(joke), 200)

@app.route("/")
def home_page():
   return "Hello World"

@app.route("/random")
def random_joke():
    rand = random.random()
    count = db.count()
    cursor = db.find().limit(1).skip(math.floor(rand*count))
    for doc in cursor:
        joke = doc
    print(joke)
    return make_json(joke)

@app.route("/<id>")
def get_joke(id):
    joke = db.find_one_or_404({'_id': ObjectId(id)})
    print(joke)
    return make_json(joke)

@app.route('/add', methods=['POST'])
def add_joke():
    new_joke = {
        "joke": request.json['joke'],
        "answer": request.json['answer']
    }
    print(new_joke)
    db.insert_one(new_joke)
    return make_json(new_joke)

if __name__ == "__main__":
    app.run(debug=True)