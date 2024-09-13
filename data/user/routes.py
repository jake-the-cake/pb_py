from app import app
from .models import User

@app.route('/api/user/new/', methods=['POST'])
def new_user():
	return User().new()

@app.route('/api/user/<string:id>/', methods=['GET'])
def get_one(id):
	return User().get({ '_id': id })

@app.route('/api/user/all/', methods=['GET'])
def get_all():
	return User().get()

@app.route('/api/user/remove/<string:id>/', methods=['DELETE'])
def remove_one(id):
	return User().remove({ '_id': id })

@app.route('/api/user/remove/all', methods=['DELETE'])
def remove_all():
	return User().remove()