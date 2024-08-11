class Model:

	def __init__(self, **kwargs):
		for key, value in kwargs.items():
			setattr(self, key, value)

	def validate(self, obj, table):
		self.errors = {}
		for key, value in obj.items():
			if key != 'errors' and key != '_id':
				obj_key = getattr(self, key).object_key
				attr = getattr(self, key)
				if attr.is_required: self.check_required(obj_key, key, value)
				if attr.is_unique: self.check_unique(obj_key, key, value, table)
		print(self.errors)

	def check_required(self, obj_key, key, value):
		if value == '' or value == None:
			self.errors[obj_key] = 'Value required for {}'.format(key)

	def check_unique(self, obj_key, key, value, table):
		result = list(table.find({ key: value }))
		if len(result) > 0:
			self.errors[obj_key] = 'Value "{}" for {} is already in use'.format(value, key)