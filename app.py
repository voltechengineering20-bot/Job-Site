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
            body { font-family: Arial; background: #f4f6f9; margin: 0; }
            header {
                background: #0d6efd;
                color: white;
                padding: 15px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .logo {
                font-size: 22px;
                font-weight: bold;
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
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>

    HTML
</header>  
img src="https://images.unsplash.com/photo-1581091870622-6c4b6c6a6a2c"
style="width:100%; height:200px; object-fit:cover;">
<img src="https://images.unsplash.com/photo-1581091870622-6c4b6c6a6a2c"
style="width:100%; height:200px; object-fit:cover;">

<div class="container">

    <div class="container">
        <h2>Available Jobs</h2>
    """

    for job in jobs:
        html += f"<div class='job'>📌 {job}</div>"

    html += "</div></body></html>"
    return html

@app.route("/post", methods=["GET","POST"])
def post():
    if request.method == "POST":
        jobs.append(request.form["title"])
        return redirect("/")
    return """
    <h2>Post Job</h2>
    <form method="post">
    <input name="title" placeholder="Enter job details"><br><br>
    <button>Post</button>
    </form>
    """

if __name__ == "__main__":
    app.run()
