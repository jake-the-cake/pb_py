from utils.controller import ApiController
from utils.field import StringField, DateField, TimeField, TableField
from utils.model import Model
from data.user.models import User

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
	
class Calendar(ApiController):

	def __init__(self, security_level = 5) -> None:
		super().__init__('calendar', security_level)

	def use_model(self):
		self.model = Model(
			user = TableField(User, 'one'),
			created_events = TableField(Event, 'many'),
			attending = TableField(Event, 'many'),
			invites = TableField(Event, 'many')
		)