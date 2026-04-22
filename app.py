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

    .btn {
        background: #198754;
        color: white;
        padding: 8px 12px;
        text-decoration: none;
        border-radius: 5px;
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
        <div>
            <a href="/register" style="color:white;">Register</a> |
            <a href="/login" style="color:white;">Login</a> |
            <a href="/post" style="color:white;">Post Job</a>
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
