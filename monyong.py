from mongoengine import *
connect('monyong') #connect ke databases

class User(Document):
    name = StringField()

class Page(Document):
    content = StringField()
    author = ReferenceField(User)
