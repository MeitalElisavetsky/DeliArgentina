import pytest
from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient
from app import routes
import os

app = Flask(__name__, static_url_path='/static')
app.config['MONGO_URI'] = 'mongodb://mongodb:27017/test_deli_argentina_db'

#app.config['MONGO_URI'] = "mongodb://root:ZTRW3W0ToK@mongodb:27017/deli_argentina_db"

mongo = PyMongo(app)



