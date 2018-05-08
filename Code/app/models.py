from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from app import db


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def is_active(self):
        return True


class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    isbn = db.Column(db.String(50))
    link = db.Column(db.String(100))
    editura = db.Column(db.String(100))
    price = db.Column(db.String(20))
    img = db.Column(db.String(100))

    library_id = db.Column(db.Integer, db.ForeignKey('library.id'), nullable=False)
    library = db.relationship('Library', backref=db.backref('books', lazy=True))



# TO delete
class BooksCarturesti(db.Model):
    # __tablename__ = "books_carturesti"
    __tablename__ = "books_main"
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    isbn = db.Column(db.String(50))
    # link = db.Column(db.String(100))
    editura = db.Column(db.String(100))
    # price = db.Column(db.String(20))
    # img = db.Column(db.String(100))

class LibrarieNet(db.Model):
    __tablename__ = "books_librarie_big"
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    # author = db.Column(db.String(100))
    isbn = db.Column(db.String(50))
    link = db.Column(db.String(100))
    # editura = db.Column(db.String(100))
    price = db.Column(db.String(20))
    img = db.Column(db.String(100))





# ###############3
# 
# 

class Carturesti(db.Model):
    __tablename__ = 'books_carturesti'
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(100), nullable=False)
    author = db.Column(db.Unicode(100))
    isbn = db.Column(db.Unicode(50))
    link = db.Column(db.Unicode(100))
    editura = db.Column(db.Unicode(100))
    price = db.Column(db.Unicode(20))

    @property
    def serialize(self):
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'editura': self.editura,
            'link': self.link,
            'price': self.price
        }


# CREATE TABLE books_librarie_small ( book_id INTEGER NOT NULL, title VARCHAR(100) NOT NULL,
# isbn VARCHAR(50), link VARCHAR(100), price VARCHAR(20), img VARCHAR(100), PRIMARY KEY (book_id) )
class Librarie_Min(db.Model):
    __tablename__ = 'books_librarie_small'
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(100), nullable=False)
    isbn = db.Column(db.Unicode(50))
    link = db.Column(db.Unicode(100))
    price = db.Column(db.Unicode(20))
    img = db.Column(db.Unicode(100))

    @property
    def serialize(self):
        return {
            'title': self.title,
            'isbn': self.isbn,
            'link': self.link,
            'price': self.price,
            'img': self.img
        }

# CREATE TABLE books_librarie_big ( book_id INTEGER NOT NULL, title VARCHAR(100) NOT NULL,
# isbn VARCHAR(50), link VARCHAR(100), price VARCHAR(20), img VARCHAR(100), PRIMARY KEY (book_id) )
# class Librarie_Max(db.Model):
#     __tablename__ = 'books_librarie_big'
#     book_id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.Unicode(100), nullable=False)
#     isbn = db.Column(db.Unicode(50))
#     link = db.Column(db.Unicode(100))
#     price = db.Column(db.Unicode(20))
#     img = db.Column(db.Unicode(100))

#     @property
#     def serialize(self):
#         return {
#             'title': self.title,
#             'isbn': self.isbn,
#             'link': self.link,
#             'price': self.price,
#             'img': self.img
#         }