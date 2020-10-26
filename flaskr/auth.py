import functools
from flask import (
    Blueprint, g, redirect, render_template, flash, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db


# create `auth` blueprint
bp = Blueprint('auth',__name__,url_prefix='/auth')
# The url_prefix will be prepended to all the URLs associated with the blueprint.

@bp.route('/register', methods=("GET","POST"))
def register():
    """/auth/register is associated with register view function"""
    if request.method == "POST":
        #  the username and password POSTed in POST request of login form
        username = request.form['username']
        password = request.form['password']
        print(f"username = {username}")
        print(type(username))
        # validate credentials and raise error
        error = None
        db = get_db()
        if username is None or username == "":
            error = "Username is required"
        elif password is None or password == "":
            error = "Password is required"
        elif db.execute("SELECT * FROM user where username = ?",(username,)).fetchone():
            error = "Username {} already exists".format(username)
        elif error is None:
            # Commit user information to database
            db.execute("INSERT INTO user (username, password) VALUES (?, ?)",
                        (username, generate_password_hash(password)))
            db.commit()
            # return redirect to auth.login view
            return redirect(url_for('auth.login'))
        flash(error) # Used to flash error messages
    # If method == GET, return login.html template
    return render_template('auth/register.html')


@bp.route('/login',methods=("GET","POST"))
def login():
    if request.method == "POST":
        # Get login details posted for user
        username = request.form["username"]
        password = request.form["password"]
        # Validate
        error = None
        db = get_db()
        if username is None:
            error = "Username is required"
        elif password is None:
            error = "Password is required"
        
        if error is not None:
            flash(error)

        user = db.execute("SELECT * from user where username = ?",(username,)).fetchone()
        if user is None:
            error = "incorrect username"
        elif not check_password_hash(user['password'], password):
            error = "Incorrect password"
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
                                  "SELECT * FROM user where id = ?", (user_id,)
                                  ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Below decorator is Useful when accessing other URL views
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view