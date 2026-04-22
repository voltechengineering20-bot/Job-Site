from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

# ✅ APP FIRST (fixes "app not defined")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'jobs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# MODELS
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    location = db.Column(db.String(100))
    user_id = db.Column(db.Integer)

# CREATE DATABASE
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# HOME PAGE
@app.route("/")
def home():
    jobs = Job.query.all()

    html = """
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Board Zambia</title>

    <style>
    body { font-family: Arial; background: #eef1f5; margin: 0; }

    header {
        background: #0d6efd;
        color: white;
        padding: 12px;
        display: flex;
        justify-content: space-between;
    }

    .container { padding: 15px; }

    .job {
        background: white;
        padding: 15px;
        margin-top: 15px;
        border-radius: 10px;
    }
    </style>

    </head>
    <body>

    <header>
        <div>🚚 Job Board Zambia</div>
        <div>
            <a href="/register" style="color:white;">Register</a> |
            <a href="/login" style="color:white;">Login</a> |
            <a href="/post" style="color:white;">Post Job</a> |
            <a href="/logout" style="color:white;">Logout</a>
        </div>
    </header>

    <div class="container">
    <h2>Available Jobs</h2>
    """

    if not jobs:
        html += "<p>No jobs yet. Post one!</p>"

    for job in jobs:
        html += f"""
        <div class='job'>
        <strong>{job.title}</strong><br>
        📍 {job.location}
        </div>
        """

    html += "</div></body></html>"
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

        return redirect("/login")

    return """
    <h2>Register</h2>
    <form method="post">
    <input name="username" placeholder="Username">
    <input name="password" placeholder="Password">
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

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect("/")

        return "Invalid login"

    return """
    <h2>Login</h2>
    <form method="post">
    <input name="username" placeholder="Username">
    <input name="password" placeholder="Password">
    <button>Login</button>
    </form>
    """


# LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


# POST JOB
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
    <input name="title" placeholder="Job title">
    <input name="location" placeholder="Location">
    <button>Post</button>
    </form>
    """


# RUN APP
if __name__ == "__main__":
    app.run()
