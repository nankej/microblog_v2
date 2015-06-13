from app.models import User
from flask_babel import gettext
from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class EditForm(Form):
    username = StringField('username', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_username, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_username = original_username

    def validate(self):
        if not Form.validate(self):
            return False
        if self.username.data == self.original_username:
            return True
        if self.username.data != User.make_valid_username(self.username.data):
            self.username.errors.append(gettext('This username has invalid characters. Please use letters, numbers, dots and underscores only.'))
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            self.username.errors.append(gettext('This username is already in use. Please choose another one.'))
            return False
        return True

class PostForm(Form):
    post = StringField('post', validators=[DataRequired()])

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])