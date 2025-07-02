from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'bb9d4eedc3047b6cb389a75d95c74ce4'

# MySQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Pujitha15@localhost/learning_portal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- Models ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    progress = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)

# ---------------- Routes ----------------
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists!', 'error')
        else:
            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, password=hashed_pw,
                            first_name=first_name, last_name=last_name, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Registered successfully!', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user'] = user.username
            return redirect(url_for('welcome'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/welcome')
def welcome():
    if 'user' in session:
        user = User.query.filter_by(username=session['user']).first()

        enrollments = Enrollment.query.filter_by(user_id=user.id).all()
        courses_in_progress = len([e for e in enrollments if not e.completed])
        completed_courses = len([e for e in enrollments if e.completed])
        certificates_earned = completed_courses

        enrolled_courses = Course.query.filter(Course.id.in_([e.course_id for e in enrollments])).all()

        return render_template(
            'index.html',
            first_name=user.first_name,
            courses=enrolled_courses,
            progress_courses=courses_in_progress,
            completed_courses=completed_courses,
            certificates_earned=certificates_earned
        )
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'user' in session:
        user = User.query.filter_by(username=session['user']).first()
        return render_template('profile.html', user=user)
    return redirect(url_for('login'))

@app.route('/courses')
def courses():
    all_courses = Course.query.all()
    return render_template('courses.html', courses=all_courses)

@app.route('/enroll/<int:course_id>', methods=['POST'])
def enroll(course_id):
    if 'user' not in session:
        flash('Login to enroll in a course.', 'error')
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['user']).first()
    existing = Enrollment.query.filter_by(user_id=user.id, course_id=course_id).first()

    if existing:
        flash('Already enrolled in this course.', 'info')
    else:
        db.session.add(Enrollment(user_id=user.id, course_id=course_id))
        db.session.commit()
        flash('Enrolled successfully!', 'success')

    return redirect(url_for('courses'))

@app.route('/my-courses')
def my_courses():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['user']).first()
    enrollments = Enrollment.query.filter_by(user_id=user.id).all()
    course_ids = [e.course_id for e in enrollments]
    courses = Course.query.filter(Course.id.in_(course_ids)).all()

    return render_template('my_courses.html', courses=courses, first_name=user.first_name)

@app.route('/add-many-courses')
def add_many_courses():
    courses = [
        Course(title="Python for Beginners", description="Learn Python basics."),
        Course(title="Advanced Python", description="OOP, decorators, and more."),
        Course(title="Web Development with Flask", description="Build web apps."),
        Course(title="HTML & CSS", description="Design responsive pages."),
        Course(title="JavaScript Essentials", description="Add interactivity."),
        Course(title="React Basics", description="Build dynamic UIs."),
        Course(title="MySQL for Developers", description="Manage MySQL DB."),
        Course(title="Machine Learning 101", description="Supervised & unsupervised."),
        Course(title="NLP Basics", description="Text and language processing."),
        Course(title="Cloud with AWS", description="Use EC2, S3, Lambda."),
    ]
    db.session.add_all(courses)
    db.session.commit()
    return "Courses added successfully!"

# ---------------- Start App ----------------
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)