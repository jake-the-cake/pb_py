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

	def __init__(self, type = None, *args) -> None:

		self.error = None
		self.object_key = ''
		self.value = None

		if not type:
			self.type = ''
			return

		all_types = [item for sublist in Field.types.values() for item in sublist]
		form_data, relational, date_time = Field.types.values()
		

		# verify that a valid field type is being used
		if type not in all_types:
			self.error = ValueError('Invalid Field Type')

		self.type = type
		

		if type in relational:
			
			key = '_id'
			self.value_data = ''
			
			for i, value in enumerate(args):
				name = str(args[0].__name__).lower()
				if i == 0:
					self.value = name
				if i == 1:
					if value == 'one':
						self.value_data = '__'
					else: self.value_data = '[__]'
				if i == 2:
					key = value
				self.value = '::'.join([name, key, str(self.value_data)])
			self.object_key = name

		elif type in form_data:
			
			# set defaults
			self.max_length = 50
			self.is_unique = False
			self.is_required = False
			
			# verify that an object key was provided
			if len(args) < 1:
				self.error = KeyError('Object Key Is Required')
			# verify that the object key is a string
			elif not isinstance(args[0], str):
				self.error = TypeError('Object Key Must Be A String')
			else:
				self.object_key = args[0]
				
				# set a max_length if provided
				if len(args) > 1 and isinstance(args[1], int):
					self.max_length = args[1]
		
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

	def use_table(self):
		pass

	@staticmethod
	def StringField(*args):
		return Field('string', *args)
	
	@staticmethod
	def FloatField(*args):
		return Field('float', *args)
	
	@staticmethod
	def IntField(*args):
		return Field('integer', *args)
	
	@staticmethod
	def BoolField(*args):
		return Field('boolean', *args)
	
	@staticmethod
	def EmailField(*args):
		return Field('email', *args)
	
	@staticmethod
	def PhoneField(*args):
		return Field('phone', *args)
	
	@staticmethod
	def DateField(*args):
		return Field('date', *args)
	
	@staticmethod
	def TimeField(*args):
		return Field('time', *args)
	
	@staticmethod
	def TableField(table, type, key = '_id'):
		return Field('table', table, type, key)
	
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