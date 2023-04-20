from hashlib import md5
from uuid import uuid4

from flask import Flask, jsonify, render_template, redirect, request, session
from flask_login import LoginManager, login_user, current_user
from forms.LoginForm import LoginForm

from models.mongo.models import *

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

SECRET_KEY = str(uuid4())
app.config['SECRET_KEY'] = SECRET_KEY

@login_manager.user_loader
def load_user(email, password):
    password = md5(password.encode()).hexdigest()
    return Admins.objects.get(email=email, password=password)

@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in') == True:
        return render_template("index.html", content='Test')
    else:
        return redirect('auth')

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

@app.route('/auth', methods=['GET', 'POST'])
def auth_user():
    if not session.get('logged_in'):
        print(request.get_data())
        form = LoginForm()
        if form.validate_on_submit():
            email = request.form.get('email')
            password = request.form.get('password')
            user = load_user(email, password)
            login_user(user)
            session['logged_in'] = True
            return redirect('/')
        return render_template("auth.html", form=form)
    else:
        return redirect('/')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect('/')

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
