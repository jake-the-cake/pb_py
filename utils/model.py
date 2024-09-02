from utils.controller import ApiController
from app import db

class Model(ApiController):

	def __init__(self):
		super().__init__()
		self.name = str.lower(self.__class__.__name__)
		self.schema = self.tools.set_class_props(self)
		self.table = db[self.name]

	def validate(self):
		pass

	def populate_by_id(self, model, id):
		print(model, id)

	def check_required(self, obj_key, key, value):
		if value == '' or value == None:
			self.errors[obj_key] = 'Value required for {}'.format(key)

	def check_unique(self, obj_key, key, value, table):
		result = list(table.find({ key: value }))
		if len(result) > 0:
			self.errors[obj_key] = 'Value "{}" for {} is already in use'.format(value, key)

	def add_one(self) -> None:
		self.table.insert_one(self.response_obj['string_data'])
	
	def get_response_data(self):
		return self.response_obj['data']
	
	def get_string_data(self):
		return self.response_obj['string-data']