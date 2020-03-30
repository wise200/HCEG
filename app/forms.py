from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.models import User
from app import photos

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    check_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    master_password = PasswordField('Master Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is taken.')

    def validate_master_password(self, password):
        admin = User.query.filter_by(username='admin').first()
        correct = admin.check_password(password.data)
        if not correct:
            raise ValidationError('Invalid Master Password')

class CommentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    text = TextAreaField('Text (1000 character max.)', validators=[DataRequired(), Length(min=1, max=1000)])
    img = FileField('Logo', validators=[FileAllowed(photos, 'Images only.'), FileRequired('File was empty.')])
    submit = SubmitField('Submit')

class PageForm(FlaskForm):
    title = StringField('Page Title', validators=[DataRequired()])
    img = FileField('Banner Image (Optional)', validators=[FileAllowed(photos, 'Images only.')])
    text = TextAreaField('Text (You can use html syntax here.)', validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Submit')
