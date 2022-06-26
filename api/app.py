from uuid import uuid4

from flask import Flask, jsonify, render_template

from models.mongo.models import *
from models.mongo.models import Admins
from models.mongo.models import DesktopSession


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", content="Test")

@app.route('/users', methods=['GET'])
def users():
    users = User.objects.all()
    return render_template("users.html", users=users)

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    users = User.objects.all()
    serialize_users = [user.serialize() for user in users]
    return jsonify({"users": serialize_users})

@app.route('/api/v1/auth/<email>/<password>', methods=['GET'])
def auth(email, password):
    admin = Admins.objects.filter(email=email, password=password)

    if not admin:
        return jsonify({"token": ""})
    else:
        desktop_session = DesktopSession.objects.filter(user_email=email)
        if not desktop_session:
            DesktopSession.objects.create(user_email=email)
        else:
            generate_token: str = str(uuid4())
            desktop_session = desktop_session.first()
            update_fields = {"session_id": generate_token}
            DesktopSession.objects.update(email, update_fields)
            return jsonify({"token": generate_token})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)