from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import request, session, redirect, url_for, flash, render_template
from flask_bcrypt import generate_password_hash, check_password_hash
# from extensions import db,bcrypt
# from models import User
from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import text, create_engine # textual queries

app = Flask(__name__)
bcrypt = Bcrypt(app) # consider later.
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///A3.db'

journal_mode = 'DELETE'
engine = create_engine('sqlite:///A3.db?journal_mode=' + journal_mode)
db = SQLAlchemy(app)
app.app_context().push()
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    fname = db.Column(db.String(20), unique=True, nullable=False)
    lname = db.Column(db.String(120), unique=True, nullable=False)
    uname = db.Column(db.String(20), unique=True, nullable=False)
    uemail = db.Column(db.String(120), unique=True, nullable=False)
    upwd = db.Column(db.String(128), nullable=False)  # Increased password length
    utype = db.Column(db.String(120), nullable=False)
    grades = db.relationship('Grade', backref='user', lazy=True)

class Grade(db.Model):
    __tablename__ = 'grades'
    gid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, db.ForeignKey('user.id'))
    work = db.Column(db.String(50), nullable = False)
    grade = db.Column(db.Integer)

class Remark(db.Model):
    __tablename__ = 'remark'
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    work = db.Column(db.String(50), db.ForeignKey('grades.work'), nullable = False)
    question = db.Column(db.Integer)
    request = db.Column(db.String(1000), nullable = False)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    fid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid_student = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uid_instructor = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lec_like = db.Column(db.String(1000), nullable = False)
    lec_improve = db.Column(db.String(1000), nullable = False)
    lab_like = db.Column(db.String(1000), nullable = False)
    lab_improve= db.Column(db.String(1000), nullable = False)
    comment = db.Column(db.String(1000))

@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template('home.html')
@app.route('/introduce')
def introduce():
    return render_template('introduce.html')

@app.route('/developers')
def developers():
    return render_template('developers.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(uname=username).first()

        if user is None:
            flash('Username not found')
            return render_template('login.html')

        elif not check_password_hash(user.upwd, password):
            flash('Invalid password')
            return render_template('login.html')

        session['user_id'] = user.id
        session['user_type'] = user.utype
        
        # flash('Login successful!')
        user_type = session.get('user_type')
        if user_type == 'instructor':
            # flash('Welcome instructor')
            return redirect(url_for('instructorHome'))
        elif user_type == 'student':
            # flash('Welcome student')
            return redirect(url_for('studentHome'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        username = request.form.get('username')
        email = request.form.get('email')

        # Check if the username or email already exists in the database
        existing_user = User.query.filter((User.uname == username) | (User.uemail == email)).first()
        if existing_user:
            if existing_user.uname == username:
                flash('Username already exists. Please choose a different username.', 'error')
            elif existing_user.uemail == email:
                flash('Email already exists. Please choose a different email.', 'error')
            return redirect(url_for('register'))

        # If the username and email are unique, proceed with registration
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        hashed_password = generate_password_hash(password).decode('utf-8')
        
        new_user = User(uname=username, uemail=email, fname = fname, lname = lname, upwd=hashed_password, utype=user_type)
        db.session.add(new_user)
        db.session.commit()
        flash("Successfully registered!", 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    return redirect(url_for('homepage'))
@app.route('/instructorHome')
def instructorHome():
    # if 'user_id' not in session or session['user_type'] != 'instructor':
    #     flash('You are not authorized to access this page.', 'error')
    #     return redirect(url_for('home'))
    
    uname = User.query.filter_by(id=session['user_id']).first().uname
    return render_template('instructorHome.html', uname=uname)

@app.route('/instructorGrades.html')
def viewGrades():
    all_grades = Grade.query.order_by(Grade.id).all()
    return render_template("instructorGrades.html", grades=all_grades)

@app.route('/instructorFeedback.html')
def viewFeedback():
    instructor_id = session['user_id']
    instructorFeedback = db.session.query(Feedback, User.uname).join(User, Feedback.uid_student == User.id).filter(Feedback.uid_instructor == instructor_id).all()
    return render_template("instructorFeedback.html", feedback=instructorFeedback)

@app.route('/enterGrades.html', methods=['GET', 'POST'])
def enterGrades():
    if request.method == 'POST':
        student_id = request.form['student_id']
        work = request.form['work']
        grade = request.form['grade']

        # Assuming Grade is the model for the 'grades' table
        new_grade = Grade(id=student_id, work=work, grade=grade)
        db.session.add(new_grade)
        db.session.commit()

        flash('Grade entered successfully!', 'success')
        return redirect(url_for('enterGrades'))
    else:
        return render_template("enterGrades.html")
    
@app.route('/instructorRemarks.html')
def viewRemarks():
    remarks = db.session.query(Remark, User.uname).join(User, Remark.id == User.id).all()
    return render_template("instructorRemarks.html", remarks=remarks)


@app.route('/studentHome')
def studentHome():
    if 'user_id' not in session or session['user_type'] != 'student':
        flash('You are not authorized to access this page.', 'error')
        return redirect(url_for('home'))
    uname = User.query.filter_by(id=session['user_id']).first().uname
    return render_template('studentHome.html', uname=uname)

 
@app.route('/studentGrades.html', methods = ['GET', 'POST'])
def studentGrades():
    student_grades = Grade.query.filter_by(id=session['user_id']).all()

    if request.method == 'POST':
        rmk_question = request.form['question']
        rmk_request = request.form['request']
        work_type = request.form['work']        
        make_request = Remark(id = session['user_id'], work = work_type, question = rmk_question, request = rmk_request)
        db.session.add(make_request)
        db.session.commit()
        flash("Submitted successfully! You'll hear back from your professor soon!", 'success')
        return redirect(url_for('studentGrades'))
    return render_template("studentGrades.html", student_grades = student_grades)

    
@app.route('/index.html')
def home():
    user_type = session.get('user_type')
    if user_type == 'instructor':
        return redirect(url_for('instructorHome'))
    elif user_type == 'student':
        return redirect(url_for('studentHome'))
    else:
        return render_template("index.html")
    
@app.route('/assignments.html')
def assignments(): 
    return render_template("assignments.html")

@app.route('/calendar.html')
def calendar():
    return render_template("calendar.html")

@app.route('/content.html')
def content():
    return render_template("content.html")

@app.route('/feedback.html', methods = ['GET', 'POST'])
def feedback():
    user = User.query.filter_by(uname=username).first()

    if user.utype == 'student':
        instructors = User.query.filter_by(utype = "instructor").all()
        if request.method == 'POST':
            selected_instructor_id = request.form['selected_instructor']
            lec_like = request.form['lec_like']
            lec_improve = request.form['lec_improve']
            lab_like = request.form['lab_like']
            lab_improve= request.form['lab_improve']
            comment = request.form['comment']

            selected_instructor = User.query.get(selected_instructor_id)

            give_feedback = Feedback(uid_student = session['user_id'], uid_instructor = selected_instructor.id,
                                    lec_like = lec_like, lec_improve = lec_improve,
                                    lab_like = lab_like, lab_improve = lab_improve, comment = comment)
            db.session.add(give_feedback)
            db.session.commit()
            return redirect(url_for('feedback'))
        else:
            return redirect(url_for('instructorFeedback'))
    return render_template('feedback.html', instructors = instructors)


@app.route('/labs.html')
def labs():
    return render_template("labs.html")

@app.route('/team.html')
def team():
    return render_template("team.html")

if __name__ == '__main__':
    db.create_all()
    # app.run(debug=True,port="5010")
    app.run(debug=True,port=5004)