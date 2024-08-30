from utils.controller import ApiController
from utils.field import Text_Field, Date_Field, Relational_Field
from utils.model import Model
from data.user.models import User

class Event(Model):
	
	title = Text_Field(keep_case = True).required()
	start_date = Date_Field().required()
	end_date = Date_Field()
	start_time = Date_Field().required()
	end_time = Date_Field()

# Event(title = 'Title')
	
class Calendar(ApiController):

	def __init__(self, security_level = 5) -> None:
		super().__init__('calendar', security_level)

	def use_model(self):
		self.model = Model(
			user = Relational_Field(),
			created_events = Relational_Field(),
			attending = Relational_Field(),
			invites = Relational_Field()
		)