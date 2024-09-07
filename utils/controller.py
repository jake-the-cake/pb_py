from utils.uuid import uuid4_hex
from flask import request, jsonify
from utils.quiggle import Quiggle

class ApiController(Quiggle):

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

	def common_reponse(self, status_code: int):
		return jsonify(self.get_response_data()), status_code

	# ------------------------ #
	# -INIT------------------- #
	# ------------------------ #

	def __init__(self) -> None:
		super().__init__()
			# create an empty response
		self.response_obj = { 'data': {}, 'string_data': {} }
			# capture request information
		self.request_obj = request
		json_dict = {}
		if request.is_json:
			self.json = request.get_json()
			for key in self.json.keys():
				py_key = key.replace('-', '_')
				json_dict[py_key] = self.json[key]
			self.data = request.get_data()
		self.json = json_dict
	
	# ------------------------ #
	# -UTILS------------------ #
	# ------------------------ #
	
	def use_id(self):	self.response_obj['data']['_id'] = uuid4_hex()

	def get_result(self, query):
		return list(self.table.find(query))
	
	def set_response_obj(self):
		for key in self.schema.keys():
			value = self.json.get(key)
			schema_key = self.schema[key]
			schema_key.set_value(value)
			schema_key.validate()
			# schema_key.use_validation(key)
			self.response_obj['data'][key] = schema_key.value
			schema_key.stringify()
			self.response_obj['string_data'][key] = schema_key.string_value
		self.use_validation(self.schema)

	# ------------------------ #
	# -CONTROLS--------------- #
	# ------------------------ #

	def new(self):
		try:
			self.set_response_obj()
			self.use_id()
			if self.errors != {}:
				return self._400({ 'errors': self.errors })
			self.add_one()
			return self.common_reponse(200)
		except Exception as e:
			raise(e)
			return self._400(self.e400)

	def remove(self, query = {}):
		result = self.get_result(query)
		for r in result:
			self.table.delete_one(r)
		return self._200({})

	def get(self, query = {}):
		self.set_response_obj()
		result = self.get_result(query)
		print(result)
		return self.common_reponse(200)