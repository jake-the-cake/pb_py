from quiggle.features.quiggle import Quiggle
from quiggle.features.value_store import Value_Store

class Number(Quiggle):

	def __init__(self, number: float | int | str, **kwargs):
		super().__init__()
		self.options = {}
		self._update_options(kwargs)
		
		store: Value_Store = Value_Store()
		store.int = None
		store.float = None
		store.str_int = None
		store.str_float = None
		store.original = number
		self.value = store

		try: self._update_values(number)
		except Exception as e: print('@ Number init ->', e)

	def _update_values(self, value) -> None:
		self.value.int = self.make_int(value)
		self.value.float = self.make_float(value)
		self.value.str_int = self._check_trailing_zeros(self.value.int, 0)
		self.value.str_float = self._check_trailing_zeros(self.value.float, self.options.get('decimals', None))

	def _update_options(self, options):
		for key in options.keys(): self.options[key] = options.get(key)

	def _check_trailing_zeros(self, value, decimals: int) -> str:
		split_value = str(value).split('.')
		if len(split_value) == 2:
			v, val = split_value
			diff = int(decimals) - len(val)
			while diff > 0:
				val += '0'
				diff -= 1
			value = '.'.join([v, val])
		return str(value)
	
		# return the length of the decimal places for the value
	@staticmethod
	def get_decimal_length(value) -> int:
		if not value: value = 0
		return len(str(float(value)).split('.')[1])
	
	@staticmethod
	def round_number(value, decimals: int = None, method: str = 'auto'):
			# No rounding if decimals is not specified, or if needing trailing 0's
		if decimals is None or decimals > Number.get_decimal_length(value):
			return float(value)
			# Apply rounding based on the specified method
		if method == 'up':
			factor = 10 ** decimals
			return int((value * factor) + 1) / factor
		elif method == 'down':
			factor = 10 ** decimals
			return int(value * factor) / factor
		elif method == 'auto':
			return round(value, decimals)
		else:
			raise ValueError("Invalid rounding method. Choose 'up', 'down', or 'auto'.")

		# callable methods
	def make_int(self, value) -> int:
		return int(Number.round_number(value, 0, self.options.get('round', 'auto')))
	
	def make_float(self, value) -> float:
		return Number.round_number(value, self.options.get('decimals', None), self.options.get('round', 'auto'))
	
	def values(self):
		return self.value.get_values()
	