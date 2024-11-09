from flask import request, jsonify

from api.field import Key_Field
from quiggle.utils.uuid import uuid4_hex
from quiggle.features.quiggle import Quiggle

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
	
	def use_id(self):
		self.schema['_id'] = Key_Field().default(uuid4_hex())
		self.schema['_id'].use_default()

	def get_result(self, query):
		return list(self.table.find(query))
	
	def new_data_object(self):
		self.use_id()
		for key in self.schema.keys():
			item = self.schema.get(key)
			item.set_value(self.json.get(key, item.value))
			item.validate()
			self.response_obj['data'][key] = item.value
			self.response_obj['string_data'][key] = item.string_value
		self.use_validation(self.schema)

	def set_response_data(self, data):
		if isinstance(data, list):
			response = []
			for item in data:
				item_data = {}
				for key in item.keys():
					self.schema[key].string_value = str(item[key])
					self.schema[key].parse()
					item_data[key] = self.schema[key].value
				response.append(item_data)
			data = response
		self.response_obj['data'] = data

	# ------------------------ #
	# -CONTROLS--------------- #
	# ------------------------ #

	def new(self):
		try:
			self.new_data_object()
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
		result = self.get_result(query)
		self.set_response_data(result)
		return self.common_reponse(200)