from models.mongo.models import *

metadata = None
db_engine = None

config: dict = {}

def update_download_count(user_id: int):
    user = User.objects(user_id=user_id).first()
    update_fields = {"download_count": user.download_count+1}
    User.objects.update_by_user_id(user.user_id, update_fields)