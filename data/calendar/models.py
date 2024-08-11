from utils.controller import ApiController
from utils.field import StringField, DateField, TimeField
from utils.model import Model

class Event(ApiController):
	
	def __init__(self, security_level = 5) -> None:
		super().__init__('event', security_level)

	def use_model(self):
		self.model = Model(
			title = StringField('title', 20).required(),
			start_date = DateField('start-date').required(),
			end_date = DateField('end-date'),
			start_time = TimeField('start-time').required(),
			end_time = TimeField('end-time'),
		)
		return self.model