from app import app, db
from app import login_manager
from flask import render_template, request, redirect, url_for, session, flash, Response, abort

from flask.ext.login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from app.models import User, Library, Book, BooksCarturesti, LibrarieNet, Librarie_Min
from app.models import User, Library, Book
import re
from app.forms import RegistrationForm
from functools import wraps
import os
from app.ocr import recognize_ISBN
import random

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None


def addInitialLibraries():
    carturesti = Library(id=1, name='Carturesti')
    librarie_net = Library(id=2, name='Librarienet')
    db.session.add(carturesti)
    db.session.add(librarie_net)
    db.session.commit()

def moveBooksDataFromTables():
    # carturesti_books = BooksCarturesti.query.all()
    carturesti_books = Book.query.all()
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

    # ##print carturesti_books[0].title

# TODO: delete after finishing with the database
# @app.route('/db')
# def index():
#   message = "Hello"
#   addInitialLibraries()
#   moveBooksDataFromTables()
#   # return render_template("index.html", message=message)


@app.route('/register', methods = ['GET', 'POST'])
def registerUser():
    if request.method == 'POST':
        email      = request.values.get('email')
        first_name = request.values.get('first_name')
        last_name  = request.values.get('last_name')
        password   = generate_password_hash(request.values.get('password'))

    user = User(email=email, password=password, first_name=first_name, last_name=last_name)
    db.session.add(user)
    db.session.commit()
    print("User registered")
    return redirect('/')


def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method=='POST':
        email    = request.values.get('email')
        password = request.values.get('password')
        # print email

        user = User.query.filter(User.email==email).first();
        if check_password_hash(user.password, password):
            login_user(user)

            flash('Logged in successfully.')

            next = request.args.get('next')
            #print request.path
            # return redirect(request.path)
            # return redirect_back('/')
            return redirect('/')

        else:
            return abort(400)

        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        # if not is_safe_url(next):
        #     return abort(400)

        # return flask.redirect(next or flask.url_for('index'))
    # next = request.args.get('next')
    # return redirect(next or '/')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')
   

@app.route('/', methods = ['GET', 'POST'])
# @login_required
def index():
    #print current_user.is_authenticated()

    message = "Hello"

    status = None
    error = None
    manual_ISBN = None

    FILENAME = "ISBN1.jpg"


    if request.method == 'POST':
        #Read ISBN from input
        manual_ISBN=request.form.get('manualISBNinput', None)
        manual_ISBN=re.sub('[^0-9]','',manual_ISBN)

        print(manual_ISBN)
        if  manual_ISBN!="":
            return redirect('/ocr_ISBN/' + manual_ISBN)
        #ISBN OCR if no input
        ##print "post here"
        f = request.files['file']
        print(f)
        if not allowed_file:
            error = 'Error! File type not allowed'
        elif not f:
            error = 'Error! Please choose file'
        if f and allowed_file(f.filename):
            # print "current folder:"
            #print os.path.dirname(os.path.abspath(__file__))

            FILE_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),app.config['UPLOAD_FOLDER'], FILENAME))
            ##print FILE_PATH
            f.save(FILE_PATH)
            # f.save(UPLOAD_FOLDER + FILENAME);
            status = 'file uploaded successfully'
            print(status)
            # return redirect('/ocr_ISBN/' + str(FILENAME))
            return redirect('/ocr_ISBN/' + FILENAME.encode('utf-8'))

    # return render_template("index.html", message=message, registerform=registerform)
    return render_template("index.html", message=message)


@app.route('/ocr_ISBN/<string:filename>', methods = ['GET', 'POST'])
# @login_required
def ocr_isbn(filename):


    status = None
    error = None
    manual_ISBN = None

    FILENAME = "ISBN1.jpg"
    if request.method == 'POST':
        ##print "post here"
        #Read ISBN from input
        manual_ISBN=request.form.get('manualISBNinput2', None)
        manual_ISBN=re.sub('[^0-9]','',manual_ISBN)
        ##print manual_ISBN
        if  manual_ISBN!="":
            return redirect('/ocr_ISBN/' + manual_ISBN)

        #ISBN OCR if no input

        f = request.files['file']
        if not allowed_file:
            error = 'Error! File type not allowed'
        elif not f:
            error = 'Error! Please choose file'
        if f and allowed_file(f.filename):
            ##print "current folder:"
            ##print os.path.dirname(os.path.abspath(__file__))

            FILE_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),app.config['UPLOAD_FOLDER'], FILENAME))
            ##print FILE_PATH
            f.save(FILE_PATH)
            # f.save(UPLOAD_FOLDER + FILENAME);
            status = 'file uploaded successfully'
            # return redirect('/ocr_ISBN/' + str(FILENAME))
            return redirect('/ocr_ISBN/' + FILENAME.encode('utf-8'))



    error = None
    if filename == "ISBN1.jpg":
        ISBN = recognize_ISBN(filename);

    if filename.isdigit():
        ISBN = int(filename)

    if ISBN == None:
        error = "ISBN could not be detected properly"

    ISBN = str(ISBN)
    # ISBN = ISBN.encode('utf-8')
    
    book = None
    book_second_price = None
    
    # book = BooksCarturesti.query.filter(BooksCarturesti.isbn==ISBN).first()
    books = Book.query.filter(Book.isbn==ISBN).order_by('price').paginate(1, 2, False).items
    if len(books) > 0:
        book = books[0]
        #print book.price
    if len(books) > 1:
        book_second_price = books[1]

    title = "-"
    author = "-"
    price="-"
    library="-"
    link="-"

    search_result = None
    recommended_books=None

    if book:
        title = book.title
        author=book.author
        price=book.price
        library=book.library
        link=book.link

        search_result = book
        
        libraries = Library.query.all()
        library_ids = []

        for library in libraries:
            library_ids.append(library.id)

        # print (library_ids)
        # print (random.choice(library_ids))

        recommended_books = Book.query.filter_by(author=book.author, library_id=random.choice(library_ids) ).all()
        if not recommended_books:
            recommended_books = Book.query.filter_by(author=book.author, library_id=random.choice(library_ids) ).all()

        # recommended_books_ids
        # print (recommended_books)

    if search_result and current_user.is_authenticated():
        # newBook = Book(
        #         title=title,
        #         author=author,
        #         price=price,
        #         library=library,
        #         link=link
        #     )
        current_user.books.append(search_result)
        db.session.commit()

        
    # else:
        # search_result.title = "-"
        # search_result.author = "-"
        # search_result.price = 0
        # search_result.library = "-"
        # search_result.link = "-"
    

    return render_template("search.html", book=search_result, recommended_books=recommended_books, book_second_price=book_second_price, isbn=ISBN)       




def allowed_file(filename):
    ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS




@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/my-profile')
def my_profile():
    email = current_user.email
    first_name = current_user.first_name
    last_name = current_user.last_name

    books = current_user.books
    return render_template("my_profile.html", email=email, first_name=first_name, last_name=last_name, books=books)


