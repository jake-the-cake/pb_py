class Field:
	
	types = {
		'form_data': [
			'string',
			'integer',
			'float',
			'boolean',
			'email',
			'phone'
		],
		'relational': [
			'table'
		],
		'date_time': [
			'date',
			'time',
		]
	}

	def __init__(self, type, args) -> None:

		all_types = [item for sublist in Field.types.values() for item in sublist]
		form_data, relational, date_time = Field.types.values()
		
		self.error = None
		self.object_key = ''

		# verify that a valid field type is being used
		if type not in all_types:
			self.error = ValueError('Invalid Field Type')

		self.type = type
		
		# set defaults
		self.max_length = 50
		self.is_unique = False
		self.is_required = False
		self.value = None

		if type in relational:
			print(type(args[0]))
			self.object_key = '' + args[0].__name__

		if type in form_data:
			if len(args) < 1:
				self.error = KeyError('Object Key Is Required')
			else:
				self.object_key = args[0]
				
				#set a max_length if provided
				if len(args) > 1 and isinstance(args[1], int):
					self.max_length = args[1]

		# elif type == 'table':
		# 	pass
		# elif type == 'date' or type == 'time':
		# 	pass
		# # verify that an object key was provided
		# # verify that the object key is a string
		# elif not isinstance(args[0], str):
		# 	self.error = TypeError('Object Key Must Be A String')
		
		# else:
		
			# set the field type

			# set the objecy_key
			# self.object_key = args[0]


		# for dev testing
		if self.error: print(self.error)
		print(self)

	def required(self):
		if not self.error:
			self.is_required = True
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
	
	@staticmethod
	def DateField(*args):
		return Field('date', args)
	
	@staticmethod
	def TimeField(*args):
		return Field('time', args)
	
	@staticmethod
	def TableField(*args):
		return Field('table', args)
	
	def __str__(self) -> str:
		return str(self.__dict__)
	
StringField = Field.StringField
IntegerField = Field.IntField
BooleanField = Field.BoolField
FloatField = Field.FloatField
EmailField = Field.EmailField
PhoneField = Field.PhoneField
DateField = Field.DateField
TimeField = Field.TimeField
TableField = Field.TableField