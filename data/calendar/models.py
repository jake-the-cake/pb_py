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

class Calendar(ApiController):

	user = Relational_Field(Event)
	created_events = Relational_Field(Event)
	attending = Relational_Field(Event)
	invites = Relational_Field(Event)