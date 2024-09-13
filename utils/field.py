# from typing import Self
from utils.color import log_bug
from utils.quiggle import Quiggle
from utils.number import Number

Self = str
allowed_field_type = str | bool | int | None
kwargs_type = dict[str, allowed_field_type]

# the base Field class contains common methods
# validates each piece of data going into db
# parses each piece of data from the db

class Field(Quiggle):

	def __init__(self: Self, field_type: str, kwargs: kwargs_type) -> None:
		super().__init__()

		# set default props
		self.key: str = None
		self.is_required: bool = False
		self.is_unique: bool = False
		self.default_value: allowed_field_type = None
		self.max_length: int = 100
		self.min_length: int = 0
		self.value: allowed_field_type = None
		self.init_parse_rules()

		# fill in props based on input
		self.field_type: str = field_type
		self.use_options(kwargs)

	# ------------
	# init methods
	# ------------

	# set the valid parse rules
	def init_parse_rules(self: Self) -> None:
		self.parse_rules = {}

	# set the corresponding is_ props
	def required(self: Self) -> Self:
		self.is_required = True
		return self
	def unique(self: Self) -> Self:
		self.is_unique = True
		return self

	# change the allowed value lengths
	def min(self: Self, length: int) -> Self:
		self.min_length = length
		return self
	def max(self: Self, length: int) -> Self:
		self.max_length = length
		return self
	
	# store a default value to use if none is given
	def default(self: Self, value) -> None:
		self.default_value = value
		return self

	# update the value and string_value
	def set_value(self: Self, value: allowed_field_type) -> None:
		self.value = value
		self.stringify()

	# update the value with the deafult_value
	def use_default(self: Self) -> None:
		self.set_value(self.default_value)

	# set the valid parse rules for the field type
	def load_options(self: Self, options: kwargs_type, valid_options: list[str]) -> None:
		for opt in valid_options:
			if opt in options:
				self.parse_rules[opt] = options[opt]

	# fallback method - only prints a bug message
	def use_options(self: Self, _: kwargs_type) -> None:
		self.tools.default_method_log(self, 'use_options')

	# ---------END init methods

	# ------------
	# read methods
	# ------------

	def set_string_value(self: Self, value: str) -> None:
		self.string_value = value

	def parse(self: Self) -> None:
		if self.field_type == 'text': 
			self.set_value(self.string_value)
		else: self.translate() # need a try statement

	# ---------END read methods

	# -------------
	# write methods
	# -------------

		# fallback content validation method on incoming data
	def validate(self: Self) -> None:
		self.tools.default_method_log(self, 'validate')

		# string version of a variable to store in db
	def stringify(self: Self) -> None:
		if not self.value: self.value = ''
		self.string_value = str(self.value)

	# ----------END write methods
# =======================================================END field class

# ----------------
# root field types
# ----------------

# ----------------
	# text
class Text_Field(Field):
	def __init__(self: Self, **kwargs) -> None:
		super().__init__('text', kwargs)

	def use_options(self: Self, options: kwargs_type) -> None:
		self.load_options(options, [
			'keep_case'
		])

	def validate(self: str) -> None:
		if self.field_type != 'text': super().validate()
		if self.value != self.string_value:
			self.errors[self.key] = 'Value is not a string.'

	def translate(self: Self) -> None:
		if self.field_type != 'text':
			self.tools.default_method_log(self, 'use_options')

# ----------------
	# number
class Number_Field(Field):
	def __init__(self: Self, **kwargs: kwargs_type) -> None:
		super().__init__('number', kwargs)
		if not hasattr(self.parse_rules, 'round'): self.parse_rules['round'] = 'auto'
		if not hasattr(self.parse_rules, 'number_type'): self.parse_rules['number_type'] = 'float'
		if not hasattr(self.parse_rules, 'deicmals'): self.parse_rules['decimals'] = None

	def use_options(self: Self, options: kwargs_type) -> None:
		self.load_options(options, [
			'round',
			'number_type',
			'decimals'
		])

	def translate(self: Self) -> None:
		number = Number(self.string_value)
		if self.parse_rules['number_type'] == 'int':
			self.set_value(number.value.int)
		elif self.parse_rules['number_type'] == 'float' and int(self.parse_rules['decimals'] or 0) > Number.get_decimal_length(number.value.float):
			self.set_value(number.value.str_float)
		else:
			self.set_value(number.value.float)

# ----------------
	# key
class Key_Field(Field):
	def __init__(self: Self, **kwargs: kwargs_type) -> None:
		super().__init__('key', kwargs)

	def translate(self):
		pass

# ----------------
	# boolean
class Boolean_Field(Field):
	def __init__(self: Self, **kwargs: kwargs_type) -> None:
		super().__init__('bool', kwargs)
	
	def translate(self: Self) -> None:
		if self.string_value == 'True': self.value = True
		if self.string_value == 'False': self.value = False

# ----------------
	# list
class List_Field(Field):
	def __init__(self: Self, **kwargs: kwargs_type) -> None:
		super().__init__('list', kwargs)
		self.value = []
	
	def translate(self: Self) -> None:
		pass

# ----------------
	# retlational
class Relational_Field(Field):
	def __init__(self: Self, table: any, **kwargs: kwargs_type) -> None:
		super().__init__('rel', kwargs)
		self.table_name = table.__class__.__name__
		self.table = table

# -------------END root field types



# ----------------------------------
# special fields that are text-based
# ----------------------------------

# ----------------------------------
	# emails
class Email_Field(Text_Field):
	def __init__(self: Self, **kwargs: kwargs_type) -> None:
		super().__init__(**kwargs)
		self.field_type = 'email'

# ----------------------------------
	# phone numbers
class Phone_Field(Text_Field):
	def __init__(self: Self, **kwargs: kwargs_type) -> None:
		super().__init__(**kwargs)
		self.field_type = 'phone'

# ----------------------------------
	# dates
class Date_Field(Text_Field):
	def __init__(self: Self, **kwargs: kwargs_type) -> None:
		super().__init__(**kwargs)
		self.field_type = 'date'

	def use_options(self: Self, options: kwargs_type) -> None:
		super().use_options(options)

# -------------------------------END special text fields