style>

    </head>
    <body>

    <header>
        <div style="font-weight:bold;">🚚 Job Board Zambia</div>
        <a href="/post" style="color:white;">Post Job</a>
    </header>

    <div class="container">

    <h2>Find Jobs Across Zambia 🇿🇲</h2>
    <p>Search and apply for jobs in Kitwe, Lusaka and beyond.</p>

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

    if not jobs:
        html += "<p>No jobs posted yet. Be the first to post one!</p>"

    for job in jobs:
        if (search in job.title.lower()) and (location == "" or location == job.location):
            html += f"<div class='job'>📌 {job.title} - {job.location}</div>"

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
