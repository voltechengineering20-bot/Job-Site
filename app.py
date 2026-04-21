
html = """
<html>
<head>
<title>Job Board Zambia</title>

<style>
body {
    font-family: 'Segoe UI', Arial;
    background: #eef1f5;
    margin: 0;
}

/* HEADER */
header {
    background: #0d6efd;
    color: white;
    padding: 15px 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 22px;
    font-weight: bold;
}

.nav a {
    color: white;
    margin-left: 15px;
    text-decoration: none;
    font-weight: 500;
}

/* CONTAINER */
.container {
    padding: 30px;
    max-width: 800px;
    margin: auto;
}

/* SEARCH BOX */
.search-box {
    background: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

input, select {
    padding: 10px;
    margin: 5px;
    width: 30%;
    border-radius: 5px;
    border: 1px solid #ccc;
}

/* BUTTON */
button {
    padding: 10px 15px;
    background: #198754;
    color: white;
    border: none;
    border-radius: 5px;
}

/* JOB CARD */
.job {
    background: white;
    padding: 15px;
    margin-top: 15px;
    border-radius: 10px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
}
</style>

</head>
<body>

<header>
    <div class="logo">🚚 Job Board Zambia</div>
    <div class="nav">
        <a href="/">Home</a>
        <a href="/post">Post Job</a>
        <a href="/login">Login</a>
    </div>
</header>

<div class="container">

<div class="search-box">
<form method="get">
    <input name="search" placeholder="Search job..." />
    <select name="location">
        <option value="">All Locations</option>
        <option value="Kitwe">Kitwe</option>
        <option value="Lusaka">Lusaka</option>
    </select>
    <button>Search</button>
</form>
</div>

<h2>Available Jobs</h2>
"""
    for job in jobs:
        if (search in job.title.lower()) and (location == "" or location == job.location):
            html += f"<div class='job'>📌 {job.title} - {job.location}</div>"

    html += "</div></body></html>"
    return html



