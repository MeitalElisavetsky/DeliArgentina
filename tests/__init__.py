from flask import Flask
from flask_pymongo import PyMongo
import pytest

app = Flask(__name__, static_url_path='/static')
app.config['MONGO_URI'] = 'mongodb://mongodb:27017/test_deli_argentina_db'
mongo = PyMongo(app)

from app import routes

