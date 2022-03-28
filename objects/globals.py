from models.mongo.models import *

metadata = None
db_engine = None

config: dict = {}

def update_download_count(user_id: int):
    user = User(user_id=user_id)
    user.download_count = user.download_count + 1
    user.save()