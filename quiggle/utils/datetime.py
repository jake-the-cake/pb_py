import datetime

def int_or_none(value):
	if value == None: return value
	return int(value)

def str_or_none(value):
	if value == None: return value
	return str(value)

class Time:

	format_lengths = {
		'hour': 2,
		'minute': 2,
		'second': 2,
		'milli': 3,
	}

	def __init__(self) -> None:
		pass

class Date:

	format_lengths = {
		'day': 2,
		'month': 2,
		'year': 4
	}

	def __init__(self, day = None, month = None, year = None) -> None:
		self.day = day
		self.month = month
		self.year = year
		self.format_values()

	def format_values(self):
		for key, value in self.format_lengths.items():
			formatted_value = str_or_none(self.trim_values(getattr(self, key), value))
			setattr(self, key, formatted_value)

	def trim_values(self, value: str, length: int):
		value = str(value)
		if value == 'None': return None
		if len(value) == length: return str(value)
		if len(value) < length: return self.to_string_with_len(value, length)
		if len(value) > length: return str(value[:2])

	def to_string_with_len(self, value, length):
		return '{:0>{width}}'.format(value, width = length)

	def from_date_code(self, code: str | int) -> None:
		code = str(code)
		if len(code) != 8: raise ValueError('Date code must be 8 characters/digits long.')
		if int(code) * 0 != 0: raise TypeError('Date code must contain only numeric characters.')
		self.day = code[:2]
		self.month = code[2:4]
		self.year = code[4:8]
		self.format_values()
		return self

	def previous_year(self):
		if self.year != None: return int(self.year) - 1
	
	def next_year(self):
		if self.year != None: return int(self.year) + 1
	
	def previous_month(self):
		if self.month != None:
			if self.month == '01':
				return '12' + str(self.previous_year())
			return self.to_string_with_len(int(self.month) - 1, 2) + self.year

x = Date(1, 1, 2012)
y = Date().from_date_code(11122024)
z = Date().next_year()

print(vars(x))
print(vars(y))
print(y.previous_year())
print(y.next_year())
print(y.previous_month())
print(x.previous_month())