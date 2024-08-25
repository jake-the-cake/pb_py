from utils.field import Text_Field, Email_Field, Number_Field
from utils.model import Model
from utils.controller import ApiController

class User(ApiController):

	def __init__(self, security_level = 5) -> None:
		super().__init__('user', security_level)

	def use_model(self):
		return Model(
			first_name = Text_Field().required(),
			last_name = Text_Field(),
			email = Email_Field().required().unique(),
			age = Text_Field(),
			security_level = Number_Field().default(),
			password = Text_Field()
		)