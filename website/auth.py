from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash 
auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    from website.models import User
    from website import db
    from website import views

    if request.method == 'POST':

        signup_form_data = request.form
        user_name = signup_form_data.get('username')
        email = signup_form_data.get('email')
        password = signup_form_data.get('password')
        repassword = signup_form_data.get('repassword')

        print(user_name, email, password)

        if User.query.filter(User.username == user_name).first():
            flash('User of this username already exists. Please use different username', category='error')
            print('ran username check')

        elif User.query.filter(User.email == email).first():
            flash('User of this email already exists. Please use different email id', category='error')
            print('ran email check')

        elif password != repassword:
            flash('password does not match', category='error')
            print('ran passcheck')
        
        elif len(password) <= 4:
            flash('Password must be atlease of 4 characters')
            print('ran passcheck two')
        
        else:
            print('at least coming here')
            new_user = User(username = user_name, email = email, password = generate_password_hash(password=password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            print('success')
            flash('user created successfully')
            return redirect(url_for('/login'))

    return render_template('signup.html')

@login_required
@auth.route('/logout')
def logout():
    logout_user()
    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    from website.models import User

    if request.method == 'POST':
        login_from_data = request.form

        email = login_from_data.get('email')
        password = login_from_data.get('password')

        verify_user = User.query.filter(User.email == email).first()

        if verify_user:
            if check_password_hash(pwhash=verify_user.password, password=password):
                flash('user logged in', category='success')
                login_user(verify_user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('password is incorrect', category='error')
                return redirect(url_for('auth.login')) 
        else:
            flash('user not found', category='error')

    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    return render_template('login.html')

