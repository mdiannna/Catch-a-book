from flask.ext.wtf import Form
from wtforms import TextField, IntegerField, PasswordField, SubmitField, SelectField
from wtforms import validators
from wtforms.validators import DataRequired
from wtforms.fields import StringField
from wtforms.widgets import TextArea
from werkzeug.datastructures import MultiDict


class uploadISBNForm(Form):
    upload_isbn = SubmitField('Upload poza isbn')


class ContactForm(Form):
    nume = StringField(u'nume:')
    email = StringField(u'email:')
    telefon = StringField(u'telefon:')
    mesaj = StringField(u'mesaj:', widget=TextArea())
    submit = SubmitField('Submit')  

    def reset(self):
        blankData = MultiDict([ ('csrf', self.generate_csrf_token()  ) ])
        self.process(blankData)


class LoginForm(Form):
    # username = StringField('Username', [validators.Length(min=6, max=35)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Submit')  


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=6, max=35)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Submit')  
