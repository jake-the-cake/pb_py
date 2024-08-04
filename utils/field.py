class Field:
	
	types = [
		'string',
		'integer',
		'float',
		'boolean',
		'email',
		'phone'
	]

	def __init__(self, type, args) -> None:

		# verify that a valid field type is being used
		if type not in Field.types:
			self.error = ValueError('Invalid Field Type')
		# verify that an object key was provided
		elif len(args) < 1:
			self.error = KeyError('Object Key Is Required')
		# verify that the object key is a string
		elif not isinstance(args[0], str):
			self.error = TypeError('Object Key Must Be A String')
		else:
			self.error = None
		
			# set the field type
			self.type = type

			# set the objecy_key
			self.object_key = args[0]
			self.__name__ = self.object_key

			# set defaults
			self.max_length = 50
			self.is_unique = False
			self.is_reqired = False
			self.value = None

			# set a max_length if provided
			if len(args) > 1 and isinstance(args[1], int):
				self.max_length = args[1]
		if self.error: print(self.error)

	def required(self):
		if not self.error:
			self.is_reqired = True
		return self
	
	def unique(self):
		if not self.error:
			self.is_unique = True
		return self
	
	def default(self, value):
		if not self.error:
			self.value = value
		return self

	@staticmethod
	def StringField(*args):
		return Field('string', args)
	
	@staticmethod
	def FloatField(*args):
		return Field('float', args)
	
	@staticmethod
	def IntField(*args):
		return Field('integer', args)
	
	@staticmethod
	def BoolField(*args):
		return Field('boolean', args)
	
	@staticmethod
	def EmailField(*args):
		return Field('email', args)
	
	@staticmethod
	def PhoneField(*args):
		return Field('phone', args)
	
	def __str__(self) -> str:
		return self.object_key

StringField = Field.StringField
IntegerField = Field.IntField
BooleanField = Field.BoolField
FloatField = Field.FloatField
EmailField = Field.EmailField
PhoneField = Field.PhoneField