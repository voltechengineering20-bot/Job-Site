
    from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__)

# 🔐 Secret key (important)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# 🗄️ Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 👤 User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# 🧱 Create database
with app.app_context():
    db.create_all()

# 🔒 Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 🏠 Home
@app.route('/')
def home():
    return render_template('index.html')

# 📝 Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Validation
        if len(password) < 6:
            return "Password must be at least 6 characters"

        # Check existing user
        if User.query.filter_by(email=email).first():
            return "User already exists"

        # Hash password
        hashed_password = generate_password_hash(password)

        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

# 🔑 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return "Invalid email or password"

    return render_template('login.html')

# 📊 Dashboard (protected)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# 🚪 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ▶ Run
if __name__ == '__main__':
    app.run(debug=True)
