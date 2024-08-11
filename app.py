from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.data

# api routes
from data.user.routes import *
from data.calendar.routes import *

# web routes
from www.hiking.routes import *
from www.apps.calendar.routes import *