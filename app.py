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
from sqlalchemy import text # textual queries


app = Flask(__name__)
bcrypt = Bcrypt(app) # consider later.
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///A3.db'
db = SQLAlchemy(app)
app.app_context().push()
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    uname = db.Column(db.String(20), unique=True, nullable=False)
    uemail = db.Column(db.String(120), unique=True, nullable=False)
    upwd = db.Column(db.String(128), nullable=False)  # Increased password length
    utype = db.Column(db.String(120), nullable=False)
    grades = db.relationship('Grade', backref='user', lazy=True)

class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Remark(db.Model):
    __tablename__ = 'remark'
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    aid = db.Column(db.Integer, nullable=False)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    fid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid_student = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uid_instructor = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feedback = db.Column(db.Text, nullable=False)

@app.route('/')
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
            flash('invalid password')
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
        
        new_user = User(uname=username, uemail=email, upwd=hashed_password, utype=user_type)
        db.session.add(new_user)
        db.session.commit()
        flash("Successfully registered!", 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    return redirect(url_for('login'))
@app.route('/instructorHome')
def instructorHome():
    # if 'user_id' not in session or session['user_type'] != 'instructor':
    #     flash('You are not authorized to access this page.', 'error')
    #     return redirect(url_for('home'))
    
    uname = User.query.filter_by(id=session['user_id']).first().uname
    return render_template('instructorHome.html', uname=uname)

@app.route('/studentHome')
def studentHome():
    if 'user_id' not in session or session['user_type'] != 'student':
        flash('You are not authorized to access this page.', 'error')
        return redirect(url_for('home'))
    uname = User.query.filter_by(id=session['user_id']).first().uname
    return render_template('studentHome.html', uname=uname)

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

@app.route('/feedback.html')
def feedback():
    return render_template("feedback.html")

@app.route('/labs.html')
def labs():
    return render_template("labs.html")

@app.route('/team.html')
def team():
    return render_template("team.html")


if __name__ == '__main__':
    db.create_all()
    # app.run(debug=True,port="5010")
    app.run(debug=True)