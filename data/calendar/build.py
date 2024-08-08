import json

# This file is used to generate a JSON file that is used by the app to build calendars

# ------------------------ #
# -FUNCTIONS-------------- #
# ------------------------ #
def feb_day_count(year: int) -> int:
	if year % 4 == 0:
		if year % 100 or year % 400 == 0: return 29
	return 28

def base_7(number: int) -> int:
	return number % 7

def next_month_first_day(day: int, change: int) -> int:
	next_day = base_7(day + change)
	if next_day == 0: next_day = 7
	return next_day

# ------------------------ #
# -CONTANTS--------------- #
# ------------------------ #
DAYS = {
	'1': ['su', 'sun', 'sunday'],
	'2': ['mo', 'mon', 'monday'],
	'3': ['tu', 'tue', 'tuesday'],
	'4': ['we', 'wed', 'wednesday'],
	'5': ['th', 'thu', 'thursday'],
	'6': ['fr', 'fri', 'friday'],
	'7': ['sa', 'sat', 'saturday'],
}

MONTHS = {
	'01': ['jan', 'january', 31],
	'02': ['feb', 'february', feb_day_count],
	'03': ['mar', 'march', 31],
	'04': ['apr', 'april', 30],
	'05': ['may', 'may', 31],
	'06': ['jun', 'june', 30],
	'07': ['jul', 'july', 31],
	'08': ['aug', 'august', 31],
	'09': ['sep', 'september', 30],
	'10': ['oct', 'october', 31],
	'11': ['nov', 'november', 30],
	'12': ['dec', 'december', 31]
}

DAY_ONE = { 'weekday': 2,	'year': 2024 }
THROUGH_YEAR = 2040

# ------------------------ #
# -USE-DATA--------------- #
# ------------------------ #
def use_calendar(year = None, month = None):
	with open('data/calendar/calendar.json', 'r') as file:
		data = json.load(file)
	
	for m in MONTHS:
		MONTHS[m][2] = ''

	calendar = {
		"months": MONTHS,
		"days": DAYS,
		"data": data
	}
	return calendar

# ------------------------ #
# -MAIN------------------- #
# ------------------------ #
def main():

	data = {}
	filename = 'data/calendar/calendar.json'

	year = DAY_ONE['year']
	weekday = DAY_ONE['weekday']

	while year <= THROUGH_YEAR:
		# empty dictionary to populate month info
		details = {}
		
		# loop through and add each months data
		for num, txt in MONTHS.items():
			# get number of days from dictionary
			num_days = txt[2]
			# determine number of days in feb
			if callable(num_days): num_days = num_days(year)
			
			# pick out the weekends
			weekends = []
			sat = 7 - weekday	+ 1
			def add_weekend(sat, sun):
				weekend = [num for num in [sat, sun] if num <= num_days]
				weekends.append(weekend)
				sat += 7
				if sat <= num_days: add_weekend(sat, sat + 1)
			add_weekend(sat, sat + 1)

			# construct data for the month
			details[str(num)] = {
				'days': num_days,
				'first': weekday,
				'weekends': weekends
			}

			# update the first day for next month
			weekday = next_month_first_day(weekday, num_days)

		# add the months into the year, and increment
		data[str(year)] = details
		year += 1

	# save to file
	with open(filename, 'w') as file:
		json.dump(data, file, indent = 2)

if __name__ == '__main__':
	main()