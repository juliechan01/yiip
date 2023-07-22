from flask import app
from flask import render_template, redirect, request, session, flash
from ..models.user_model import User

from flask import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')



# working on post methods below for register and login
@app.route('/register', methods = ['post'])
def register():
    if request.form['action'] == 'register':

        # User model validation can be utilized here; improper validation creates redirect to register page
        if not User.validate_user(request.form):
            return redirect('/register')

        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        # check console for created hashed password
        print("PW HASH IS BELOW: ")
        print(pw_hash)

        data_row = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password' : pw_hash,
            'birthday' : request.form['birthday']
        }

        # IF
        # check database to see if email already exists
        # if exists, return redirect to register page with errors showing
        # flash can be utilized here to tell user about this

        # IF
        # if email is not in database, proceed with User model function to save entry, save session,
        # and proceed to Map page
        # variable can be created (below) to keep session usable
        user_id = User.save(data_row)
        session['user_id'] = user_id
        return redirect('/dashboard')
    

@app.route('/login', methods = ['post'])
def login():
    if request.form['action'] == 'user_login':
        data_row = {
            'email' : request.form['email']
        }
        user_in_db = User.get_by_email(data_row)

        if not user_in_db:
            flash("Invalid Email/Password.")
            return redirect('/')
        if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            flash("Invalid Email/Password.")
            return redirect('/')

    session['user_id'] = user_in_db.id
    return redirect('/dashboard')