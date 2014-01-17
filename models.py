from mongoengine import *
from mongoengine.errors import ValidationError

connect('e-learning') #connect ke databases
import datetime

GENDER =(
	('F', 'Female'),
        ('M', 'Male')
        )

class User(Document):
	_id = StringField(primary_key=True)
	username = StringField(max_length=150, required=True)
	fullname = StringField(max_length=200, required=True)
	email = EmailField(unique=True, required=True)
	password = StringField(required=True)
	birthday = DateTimeField(required=True)
	gender = StringField(max_length=1, choices=GENDER, required=True)
	date_joined = DateTimeField()

class Profile(Document):
	author = ReferenceField(User)
	alamat = StringField(max_length=80)
	phone = IntField()
	website = StringField(max_length=80)
	date_added = DateTimeField()
	cv_url = StringField()
	profile_images_url = StringField(max_length=300)	
	meta = {'allow_inheritance': True}
	

		


