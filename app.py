
from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'jobs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    location = db.Column(db.String(100))
    user_id = db.Column(db.Integer)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# HOME
@app.route("/")
def home():
    jobs = Job.query.all()

    html = "<h2>Jobs</h2>"
    for job in jobs:
        html += f"<p>{job.title} - {job.location}</p>"

    return html


# REGISTER
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return "Registered successfully. Go to /login"

    return """
    <h2>Register</h2>
    <form method="post">
    <input name="username">
    <input name="password">
    <button>Register</button>
    </form>
    """


# LOGIN
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return "Login successful"

        return "Invalid login"

    return """
    <h2>Login</h2>
    <form method="post">
    <input name="username">
    <input name="password">
    <button>Login</button>
    </form>
    """


@app.route("/post", methods=["GET","POST"])
@login_required
def post():
    if request.method == "POST":
        job = Job(
            title=request.form["title"],
            location=request.form["location"],
            user_id=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        return redirect("/")

    return """
    <h2>Post Job</h2>
    <form method="post">
    <input name="title">
    <input name="location">
    <button>Post</button>
    </form>
    """


if __name__ == "__main__":
    app.run()
