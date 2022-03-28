from datetime import datetime as dt

from mongoengine import *

connect("download_bot")

class User(Document):
    user_id = IntField()
    username = StringField(max_length=255, default=None)
    first_name = StringField(max_length=255, default=None)
    last_name = StringField(max_length=255, default=None)
    date_joined = DateTimeField(default=dt.utcnow)
    download_count = IntField(default=0)