from flask import (
    Blueprint, g, render_template, redirect, flash, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog',import_name=__name__)

# Route / to show all blog posts
@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
    "SELECT p.id, title, body, created, author_id, username"
    " FROM post p JOIN user u WHERE p.author_id = u.id"
    " ORDER BY created DESC"
    ).fetchall()
    return render_template('blog/index.html',posts=posts)
