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


@app.route('/recommended-books')
@login_required
def recommended_books():
	return render_template("recommended_books.html")


@app.route('/contact')
def contact():
	return render_template("contact.html")


@app.route('/about')
def about():
	return render_template("about.html")


@app.route('/book-details')
def book_details():
	return render_template("book_details.html")


@app.route('/register')
def register():
	return render_template("register.html")


@app.route('/login')
def login():
	return render_template("login.html")


@app.route('/my-profile')
def my_profile():
	return render_template("my_profile.html")


@app.route('/search-results')
def search_results():
	return render_template("search_results.html")
