from datetime import datetime as dt
from orm import Model, DateTime, String, Integer, ModelRegistry

from objects.globals import db

models  = ModelRegistry(database=db)


class User(Model):
    tablename = "users"
    registry = models

    fields = {
        "id": Integer(primary_key=True),
        "user_id": Integer(),
        "username": String(max_length=255, allow_null=True),
        "first_name": String(max_length=255, allow_null=True),
        "last_name": String(max_length=255, allow_null=True),
        "joined": DateTime(default=dt.now()),
        "download_count": Integer()
    }

    def __repr__(self):
        return "<Id=%s, UserId=%s>" % (self.id, self.user_id,)