from flask import Flask, request, redirect

app = Flask(__name__)

jobs = []

@app.route("/")
def home():
    html = "<h1>Job Board</h1><a href='/post'>Post Job</a><hr>"
    for job in jobs:
        html += f"<b>{job}</b><hr>"
    return html

@app.route("/post", methods=["GET","POST"])
def post():
    if request.method == "POST":
        jobs.append(request.form["title"])
        return redirect("/")
    return """
    <h2>Post Job</h2>
    <form method="post">
    <input name="title" placeholder="Job title">
    <button>Post</button>
    </form>
    """

if __name__ == "__main__":
    app.run()
