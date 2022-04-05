from datetime import datetime as dt

from mongoengine import *

connect("download_bot")


class CommonQuerySet(QuerySet):
    def update_by_user_id(self, user_id: str, fields: dict):
        update_document = self.filter(user_id=user_id).modify(
            new=True, **fields
        )

        if not update_document:
            raise ("Wrong user id =>", user_id)
        return update_document

class User(Document):
    user_id = IntField()
    username = StringField(max_length=255, default=None)
    first_name = StringField(max_length=255, default=None)
    last_name = StringField(max_length=255, default=None)
    date_joined = DateTimeField(default=dt.utcnow)
    download_count = IntField(default=0)
    meta = {"queryset_class": CommonQuerySet}