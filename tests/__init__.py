from flask import Flask
from flask_pymongo import PyMongo
import pytest

app = Flask(__name__, static_url_path='/static')
mongo = PyMongo(app)

from app import routes

