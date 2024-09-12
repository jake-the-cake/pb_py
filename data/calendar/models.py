from utils.field import Text_Field, Date_Field, Relational_Field, List_Field
from utils.model import Model
from data.user.models import User

class Event(Model):
	
	title = Text_Field(keep_case = True).required().unique()
	start_date = Date_Field().required().min(80)
	end_date = Date_Field().default('test').max(1)
	start_time = Date_Field().required()
	end_time = Date_Field()
	invites = List_Field()

class Calendar(Model):

	user = Relational_Field(User)
	created_events = Relational_Field(Event)
	invites = List_Field()