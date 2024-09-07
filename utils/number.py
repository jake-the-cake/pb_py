# from quiggle import Quiggle

class Number:

	def __init__(self, number: float | int | str, **kwargs):
		super().__init__()
		self.value = number
		self.options = {}
		for key in	kwargs.keys(): self.options[key] = kwargs.get(key)

	def make_int(self, **kwargs):
		for key in	kwargs.keys(): self.options[key] = kwargs.get(key)
		self.value = int(self.value)
		return self
	
	def make_float(self, **kwargs):
		for key in	kwargs.keys(): self.options[key] = kwargs.get(key)
		self.value = float(self.value)
		if 'decimals' in self.options:
			val = str(self.value).split('.')
			if len(val) == 2:
				l_decimal = int(self.options['decimals'])
				l_val = len(val[1])
				diff = l_decimal - l_val
				if diff > 0:
					while diff > 0:
						print(diff)
						val[1] = val[1] + '0'
						diff -= 1
					self.value = '.'.join(val)
		return self

x = Number(88.25555, decimals = 3)
x.make_float()
print(x.value)

# allowed_dots = 999

# 	# verify that it can be converted
# if dot_count > 1 or dot_count < 0: raise conversion_err

# def check_whole_number_float(value: str):
# 	split_value = value.split('.')
# 	if (len(split_value) == 2):
# 		for num in split_value[1]:
# 			if num != '0': return
# 		self.string_value = str(split_value[0])
# 	if 'round_int' in self.parse_rules:
# 		int_value = int(self.string_value.split('.')[0])
# 		round_int_rule = self.parse_rules['round_int']
# 		if round_int_rule == 'up':
# 			self.value = int_value + 1
# 			return
# 		if round_int_rule == 'down':
# 			self.value = int_value
# 			return
# 	raise format_err

# check_whole_number_float(self.string_value)

# 	# option to set output to float or int
# if 'number_type' in self.parse_rules:
# 	type = self.parse_rules['number_type']
# 	if type == 'float': allowed_dots = 1
# 	if type == 'int': allowed_dots = 0

# 	# if there are no dots in the mumber, and its not specified as a float, make int
# if dot_count == 0 and allowed_dots != 1: self.value = int(self.string_value)
# 	# return a float if specified
# elif allowed_dots == 1: self.value = float(self.string_value)
# 	# if there is one dot, but specified as an int, raise error unless round_int option is valid
# else: check_whole_number_float(self.string_value)