from models.mongo.models import User

class Update:
    @staticmethod
    def update_user_data(message):
        user = User.objects.filter(user_id=message.from_user.id).get()
        user.username = message.from_user.username
        user.first_name = message.from_user.first_name
        user.last_name = message.from_user.last_name
        user.save()
