import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(database=current_app.config['DATABASE'],
                                detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db',None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    # open_resource() opens file in relative path of flaskr package
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """initialize DB schema from schema.sql"""
    init_db()
    click.echo("Database initialized!!")

# register with the application
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

