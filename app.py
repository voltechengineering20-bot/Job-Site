from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# ---------------- USERS ----------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- JOBS ----------------
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    desc = db.Column(db.String(200))

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    jobs = Job.query.all()
    html = "<h1>Job Board</h1>"
    
    if current_user.is_authenticated:
        html += f"Welcome {current_user.username} | <a href='/logout'>Logout</a><br>"
        html += "<a href='/post'>Post Job</a><br><br>"
    else:
        html += "<a href='/login'>Login</a> | <a href='/register'>Register</a><br><br>"

    for job in jobs:
        html += f"<b>{job.title}</b><br>{job.desc}<hr>"

    return html

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        user = User(username=request.form["user"], password=request.form["pass"])
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return """
    <h2>Register</h2>
    <form method="post">
    Username:<input name="user"><br>
    Password:<input name="pass"><br>
    <button>Register</button>
    </form>
    """

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["user"], password=request.form["pass"]).first()
        if user:
            login_user(user)
            return redirect("/")
    return """
    <h2>Login</h2>
    <form method="post">
    Username:<input name="user"><br>
    Password:<input name="pass"><br>
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
        job = Job(title=request.form["title"], desc=request.form["desc"])
        db.session.add(job)
        db.session.commit()
        return redirect("/")

    return """
    <h2>Post Job</h2>
    <form method="post">
    Title:<input name="title"><br>
    Description:<textarea name="desc"></textarea><br>
    <button>Post</button>
    </form>
    """

# ---------------- RUN ----------------
with app.app_context():
    db.create_all()

app.
if __name__ == "__main__":
    app.run()
