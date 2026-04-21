
from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'jobs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    location = db.Column(db.String(100))
    user_id = db.Column(db.Integer)

# Create DB
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home
@app.route("/")
def home():
    jobs = Job.query.order_by(Job.id.desc()).all()

    html = "<h1>Job Board</h1>"

    if current_user.is_authenticated:
        html += f"Welcome {current_user.username} | <a href='/logout'>Logout</a><br>"
        html += "<a href='/post'>Post Job</a><br><br>"
    else:
        html += "<a href='/login'>Login</a> | <a href='/register'>Register</a><br><br>"

    for job in jobs:
        html += f"<p>{job.title} - {job.location}</p>"

    return html

# Register
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        user = User(username=request.form["username"], password=generate_password_hash(request.form["password"])
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return """
    <h2>Register</h2>
    <form method="post">
    <input name="username" placeholder="Username"><br><br>
    <input name="password" placeholder="Password"><br><br>
    <button>Register</button>
    </form>
    """

# Login
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and user.password == request.form["password"]:
            login_user(user)
            return redirect("/")
        return "Invalid login"

    return """
    <h2>Login</h2>
    <form method="post">
    <input name="username" placeholder="Username"><br><br>
    <input name="password" placeholder="Password"><br><br>
    <button>Login</button>
    </form>
    """

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

# Post Job (only logged in users)
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
    <input name="title" placeholder="Job title"><br><br>

    <select name="location">
        <option value="Kitwe">Kitwe</option>
        <option value="Lusaka">Lusaka</option>
    </select><br><br>

    <button>Post</button>
    </form>
    """

if __name__ == "__main__":
    app.run()
