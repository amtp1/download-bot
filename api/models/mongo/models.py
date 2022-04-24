from datetime import datetime as dt

from mongoengine import *

from uuid import uuid4

connect("download_bot")

class UserQuerySet(QuerySet):
    def update(self, user_id: str, fields: dict):
        update_document = self.filter(user_id=user_id).modify(
            new=True, **fields
        )

        if not update_document:
            raise ("Wrong user id =>", user_id)
        return update_document

class DesktopSessionSet(QuerySet):
    def update(self, user_email: str, fields: dict):
        update_document = self.filter(user_email=user_email).modify(
            new=True, **fields
        )

        if not update_document:
            raise ("Wrong user email =>", user_email)
        return update_document

class User(Document):
    user_id = IntField()
    username = StringField(max_length=255, default=None)
    first_name = StringField(max_length=255, default=None)
    last_name = StringField(max_length=255, default=None)
    date_joined = DateTimeField(default=dt.utcnow)
    download_count = IntField(default=0)

    meta = {"queryset_class": UserQuerySet}

    def serialize(self):
        return dict(
            id=str(self.id), user_id=self.user_id,
            username=self.username, first_name=self.first_name,
            last_name=self.last_name, date_joined=self.date_joined,
            download_count=self.download_count
            )

class DesktopSession(Document):
    session_id = StringField(unique=True, max_length=255, default=str(uuid4()))
    user_email = StringField(max_length=255, default=None)
    created = DateTimeField(default=dt.utcnow)

    meta = {"queryset_class": DesktopSessionSet}

class Admins(Document):
    email = StringField(max_length=255)
    password = StringField(max_length=255)
    date_joined = DateTimeField(default=dt.utcnow)