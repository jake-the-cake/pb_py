from utils.controller import ApiController
from app import db

def set_class_props(c, obj = {}):
		# class dict variable
	d = c.__class__.__dict__
		# fill dict with class keys
	for key in d.keys():
			# exclude default methods
		if not key.startswith('__'):
				obj[key] = d[key]
	return obj

class Model(ApiController):

	def __init__(self):
		self.schema = {}
		self.name = str.lower(self.__class__.__name__)
		set_class_props(self, self.schema)
		super().__init__()
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