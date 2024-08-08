from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.data

from www.hiking.routes import *
from data.user.routes import *
from www.apps.calendar.routes import *