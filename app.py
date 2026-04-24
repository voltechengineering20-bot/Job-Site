from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

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
    company = db.Column(db.String(100))
    location = db.Column(db.String(100))
    whatsapp = db.Column(db.String(20))
    user_id = db.Column(db.Integer)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# HOME
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
    body { font-family: Arial; background: #f4f6f9; margin: 0; }

    header {
        background: #0d6efd;
        color: white;
        padding: 15px;
    }

    .nav {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 5px;
    }

    .nav a {
        color: white;
        text-decoration: none;
        font-size: 14px;
    }

    .container { padding: 15px; }

    input, select {
        width: 100%;
        padding: 12px;
        margin-top: 10px;
        border-radius: 8px;
        border: 1px solid #ccc;
    }

    button {
        width: 100%;
        padding: 12px;
        margin-top: 10px;
        border-radius: 8px;
        border: none;
        background: #198754;
        color: white;
        font-weight: bold;
    }

    .job {
        background: white;
        padding: 15px;
        margin-top: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .apply-btn {
        display: inline-block;
        margin-top: 10px;
        background: #25D366;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        text-decoration: none;
    }
    </style>
    </head>

    <body>

    <header>
        <div><strong>🚚 Job Board Zambia</strong></div>
        <div class="nav">
            <a href="/">Home</a>
            <a href="/post">Post</a>
            <a href="/dashboard">Dashboard</a>
            <a href="/login">Login</a>
            <a href="/logout">Logout</a>
        </div>
    </header>

    <div class="container">
<div style="background:white; padding:20px; border-radius:12px; margin-bottom:15px;">
    <h2>Find Jobs Across Zambia 🇿🇲</h2>
    <p>Connect with top employers in Kitwe, Lusaka and beyond.</p>
</div>
    <h2>Find Jobs</h2>

    <form method="get">
        <input name="search" placeholder="Search jobs..." />
        <select name="location">
            <option value="">All Locations</option>
            <option value="Kitwe">Kitwe</option>
            <option value="Lusaka">Lusaka</option>
        </select>
        <button>Search</button>
    </form>

    <h2>Available Jobs</h2>
    """

    found = False

    for job in jobs:
        if (search in job.title.lower()) and (location == "" or location == job.location):
            found = True
            html += f"""
            <div class='job'>
            <strong>{job.title}</strong><br>
            🏢 {job.company}<br>
            📍 {job.location}<br>
            <a class='apply-btn' href='https://wa.me/{job.whatsapp}'>Apply via WhatsApp</a>
            </div>
            """

    if not found:
        html += "<p>No jobs found.</p>"

    html += "</div></body></html>"
    return html


# REGISTER
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


# LOGIN
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
            company=request.form["company"],
            location=request.form["location"],
            whatsapp=request.form["whatsapp"],
            user_id=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        return redirect("/")

    return """
    <h2>Post Job</h2>
    <form method="post">
    <input name="title" placeholder="Job title">
    <input name="company" placeholder="Company name">
    <select name="location">
        <option value="Kitwe">Kitwe</option>
        <option value="Lusaka">Lusaka</option>
    </select>
    <input name="whatsapp" placeholder="WhatsApp number (260...)">
    <button>Post</button>
    </form>
    """


# DASHBOARD
@app.route("/dashboard")
@login_required
def dashboard():
    jobs = Job.query.filter_by(user_id=current_user.id).all()

    html = "<h2>Your Jobs</h2><a href='/'>Home</a><br><br>"

    if not jobs:
        html += "<p>No jobs yet.</p>"

    for job in jobs:
        html += f"<p>{job.title} - {job.location}</p>"

    return html


if __name__ == "__main__":
    app.run()

    
