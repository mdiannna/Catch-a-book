# -*- coding: utf-8 -*-
from app import app, db
from app import login_manager
from flask import render_template, request, redirect, url_for, session
from flask.ext.login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Library, Book, BooksCarturesti, LibrarieNet


import os
from werkzeug.utils import secure_filename

from settings import UPLOAD_FOLDER

import ocr
from ocr import recognize_ISBN
import sys
import re

def addInitialLibraries():
	carturesti = Library(id=1, name='Carturesti')
	librarie_net = Library(id=2, name='Librarienet')
	db.session.add(carturesti)
	db.session.add(librarie_net)
	db.session.commit()

def moveBooksDataFromTables():
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


def allowed_file(filename):
    ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods = ['GET', 'POST'])
def index():
    status = None
    error = None
    manual_ISBN = None

    FILENAME = "ISBN1.jpg"
    if request.method == 'POST':
        #Read ISBN from input
        manual_ISBN=request.form.get('manualISBNinput', None)
        manual_ISBN=re.sub('[^0-9]','',manual_ISBN)
        print manual_ISBN
        if  manual_ISBN!="":
            return redirect('/ocr_ISBN/' + manual_ISBN)
        #ISBN OCR if no input
        print "post here"
        f = request.files['file']
        if not allowed_file:
            error = 'Error! File type not allowed'
        elif not f:
            error = 'Error! Please choose file'
        if f and allowed_file(f.filename):
            print "current folder:"
            print os.path.dirname(os.path.abspath(__file__))

            FILE_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),app.config['UPLOAD_FOLDER'], FILENAME))
            print FILE_PATH
            f.save(FILE_PATH)
            # f.save(UPLOAD_FOLDER + FILENAME);
            status = 'file uploaded successfully'
            return redirect('/ocr_ISBN/' + str(FILENAME))

    return render_template("index.html", methods = ['GET', 'POST'])


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


@app.route('/instructions')
def instructions():
	return render_template("instructions.html")


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



@app.route('/ocr_ISBN/<string:filename>', methods = ['GET', 'POST'])
def ocr_isbn(filename):


    status = None
    error = None
    manual_ISBN = None

    FILENAME = "ISBN1.jpg"
    if request.method == 'POST':
        print "post here"
        #Read ISBN from input
        manual_ISBN=request.form.get('manualISBNinput2', None)
        manual_ISBN=re.sub('[^0-9]','',manual_ISBN)
        print manual_ISBN
        if  manual_ISBN!="":
            return redirect('/ocr_ISBN/' + manual_ISBN)

        #ISBN OCR if no input

        f = request.files['file']
        if not allowed_file:
            error = 'Error! File type not allowed'
        elif not f:
            error = 'Error! Please choose file'
        if f and allowed_file(f.filename):
            print "current folder:"
            print os.path.dirname(os.path.abspath(__file__))

            FILE_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),app.config['UPLOAD_FOLDER'], FILENAME))
            print FILE_PATH
            f.save(FILE_PATH)
            # f.save(UPLOAD_FOLDER + FILENAME);
            status = 'file uploaded successfully'
            return redirect('/ocr_ISBN/' + str(FILENAME))



    error = None
    if filename == "ISBN1.jpg":
        ISBN = recognize_ISBN(filename);

    if filename.isdigit():
        ISBN = int(filename)

    if ISBN == None:
        error = "ISBN could not be detected properly"

    ISBN = unicode(ISBN)
    print "ISBN:", ISBN
    # Price comparison
    good_price = None
    bad_price = None
    object_Carturesti = Carturesti.query.filter(Carturesti.isbn==ISBN)
    object_Librarie_Min = Librarie_Min.query.filter(Librarie_Min.isbn==ISBN)
    object_Librarie_Max = Librarie_Max.query.filter(Librarie_Max.isbn==ISBN)

    print object_Carturesti.count()
    if object_Carturesti.count() + object_Librarie_Min.count() + object_Librarie_Max.count() == 0:
        error = "Cartea nu a fost gasită în baza de date"
        return render_template("search.html", error=error)
    else:
        print "object Carturesti:", object_Carturesti[0]
        title = object_Carturesti[0].title
        print "titlu:", title
        author = object_Carturesti[0].author
        print "titlu:", author

    librarie_good = 'Carturesti'
    librarie_bad = 'librarie.net'

    link_img = None
    if object_Carturesti.count()>0:
        if object_Librarie_Min.count()>0:
            link_img = object_Librarie_Min[0].img
            if float(object_Carturesti[0].price.replace(',', '.')) < float(object_Librarie_Min[0].price.replace(',', '.')):
                good_price = object_Carturesti[0]
                bad_price = object_Librarie_Min[0]
                librarie_good = 'Carturesti'
                librarie_bad = 'librarie.net'
            else:
                good_price = object_Librarie_Min[0]
                bad_price = object_Carturesti[0]
                librarie_good = 'librarie.net'
                librarie_bad = 'Carturesti'
        else:
            good_price = object_Carturesti[0]
            librarie_good = 'Carturesti'
    else:
        if object_Librarie_Max.count()>0:
            link_img = object_Librarie_Max[0].img
            good_price = object_Librarie_Max[0]
            librarie_good = 'librarie.net'


    if author:
        same_author_objects = find_same_author_objects(author, ISBN)
        RecImgLinks = get_recommended_image_links(same_author_objects)
    if good_price:
        good_price=good_price.price
    if bad_price:
        bad_price=bad_price.price



    return render_template("search.html", title=title, author=author,
             good_price=good_price, bad_price=bad_price, isbn=ISBN,
             librarie_good=librarie_good, librarie_bad=librarie_bad, error=error,
             same_author_objects=same_author_objects, image_link=link_img, rec_img_links=RecImgLinks)
