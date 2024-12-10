from flask import Blueprint, render_template,redirect, url_for, request, flash
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!!!',category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')
            
    return render_template('login.html',user=current_user)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')


        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!!!', category='error')
        elif (len(email) < 4):
            flash('Email is too short, enter a valid email!!', category='error')
        elif (len(first_name) < 2):
            flash('Name is too short, Enter a longer name!!', category='error')
        elif (password1 != password2):
            flash('Passwords do not match!!', category='success')
        elif (len(password1) < 7):
            flash('Password is too short!!', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()            
            login_user(new_user, remember=True)
            flash('Account Created!!', category='success')
            return redirect(url_for('views.home'))

    

    return render_template('sign-up.html',user=current_user)
