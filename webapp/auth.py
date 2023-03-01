from distutils.log import error
from genericpath import exists
from flask import Blueprint, render_template, request, flash, redirect,url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET' :
        return render_template("login.html", user=current_user)
        
    if request.method == 'POST' : 
        email = request.form['email']
        password = request.form['password']
        
        from .models import User
        user = User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('The Credentials do not match. Please try again!', category='error')
        else:
            flash('Sorry, We couldn\'t find you in our Database',category='error')
        return render_template("login.html", user=current_user)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html", user=current_user)
        
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        conf_password = request.form['conf_password']
        
        from .models import User
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('This email is already registered, Try logging in',category='error')
        elif len(password) < 8:
            flash('Password must be at least 8 characters',category='error')
        elif password != conf_password:
            flash('Passwords do not match',category='error')
        else:
            from . import db
            userinfo = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
            db.session.add(userinfo)
            db.session.commit()
            flash('You are now registered with us', category='success')
            return redirect(url_for('auth.login'))
    return render_template("register.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully!', category='success')
    return redirect(url_for('auth.login'))