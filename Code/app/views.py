from app import app, db
from app import login_manager
from flask import render_template, request, redirect, url_for, session
from flask.ext.login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash



@app.route('/')
# @login_required
def index():
	message = "Hello"
	return render_template("index.html", message=message)


@app.route('/test')
# @login_required
def test():
	return render_template("template.html")
