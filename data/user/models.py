from utils.model import StringField, EmailField, Model
from utils.controller import ApiController

class User(ApiController):

	def __init__(self, security_level = 5) -> None:
		print(security_level)
		super().__init__('user', security_level)

	def use_model(self):
		return Model(
			first_name = StringField('first-name', 20).required(),
			last_name = StringField('last-name', 20),
			email = EmailField('email', 30).required().unique(),
			age = StringField('age', 3)
		)