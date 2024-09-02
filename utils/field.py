# from typing import Self
from utils.color import log_bug
from utils.quiggle import Quiggle

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

	# set the value from input or default
	def set_value(self: Self, value: allowed_field_type) -> None: self.value = value
	def use_default(self: Self) -> None: self.value = self.default_value

	# set the valid parse rules for the field type
	def load_options(self: Self, options: kwargs_type, valid_options: list[str]) -> None:
		for opt in valid_options:
			if opt in options: self.parse_rules[opt] = options[opt]

	# fallback method - only prints a bug message
	def use_options(self: Self, _: kwargs_type) -> None:
		log_bug(' - Field class "{}" has no use_options method - '.format(self.__class__.__name__))

	# ---------END init methods

	# ------------
	# read methods
	# ------------

	def set_string_value(self: Self, value: str) -> None:
		self.string_value = value

	def parse(self: Self) -> None:
		if self.field_type == 'text': self.value = self.string_value
		else: self.translate() # need a try statement

	# ---------END read methods

	# -------------
	# write methods
	# -------------

		# fallback validation method on incoming data
	def validate(self: Self) -> None:
		self.tools.default_method_log(self, 'validate')

		# string version of a variable to store in db
	def stringify(self: Self) -> None:
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

# ----------------
	# number
class Number_Field(Field):
	def __init__(self: Self, **kwargs: kwargs_type) -> None:
		super().__init__('number', kwargs)

	def use_options(self: Self, options: kwargs_type) -> None:
		self.load_options(options, [
			'round_int',
			'number_type'
		])

	def translate(self: Self) -> None:

			# set error messages
		conversion_err = ValueError('Value cannot be converted to a number.')
		format_err = ValueError('Expected int, but received float. Use "round_int" option to convert "up" or "down".')

		# ----- FLOAT/INT OPTION -----
			# set variables
		dot_count = len(self.string_value.split('.')) - 1
		allowed_dots = 999

			# verify that it can be converted
		if dot_count > 1 or dot_count < 0: raise conversion_err

		def check_whole_number_float(value: str):
			split_value = value.split('.')
			if (len(split_value) == 2):
				for num in split_value[1]:
					if num != '0': return
				self.string_value = str(split_value[0])
			if 'round_int' in self.parse_rules:
				int_value = int(self.string_value.split('.')[0])
				round_int_rule = self.parse_rules['round_int']
				if round_int_rule == 'up':
					self.value = int_value + 1
					return
				if round_int_rule == 'down':
					self.value = int_value
					return
			raise format_err

		check_whole_number_float(self.string_value)

			# option to set output to float or int
		if 'number_type' in self.parse_rules:
			type = self.parse_rules['number_type']
			if type == 'float': allowed_dots = 1
			if type == 'int': allowed_dots = 0
		
			# if there are no dots in the mumber, and its not specified as a float, make int
		if dot_count == 0 and allowed_dots != 1: self.value = int(self.string_value)
			# return a float if specified
		elif allowed_dots == 1: self.value = float(self.string_value)
			# if there is one dot, but specified as an int, raise error unless round_int option is valid
		else: check_whole_number_float(self.string_value)
		# -------------------------END float/int option



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