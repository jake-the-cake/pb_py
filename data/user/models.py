from flask import jsonify, request
from app import db
from utils.uuid import uuid4_hex
from utils.model import StringField, EmailField, Model

class ApiModel:

	def __init__(self, model) -> None:
		self.table = db[model]
	
	def get_result(self, query):
		return list(self.table.find(query))

	def _200(self, response):	return jsonify(response), 200
	def _400(self, response):	return jsonify(response), 400
	def _401(self, response):	return jsonify(response), 401
	def _404(self, response):	return jsonify(response), 404
	def _500(self, response):	return jsonify(response), 500

	def new(self, model):
		data = request.get_json()
		return self._200(data)

	def remove(self, query = {}):
		result = self.get_result(query)
		for r in result:
			self.table.delete_one(r)
		return self._200(result)

	def get(self, query = {}):
		self.model()
		result = self.get_result(query)
		return self._200(result)

class User(ApiModel):

	def __init__(self) -> None:
		super().__init__('user')
		print(self)

	def model(self):
		return Model(
			first_name = StringField('first-name', 20).required(),
			last_name = StringField('last-name', 20),
			email = EmailField('email', 30).required().unique(),
			age = StringField('age', 3)
		)
	

		

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