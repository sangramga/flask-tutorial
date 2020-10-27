# Flask tutorial

1. Followed official flask site [here](https://flask.palletsprojects.com/en/1.1.x/tutorial)
## Installing Flask and dependencies

  `source /opt/conda/bin/activate` 


  `conda create -n flask -c conda-forge python=3.8.6 flask=1.1.2`


  `conda activate flask`


  For version checks of  flask and python (`-E` for extended REGEX and `-w` for complete match words only)


  `conda list | grep -Ew 'python|flask' `

<h1>1. Application Setup</h1>

## Application Factory  

Instead of creating a **Flask** instance globally, you will create it inside a function `create_app`. This function is known as the *application factory*. Any configuration, registration, and other setup the application needs will happen inside the function, then the application will be returned.  


## Running Flask App

````
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
$ flask run
````

<h1> 2. Define and Access Database </h1>
**SQLite** is convenient because it doesn’t require setting up a separate database server and is built-in to Python. Also light-weight and good for small applications.

### Connect to Database
Use DB connection to perform queries and operations, close connection after work is done
* Store connection in `g` instead of creating new connection after every request.
* `current_app` is the application context accessed without importing it
* `flask init-db` will call `init_db_command()` using `click.command()` decorator. `flaskr.sqlite` will be created if it does not exists in the instance path. 
* Using `schema.sql` for definining DB schema and `db.executescript()` using sqlite3 connection.

### Register with Application  

* The `close_db` and `init_db_command` functions need to be registered with the application instance; otherwise, they won’t be used by the application. However, since you’re using a factory function, that instance isn’t available when writing the functions. Instead, write a function `init_app` in `db.py` that takes an application and does the registration.  

### Initialize Database using flask cli  

````
$ flask init-db
Database initiated !!
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
$ flask run  

* Serving Flask app "flaskr" (lazy loading)
* Environment: development
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
````

------------------------------

<h1> 3. Blueprints and Views </h1>
* `Views` can take matching pattern URL's,  and returns outgoing response. Flask can also generate URL as output of view dependning upon its name and arguments.  

* `Blueprint` is used to register related `views` within itself. Then the `blueprint` is registered with the application instead of registering `views` directly.  

* In this `flaskr` app, two blueprints will be created one for `auth` and other for `blogs`. Check `auth.py` for  blueprint and related views.

### Register Blueprint
* `Blueprint()` is used to create blueprint with `url_prefix='auth'` and `app.register_blueprint()` is used to register with app.
* The `auth` Bluprint will have views to register, login and logout.

### Register Views
* **`@bp.route`** associates URL `\register` with `register` view function
* **`request.form`** is a special type of dict mapping submitted form keys and values. The user will input their username and password in POST method.
* **`generate_password_hash`** is used for storing hashes of passwords in DB, if validations are successful.
* After storing the user, they are redirected to the login page. **`url_for()`** generates the URL for the login view based on its name. This is preferable to writing the URL directly as it allows you to change the URL later without changing all code that links to it.
* `redirect()` to a particular URL of a view or a page. `flash` used to store and display error messages.
* `render_template()` will render HTML page templates in case of `GET` requests.

### Login/Logout view
* **`session`** is a dict to store cookie in a browser to identify user in case of re-visiting the site. Flask securely signs the cookies so that it cannot be tempered.  

* `bp.before_app_request()` registers a function that runs before the view function, no matter what URL is requested. `load_logged_in_user` checks if a user id is stored in the session and gets that user’s data from the database, storing it on `g.user`, which lasts for the length of the request. 

* `\logout` view will clear the `session` cookies, so thath its not used for subsequent requests.  

* `login_required` decorator can used to wrap other views like create, delete and edit blogs.

------------------------------

<h1> 4. Templates </h1>

-----------------------------

<h1> 5. Blog Blueprint </h1>


# Register Blueprint for blogs
* `app.add_url_rule()` associates the endpoint name `'index'` with the `/` url so that url_for('index') or url_for('blog.index') will both work, generating the same `/` URL either way.


-----------------------------
<h1> 6. Make package installable </h1>

# Added setup.py and MANIFEST.in  
* In `setup.py`, `packages` tells which directories to include and `find_packages()` finds those directories automatically. To include static and templates `include_package_data = True` and `MANIFEST.in` file is also required.
* For installation in editable/development mode `pip install -e .`. You can make changes without re-installing the package.
*  `export FLASK_APP=flaskr` and `flask run` used to run app. Since it is installed, its possible to run it from anywhere, not just from flaskr directory.

---------------------------------
<h1> 7. Testing and Coverage</h1>

* `pip install pytest coverage`