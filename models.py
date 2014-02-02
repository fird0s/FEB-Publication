from mongoengine import *
from mongoengine.errors import ValidationError, NotUniqueError, DoesNotExist

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
	phone = StringField(max_length=20)
	emergency_call = StringField(max_length=20)
	website = StringField(max_length=80)
	date_added = DateTimeField()
	cv_url = StringField()
	profile_images_url = StringField(max_length=300)	
	password_jurnal = StringField(max_length=100)
	about = StringField(max_length=2000)
	meta = {'allow_inheritance': True}
	
class Kategori(Document):
	nama = StringField(max_length=50)
	about_category = StringField()
	date_added = DateTimeField()

class Jurnal(Document):
	author = ReferenceField(User)
	jurnal_name = StringField(max_length=500)
	jurnal_location = StringField(max_length=100)
	date_added = DateTimeField()
	kategori = StringField(max_length=100)
	summary = StringField(max_length=2000)
	

	
	
		


