from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField
from wtforms.validators import  Length, EqualTo, Email, DataRequired 
from flask_wtf.file import FileField , FileAllowed ,FileRequired



class LoginForm(FlaskForm):
   username = StringField(label='User Name', validators=[Length(min=2,max=30),DataRequired()])
   password = PasswordField(label='Password',validators=[Length(min = 6, max=30),DataRequired()])
   submit = SubmitField(label='login')



class RegisterForm(FlaskForm):
   username = StringField(label='User Name', validators=[Length(min=2,max=30),DataRequired()])
   email_address = StringField(label='Email Address',validators=[Email(), DataRequired()])
   password1 = PasswordField(label='Password', validators=[Length(min=2,max=30),DataRequired()])
   password2 = PasswordField(label='Confirm Password',validators=[EqualTo('password1'),DataRequired()])
   submit   = SubmitField(label='Register')
 
 
 
class Categoryform(FlaskForm):
   name = StringField(label='Category', validators=[DataRequired()])
   submit   = SubmitField(label='Add Category')
   
 
 
 
class AddItemsform(FlaskForm):
   name = StringField(label='Item Name', validators=[Length(min=2,max=30),DataRequired()])
   price= StringField(label='Price', validators=[DataRequired()])
   stock = StringField(label='Stock',validators=[DataRequired()])
   description = StringField(label='Description',validators=[DataRequired()])
   image_1 = FileField(label='image_1',validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png','gif'])])
   submit   = SubmitField(label='Add product')
 