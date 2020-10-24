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

## Define and Access Database
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
````





