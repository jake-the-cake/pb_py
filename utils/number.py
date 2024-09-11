from utils.quiggle import Quiggle

class Number(Quiggle):

	def __init__(self, number: float | int | str, **kwargs):
			
			# inits
		super().__init__()
		self.options = {}
		self._update_options(kwargs)
			
			# autovars
		self.number_type = 'float'
		self.original_value = number
			
			# set values
		try: self._update_values(float(number))
		except Exception as e: print('@ Number init ->', e)

	def _update_values(self, value) -> None:
		self.value = value
		self.string_value = self._check_trailing_zeros(self.value)

	def _update_options(self, options):
		for key in options.keys(): self.options[key] = options.get(key)

	def _check_trailing_zeros(self, value) -> str:
		split_value = str(value).split('.')
		if len(split_value) == 2:
			v, val = split_value
			diff = self.options.get('decimals') - len(val)
			while diff > 0:
				val += '0'
				diff -= 1
			value = '.'.join([v, val])
		return value

	def _round_number(self):
			# vars for number of decimals and the rounding method
		decimals = self.options.get('decimals', None)
		rounding_method = self.options.get('round', 'auto')
			# No rounding if decimals is not specified, or if needing trailing 0's
		if decimals is None or decimals > self.get_decimal_length():
			self._update_values(float(self.value))
			return
			# Apply rounding based on the specified method
		if rounding_method == 'up':
			factor = 10 ** decimals
			self._update_values((int(self.value * factor) + 1) / factor)
		elif rounding_method == 'down':
			factor = 10 ** decimals
			self._update_values(int(self.value * factor) / factor)
		elif rounding_method == 'auto':
			self._update_values(round(self.value, decimals))
		else:
			raise ValueError("Invalid rounding method. Choose 'up', 'down', or 'auto'.")

		# callable methods
	def make_int(self, **kwargs):
		self._update_options(kwargs)
		self.number_type = 'int'
		self.options['decimals'] = 0
		self._round_number()
		self._update_values(int(self.value))
		return self
	
	def make_float(self, **kwargs):
		self._update_options(kwargs)
		self.number_type = 'float'
		self._round_number()
		return self
	
		# return the length of the decimal places for the value
	def get_decimal_length(self) -> int:
		return len(str(float(self.value)).split('.')[1])