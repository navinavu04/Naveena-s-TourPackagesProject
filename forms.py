from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed

class VendorRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class PackageForm(FlaskForm):
     title = StringField('Title', validators=[DataRequired()])
     description = TextAreaField('Description', validators=[DataRequired()])
     price = FloatField('Price', validators=[DataRequired()])
     location = StringField('Location', validators=[DataRequired()])
     duration =StringField('Duration (in days)', validators=[DataRequired()])
     submit = SubmitField('Create Package')
     image = FileField('Package Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])