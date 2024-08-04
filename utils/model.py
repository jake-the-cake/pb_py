class Model:

	def __init__(self, **kwargs):
		for key, value in kwargs.items():
			setattr(self, key, value)

	def validate(self, obj, table):
		self.errors = {}
		for key, value in obj.items():
			if key != 'errors' and key != '_id':
				self.check_required(key, value)
				self.check_unique( key, value, table)

	def check_required(self, key, value):
		if value == '' or None:
			self.errors[key] = 'Value required for {}'.format(key)

	def check_unique(self, key, value, table):
		attr = getattr(self, key)
		if attr.is_unique:
			result = list(table.find({ key: value }))
			if len(result) > 0:
				self.errors[key] = 'Value "{}" for {} is already in use'.format(value, key)