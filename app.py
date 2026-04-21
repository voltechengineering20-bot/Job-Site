from flask import Flask, request, redirect

app = Flask(__name__)

jobs = []

@app.route("/")
def home():
    html = """
    <html>
    <head>
        <title>Job Board Zambia</title>
        <style>
            body {
                font-family: Arial;
                background: #f4f6f9;
                margin: 0;
            }
            header {
                background: #007bff;
                color: white;
                padding: 15px;
                text-align: center;
                font-size: 24px;
            }
            .container {
                padding: 20px;
            }
            .btn {
                display: inline-block;
                padding: 10px 15px;
                background: #28a745;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
            .job {
                background: white;
                padding: 15px;
                margin-top: 10px;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>

    <header>Job Board Zambia</header>

    <div class="container">
        <a class="btn" href="/post">+ Post a Job</a>
        <h2>Available Jobs</h2>
    """

    for job in jobs:
        html += f"<div class='job'>{job}</div>"

    html += """
    </div>
    </body>
    </html>
    """
    return html

@app.route("/post", methods=["GET","POST"])
def post():
    if request.method == "POST":
        jobs.append(request.form["title"])
        return redirect("/")
    return """
    <h2>Post Job</h2>
    <form method="post">
    <input name="title" placeholder="Enter job details" style="width:300px"><br><br>
    <button>Post</button>
    </form>
    """

if __name__ == "__main__":
    app.run()
