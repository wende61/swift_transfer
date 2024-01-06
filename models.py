from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import SelectField, StringField, PasswordField, SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf import FlaskForm
from extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    customer = db.relationship('Customers', backref='user', uselist=False)
    
    def set_password(self, password):
        hashed_password = generate_password_hash(password, method='scrypt')
        self.password = hashed_password

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


# Define SwiftConnectRequest model with a foreign key relationship to User
class SwiftConnectRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(255), nullable=False)
    customer_email = db.Column(db.String(255), nullable=False)
    request_details = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    amount = db.Column(db.Float, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    sender = db.relationship('Customers', foreign_keys=[sender_id], backref='sent_requests')
    customer = db.relationship('Customers', foreign_keys=[customer_id], backref='received_requests')
    
class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    customer_email = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    requests = db.relationship('SwiftConnectRequest', backref='customers', lazy=True, foreign_keys=[SwiftConnectRequest.customer_id])

    
class CustomerForm(FlaskForm):
  first_name = StringField('First Name', validators=[DataRequired()])
  last_name = StringField('Last Name', validators=[DataRequired()])
  customer_email = StringField('Customer Email', validators=[DataRequired()])
  address = TextAreaField('Address', validators=[DataRequired()])
  username = StringField('Username')
  submit = SubmitField('Submit')
   
class AdminOnboardForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('customer', 'Customer')], validators=[DataRequired()])
    submit = SubmitField('Onboard')
    

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class SwiftTransferForm(FlaskForm):
    amount = StringField('Amount', validators=[DataRequired()])
    recipient_email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send')

class SwiftTransferEditForm(FlaskForm):
    amount = StringField('Amount', validators=[DataRequired()], render_kw={'readonly': True})
    customer_email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'readonly': True})
    status = SelectField('Status', choices=[('Canceled', 'Cancel'), ('Reversed', 'Reverse'),('Approved', 'Approve'),('Rejected', 'Reject')], validators=[DataRequired()])
    submit = SubmitField('Send')
   
class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Update')
    
class ChangePasswordForm(FlaskForm):
    old_password = StringField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change')