from utils.controller import ApiController
from app import db

class Model(ApiController):

	def __init__(self):
		super().__init__()
		self.name = str.lower(self.__class__.__name__)
		self.schema = self.tools.set_class_props(self)
		self.schema['_id'] = None
		self.table = db[self.name]

	# fallback if no validate method is present
	def validate(self):
		pass

	# check that the values meet the settings
	def use_validation(self, obj):
		for key in obj:
			if key == '_id':
				continue
			item = obj[key]
			if not item.value: item.use_default()
			if item.is_required == True: self.check_required(key, item)			
			if item.is_unique == True: self.check_unique(key, item)			
			self.check_length(key, item)
		# pass to custom validation
		self.validate()
		print(self.errors)

	def populate_by_id(self, model, id):
		print(model, id)

	def check_required(self, key, obj):
		if not obj.value:
			self.errors[key + '_required'] = 'Value required for {}.'.format(key)

	def check_unique(self, key, obj):
		result = list(self.table.find({ key: obj.value }))
		if len(result) > 0:
			self.errors[key + '_unique'] = "'{}' is already in use.".format(obj.value, key)

	def check_length(self, key, obj):
		l = len(obj.string_value)
		if l < obj.min_length or l > obj.max_length:
			self.errors[key + '_length'] = 'Value must be {}-{} characters in length.'.format(obj.min_length, obj.max_length)

	def add_one(self) -> None:
		self.table.insert_one(self.response_obj['string_data'])
	
	def get_response_data(self):
		return self.response_obj['data']
	
	def get_string_data(self):
		return self.response_obj['string-data']