from utils.uuid import uuid4_hex
from flask import request, jsonify
from app import db

class ApiController:

	e400 = { 'Error': 'The request contains error(s).' }
	e401 = { 'Error': 'You are not authorized.' }
	e404 = { 'Error': 'The requested content was not found.' }

	def __init__(self, model, security_level) -> None:
				
		# set request information
		self.request_obj = request
		if request.is_json:
			self.json = request.get_json()
			self.data = request.get_data()

		# create an empty response
		self.response_obj = {}
		
		# security check
		self.has_clearance = self.security_check(security_level)

		# connect to data model if clear
		if self.has_clearance:
			self.table = db[model]
			self.model = self.use_model()

	def security_check(self, level):
		if level >= 5: return True
		if level == 1:
			if self.json.get('security-token'): return True
		return False
	
	def get_result(self, query):
		return list(self.table.find(query))
	
	def has_valid_key(self, key, value):
		if hasattr(self, 'json'):
			if self.json.get(key) == value:	return True
		return False
	
	def use_id(self):
		self.response_obj['_id'] = uuid4_hex()

	def _200(self, response):	return jsonify(response), 200
	def _400(self, response):	return jsonify(response), 400
	def _401(self, response):	return jsonify(response), 401
	def _404(self, response):	return jsonify(response), 404
	def _500(self, response):	return jsonify(response), 500

	def new(self):
		if not self.has_clearance: return self._401(self.e401)
		try:
			for key, obj in self.model.__dict__.items():
				value = self.json.get(obj.object_key)
				if value == None:
					value = obj.value
				obj.value = value
				self.response_obj[key] = value
			self.use_id()
			self.model.validate(self.response_obj, self.table)
			if self.model.errors != {}:
				return self._400({ 'Error': self.model.errors })
			self.table.insert_one(self.response_obj)
			return self._200(self.response_obj)
		except Exception as e:
			print(e)
			return self._400({ 'Error': 'err' })

	def remove(self, query = {}):
		if not self.has_clearance: return self._401(self.e401)
		result = self.get_result(query)
		for r in result:
			self.table.delete_one(r)
		return self._200(result)

	def get(self, query = {}):
		if not self.has_clearance: return self._401(self.e401)
		result = self.get_result(query)
		return self._200(result)