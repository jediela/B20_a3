# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()
# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     uname = db.Column(db.String(20), unique=True, nullable=False)
#     uemail = db.Column(db.String(120), unique=True, nullable=False)
#     upwd = db.Column(db.String(128), nullable=False)
#     utype = db.Column(db.String(120), nullable=False)
#     grades = db.relationship('Grade', backref='user', lazy=True)

# class Grade(db.Model):
#     __tablename__ = 'grades'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# def init_db(app):
#     db.init_app(app)