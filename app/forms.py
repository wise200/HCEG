from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.models import User

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
