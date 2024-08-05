from utils.field import StringField, EmailField, IntegerField
from utils.model import Model
from utils.controller import ApiController

class User(ApiController):

	def __init__(self, security_level = 5) -> None:
		super().__init__('user', security_level)

	def use_model(self):
		return Model(
			first_name = StringField('first-name', 20).required(),
			last_name = StringField('last-name', 20),
			email = EmailField('email', 30).required().unique(),
			age = StringField('age', 3),
			security_level = IntegerField('security-level', 1).default(4),
			password = StringField('password', 100)
		)