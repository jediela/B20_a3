# from flask import Blueprint,request,flash,redirect,render_template,url_for,session
# from flask_bcrypt import Bcrypt
# from app import db, User
# from flask_bcrypt import generate_password_hash, check_password_hash

# auth_bp = Blueprint('auth', __name__)

# # 블루프린트 등록

# @auth_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')

#         existing_user = User.query.filter((User.uname == username) | (User.uemail == email)).first()
#         if existing_user:
#             if existing_user.uname == username:
#                 flash('Username already exists. Please choose a different username.', 'error')
#             elif existing_user.uemail == email:
#                 flash('Email already exists. Please choose a different email.', 'error')
#             return redirect(url_for('auth.register'))

#         password = request.form.get('password')
#         user_type = request.form.get('user_type')
#         hashed_password = generate_password_hash(password).decode('utf-8')
        
#         new_user = User(uname=username, uemail=email, upwd=hashed_password, utype=user_type)
#         db.session.add(new_user)
#         db.session.commit()
#         flash("Successfully registered!", 'success')
#         return redirect(url_for('auth.login'))

#     return render_template('register.html')

# @auth_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')

#         # if not username or not password:
#             flash('Username and password are required.')
#             return render_template('login.html')

#         user = User.query.filter_by(uname=username).first()

#         if not user:
#             flash('Invalid username or password')
#             return render_template('login.html')

#         if not check_password_hash(user.upwd, password):
#             flash('Invalid username or password')
#             return render_template('login.html')

#         session['user_id'] = user.id
#         session['user_type'] = user.utype
#         flash('Login successful!')
#         user_type = session.get('user_type')
#         if user_type == 'instructor':
#             flash('Welcome instructor')
#             return redirect(url_for('instructorHome'))
#         elif user_type == 'student':
#             flash('Welcome student')
#             return redirect(url_for('studentHome'))

#     return render_template('login.html')

# @auth_bp.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     session.pop('user_type', None)
#     return redirect(url_for('auth.login'))
