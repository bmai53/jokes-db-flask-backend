from flask import Flask, make_response, jsonify, request
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
import random
import math

load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["MONGO_URI"] = os.environ["MONGO_CONNECTION"]
db = PyMongo(app).db.jokes

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
    count = db.count()
    cursor = db.find().limit(1).skip(math.floor(rand*count))
    for doc in cursor:
        joke = doc
    print(joke)
    return make_json(joke)

@app.route("/<id>")
@cross_origin()
def get_joke(id):
    joke = db.find_one_or_404({'_id': ObjectId(id)})
    print(joke)
    return make_json(joke)

@app.route('/add', methods=['POST'])
@cross_origin()
def add_joke():
    new_joke = {
        "joke": request.json['joke'],
        "answer": request.json['answer']
    }
    if request.json['joke'] == '':
        print("Empty joke")
        return make_response(jsonify({"error" : "joke not set"}), 400)
    else:
        print(new_joke)
        db.insert_one(new_joke)
        return make_json(new_joke)

if __name__ == "__main__":
    app.run(debug=True)