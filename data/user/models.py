from api.field import Text_Field, Email_Field, Number_Field
from api.model import Model

class User(Model):

	first_name = Text_Field().required()
	last_name = Text_Field()
	email = Email_Field().required().unique()
	age = Text_Field()
	security_level = Number_Field().default(5)
	password = Text_Field()