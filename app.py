from flask import Flask, request, redirect, url_for
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

@app.route("/")
def home():
    search = request.args.get("search", "").lower()
    location = request.args.get("location", "")

    jobs = Job.query.order_by(Job.id.desc()).all()

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

    input, select, button {
        width: 100%;
        padding: 12px;
        margin-top: 10px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }

    button {
        background: #198754;
        color: white;
        border: none;
    }

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
        <a href="/post" style="color:white;">Post Job</a>
    </header>

    <div class="container">

    <form method="get">
        <input name="search" placeholder="Search job..." />
        <select name="location">
            <option value="">All Locations</option>
            <option value="Kitwe">Kitwe</option>
            <option value="Lusaka">Lusaka</option>
        </select>
        <button>Search</button>
    </form>

    <h2>Available Jobs</h2>
    """

    for job in jobs:
        if (search in job.title.lower()) and (location == "" or location == job.location):
            html += f"<div class='job'>📌 {job.title} - {job.location}</div>"

    html += "</div></body></html>"
    return html


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=generate_password_hash(request.form["password"])
        )
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


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


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

    <select name="location">
        <option value="Kitwe">Kitwe</option>
        <option value="Lusaka">Lusaka</option>
    </select>

    <button>Post</button>
    </form>
    """


if __name__ == "__main__":
    app.run()
