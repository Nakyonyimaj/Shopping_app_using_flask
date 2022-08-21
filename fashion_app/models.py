
from fashion_app import db , login_manager , bcrypt
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))


      
class User(UserMixin,db.Model):
   id = db.Column(db.Integer,primary_key= True )
   username = db.Column(db.String(length=30),nullable = False,unique = True)
   email_address = db.Column(db.String(length=30),nullable = False,unique = True)
   password= db.Column(db.String(length=60), nullable=False)
   

    
   
   def __init__(self, username, password,  email_address):
      self.username = username
      self.password = bcrypt.generate_password_hash(password)
      self.email_address = email_address
   
        
   
   def __repr__(self):
      return "Username: {}, Email: {} password: {}".format(self.username, self.email_address, self.password)

        
   def verify_password(self, attempted_password):
      return bcrypt.check_password_hash(self.password, attempted_password)
   
   
   
class AddItems(db.Model):
   id = db.Column(db.Integer(), primary_key = True)
   name = db.Column(db.String(),nullable=False)
   price = db.Column(db.Integer(),nullable = False)
   stock = db.Column(db.Integer(),nullable = False)
   description = db.Column(db.String(),nullable=False)
   image_1 = db.Column(db.String(150), nullable=False ,default= 'image.jpg')
   
   
   category_id = db.Column(db.Integer(),db.ForeignKey('category.id'),nullable = False)
   category = db.relationship('Category',backref=db.backref('posts',lazy=True))
   
   
   def __repr__(self):
      return "name: {}, price: {}, stock: {}, description: {}, image_1: {}".format(self.name, self.price, self.stock, self.description, self.image_1)
   

   

   
class Category(db.Model):
   id = db.Column(db.Integer(),primary_key=True)
   name = db.Column(db.String(length=30),nullable = False,unique = True)
   
   def __repr__(self):
      return self.name 
   
   
   

   