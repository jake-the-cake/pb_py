from flask import jsonify, request
from app import db
from utils.uuid import uuid4_hex

class User:

	def new_user(self):
		data = request.get_json()
		user = {
			'_id': uuid4_hex(),
			'first_name': data.get('first-name'),
			'last_name': data.get('last-name'),
			'email': data.get('email'),
			'age': data.get('age')
		}
		try:
			db.user.insert_one(user)
			return jsonify(user), 200
		except Exception as e:
			return jsonify(e), 400

	
	def get(self, query = {}):
		users = list(db.user.find(query))
		return jsonify(users), 200