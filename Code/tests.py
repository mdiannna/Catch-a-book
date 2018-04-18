#!flask/bin/python
# useful resources:
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-unit-testing-legacy
# http://www.patricksoftwareblog.com/unit-testing-a-flask-application/
# https://docs.python.org/2/library/unittest.html
# https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
# https://damyanon.net/post/flask-series-testing/

import os
import unittest

# from config import basedir
from app import app, db
from app.models import User
from settings import db_path

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = db_path
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ################################
    # Test pages
    ################################
    
    # Test main page
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # Test about page 
    def test_about_page(self):
        response = self.app.get('/about', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # Test contact page - GET
    def test_contact_page(self):
        response = self.app.get('/contact', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # Test register page - GET
    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    # Test login page - GET
    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # Test logout page - GET
    def logout(self):
        response = self.app.get(
            '/logout',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)


    def register(self, email, password, confirm):
        response = self.app.post(
            '/register',
            data=dict(email=email, password=password, confirm=confirm),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

 
    def login(self, email, password):
        respone = self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        

    ################################
    # Test database
    ################################

    # Test register user
    def test_register_user(self):
        test_email = 'john@example.com'
        test_username = 'john'
        test_password = '123'
        existing_users_with_email_nr = User.query.filter_by(email = test_email).count()
        user = User(email=test_email, username=test_username, password=test_password)
        db.session.add(user)
        db.session.commit()
        print user.id
        current_users_with_email_nr = User.query.filter_by(email = test_email).count()
        self.assertEqual(existing_users_with_email_nr+1, current_users_with_email_nr)

       
    # def test_avatar(self):
    #     u = User(email='john@example.com')
    #     # avatar = u.username("test")
    #     # expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
    #     assert avatar[0:len(expected)] == expected

    # def test_make_unique_nickname(self):
    #     u = User(email='john@example.com')
    #     db.session.add(u)
    #     db.session.commit()
    #     nickname = User.make_unique_nickname('john')
    #     assert nickname != 'john'
    #     u = User(email='susan@example.com')
    #     db.session.add(u)
    #     db.session.commit()
    #     nickname2 = User.make_unique_nickname('john')
    #     assert nickname2 != 'john'
    #     assert nickname2 != nickname

if __name__ == '__main__':
    unittest.main()