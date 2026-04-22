from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'jobs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    location = db.Column(db.String(100))

# Create DB
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    search = request.args.get("search", "").lower()
    location = request.args.get("location", "")

    jobs = Job.query.order_by(Job.id.desc()).all()

    html = """
    <html>
    <head>
        <title>Job Board Zambia</title>
        <style>
            body { font-family: Arial; background: #f4f6f9; margin: 0; }
            header {
                background: #0d6efd;
                color: white;
                padding: 15px;
                display: flex;
                justify-content: space-between;
            }
            .container { padding: 20px; }
            .btn {
                padding: 10px 15px;
                background: #198754;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
            .job {
                background: white;
                padding: 15px;
                margin-top: 10px;
                border-radius: 8px;
            }
            input, select {
                padding: 8px;
                margin: 5px;
            }
        </style>
    </head>
    <body>

    <header>
        <div>🚚 Job Board Zambia</div>
        <a class="btn" href="/post">Post Job</a>
    </header>

    <div class="container">

    <h2>Search Jobs</h2>

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


@app.route("/post", methods=["GET","POST"])
def post():
    if request.method == "POST":
        new_job = Job(
            title=request.form["title"],
            location=request.form["location"]
        )
        db.session.add(new_job)
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
