from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

def init_app():
    try:
        load_dotenv()
    except:
        print('env not found')
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.environ["MONGO_CONNECTION"]
    db = PyMongo(app).db
    return [app, db]