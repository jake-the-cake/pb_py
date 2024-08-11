from app import app
from .models import Event

@app.route('/api/event/new/', methods=['POST'])
def new_event():
	return Event().new()

# @app.route('/api/user/<string:id>/', methods=['GET'])
# def get_one(id):
# 	return User().get({ '_id': id })

@app.route('/api/event/all/', methods=['GET'])
def get_all_events():
	return Event().get()

# @app.route('/api/user/remove/<string:id>/', methods=['DELETE'])
# def remove_one(id):
# 	return User().remove({ '_id': id })

# @app.route('/api/user/remove/all', methods=['DELETE'])
# def remove_all():
# 	return User(1).remove()