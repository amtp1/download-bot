from uuid import uuid4

from flask import Flask, jsonify, render_template

from models.mongo.models import *
from models.mongo.models import Admins
from models.mongo.models import DesktopSession

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", content='Test')

@app.route('/users', methods=['GET'])
def users():
    users = []
    for user in User.objects.all():
        user_download = Download.objects.filter(user=user)
        if user_download:
            user.download_count = user.download_count + len(user_download.all())
        users.append(user)
    return render_template('users.html', users=users, downloads=downloads)

@app.route('/downloads', methods=['GET'])
def downloads():
    downloads = [download.serialize() for download in Download.objects.all()]
    return render_template('downloads.html', downloads=downloads)

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    users = User.objects.all()
    serialize_users = [user.serialize() for user in users]
    return jsonify({'users': serialize_users})

@app.route('/api/v1/auth/<email>/<password>', methods=['GET'])
def auth(email, password):
    admin = Admins.objects.filter(email=email, password=password)

    if not admin:
        return jsonify({'token': ''})
    else:
        desktop_session = DesktopSession.objects.filter(user_email=email)
        if not desktop_session:
            DesktopSession.objects.create(user_email=email)
        else:
            generate_token: str = str(uuid4())
            desktop_session = desktop_session.first()
            update_fields = {"session_id": generate_token}
            DesktopSession.objects.update(email, update_fields)
            return jsonify({'token': generate_token})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
