from app import app, db
from app import login_manager
from flask import render_template, request, redirect, url_for, session, flash, Response, abort
from urlparse import urlparse, urljoin

from flask.ext.login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Library, Book, BooksCarturesti, LibrarieNet, Librarie_Min
import re
from app.forms import RegistrationForm
from functools import wraps

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
        email    = request.values.get('email')
        password = generate_password_hash(request.values.get('password'))

    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    print("User registered")
    return redirect('/')



# def is_safe_url(target):
#     ref_url = urlparse(request.host_url)
#     test_url = urlparse(urljoin(request.host_url, target))
#     return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    # form = LoginForm()
    if request.method=='POST':
        email    = request.values.get('email')
        password = request.values.get('password')
        print email 

        user = User.query.filter(User.email==email).first();
        if check_password_hash(user.password, password):
            login_user(user)

            flash('Logged in successfully.')

            next = request.args.get('next')
            print request.path
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
    print current_user.is_authenticated()

    message = "Hello"

    status = None
    error = None
    manual_ISBN = None

    FILENAME = "ISBN1.jpg"


    if request.method == 'POST':
        #Read ISBN from input
        manual_ISBN=request.form.get('manualISBNinput', None)
        manual_ISBN=re.sub('[^0-9]','',manual_ISBN)
        ##print manual_ISBN
        if  manual_ISBN!="":
            return redirect('/ocr_ISBN/' + manual_ISBN)
        #ISBN OCR if no input
        ##print "post here"
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
            return redirect('/ocr_ISBN/' + str(FILENAME))

    # return render_template("index.html", message=message, registerform=registerform)
    return render_template("index.html", message=message)


@app.route('/ocr_ISBN/<string:filename>', methods = ['GET', 'POST'])
@login_required
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
            return redirect('/ocr_ISBN/' + str(FILENAME))



    error = None
    if filename == "ISBN1.jpg":
        ISBN = recognize_ISBN(filename);

    if filename.isdigit():
        ISBN = int(filename)

    if ISBN == None:
        error = "ISBN could not be detected properly"

    ISBN = str(ISBN)
    ##print "ISBN:", ISBN
    # Price comparison
    good_price = None
    bad_price = None
    object_Carturesti = BooksCarturesti.query.filter(BooksCarturesti.isbn==ISBN).first()
    object_Librarie_Min = Librarie_Min.query.filter(Librarie_Min.isbn==ISBN).first()
    
    ##print object_Carturesti   
    ##print object_Librarie_Min

    title = "No title found"
    author = "No author found"

    if object_Carturesti:
        title = object_Carturesti.title
        author=object_Carturesti.author
    return render_template("search.html", title=title, author=author, isbn=ISBN)       



def find_same_author_objects(author, initial_isbn):
    object_Carturesti = BooksCarturesti.query.filter(BooksCarturesti.author==author, BooksCarturesti.isbn!=initial_isbn)
    rec=[]
    # Eliminare recomandari duplicate
    for item in object_Carturesti:
        if item not in rec:
            rec.append(item)

    if len(rec)>=1:
        obj = Librarie_Min.query.filter(Librarie_Min.isbn==rec[0].isbn)
        if obj.count()>=1:
            if obj[0].price < rec[0].price:
                rec[0].price = obj[0].price
                rec[0].link = obj[0].link
    if len(rec)>=2:
        obj = Librarie_Min.query.filter(Librarie_Min.isbn==rec[1].isbn)
        if obj.count()>=1:
            if obj[0].price < rec[1].price:
                rec[1].price = obj[0].price
                rec[1].link = obj[0].link
    if len(rec)>=3:
        obj = Librarie_Min.query.filter(Librarie_Min.isbn==rec[2].isbn)
        if obj.count()>=1:
            if obj[0].price < rec[2].price:
                rec[2].price = obj[0].price
                rec[2].link = obj[0].link
    if len(rec)>=4:
        obj = Librarie_Min.query.filter(Librarie_Min.isbn==rec[3].isbn)
        if obj.count()>=1:
            if obj[0].price < rec[3].price:
                rec[3].price = obj[0].price
                rec[3].link = obj[0].link
    return rec



def get_recommended_image_links(rec):
    rec_img=[]
    if len(rec)>=1:
        obj = Librarie_Min.query.filter(Librarie_Min.isbn==rec[0].isbn)
        if obj.count()>=1:
            rec_img.append(obj[0].img)
        else:
            rec_img.append(None)
    if len(rec)>=2:
        obj = Librarie_Min.query.filter(Librarie_Min.isbn==rec[1].isbn)
        if obj.count()>=1:
            rec_img.append(obj[0].img)
        else:
            rec_img.append(None)
    if len(rec)>=3:
        obj = Librarie_Min.query.filter(Librarie_Min.isbn==rec[2].isbn)
        if obj.count()>=1:
            rec_img.append(obj[0].img)
        else:
            rec_img.append(None)
    if len(rec)>=4:
        obj = Librarie_Min.query.filter(Librarie_Min.isbn==rec[3].isbn)
        if obj.count()>=1:
            rec_img.append(obj[0].img)
        else:
            rec_img.append(None)
    return rec_img


def allowed_file(filename):
    ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



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


