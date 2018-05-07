from app import app, db
from app import login_manager
from flask import render_template, request, redirect, url_for, session
from flask.ext.login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Library, Book, BooksCarturesti, LibrarieNet


def addInitialLibraries():
	carturesti = Library(id=1, name='Carturesti')
	librarie_net = Library(id=2, name='Librarienet')
	db.session.add(carturesti)
	db.session.add(librarie_net)
	db.session.commit()

def moveBooksDataFromTables():
	carturesti_books = BooksCarturesti.query.all()
	for book in carturesti_books:
		new_book = Book(title=book.title, 
			author=book.author,
			isbn=book.isbn,
			link=book.link,
			editura=book.editura,
			price=book.price,
			# img=book.img,
			library_id=1) 
		db.session.add(new_book)
		db.session.commit()

	librarie_net_books = LibrarieNet.query.all()
	for book in librarie_net_books:
		new_book = Book(title=book.title, 
			# author=book.author,
			isbn=book.isbn,
			link=book.link,
			# editura=book.editura,
			price=book.price,
			img=book.img,
			library_id=2) 
		db.session.add(new_book)
		db.session.commit()

	# print carturesti_books[0].title

# TODO: delete after finishing with the database
# @app.route('/db')
# def index():
# 	message = "Hello"
# 	addInitialLibraries()
# 	moveBooksDataFromTables()
#	# return render_template("index.html", message=message)


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


@app.route('/my-profile')
def my_profile():
	return render_template("my_profile.html")


@app.route('/search-results')
def search_results():
	return render_template("search_results.html")
