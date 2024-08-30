from utils.uuid import uuid4_hex
from flask import request, jsonify
# from app import db

class ApiController:

		# error responses
	e400 = { 'Error': 'The request contains error(s).' }
	e401 = { 'Error': 'You are not authorized.' }
	e404 = { 'Error': 'The requested content was not found.' }

		# response status returns
	def _200(self, response):	return jsonify(response), 200
	def _201(self, response):	return jsonify(response), 201
	def _400(self, response):	return jsonify(response), 400
	def _401(self, response):	return jsonify(response), 401
	def _404(self, response):	return jsonify(response), 404
	def _500(self, response):	return jsonify(response), 500

	# ------------------------ #
	# -INIT------------------- #
	# ------------------------ #

	def __init__(self) -> None:
		
			# capture request information
		self.request_obj = request
		if request.is_json:
			self.json = request.get_json()
			self.data = request.get_data()
		
		# create an empty response
		self.response_obj = {}
	
	# ------------------------ #
	# -UTILS------------------ #
	# ------------------------ #
	
	def use_id(self):	self.response_obj['_id'] = uuid4_hex()

	def get_result(self, query):
		return list(self.table.find(query))
	
	def set_response_obj(self):
		for key in self.schema.keys():
			print(key)
			self.response_obj[key] = self.schema[key]
			self.response_obj[key].value = self.json.get(key)

		print(vars(self))

	# ------------------------ #
	# -CONTROLS--------------- #
	# ------------------------ #

	def new(self):
		try:
			self.set_response_obj()
			self.use_id()
			if self.errors != {}:
				return self._400({ 'errors': self.model.errors })
			self.table.insert_one(self.response_obj)
			return self._200(self.response_obj)
		except Exception as e:
			raise (e)
			return self._400(self.e400)

	def remove(self, query = {}):
		result = self.get_result(query)
		for r in result:
			self.table.delete_one(r)
		return self._200(result)

	def get(self, query = {}):
		result = self.get_result(query)
		return self._200(result)