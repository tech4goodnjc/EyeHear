from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
 
#Initialising login manager and database
login = LoginManager()
db = SQLAlchemy()
 
class UserModel(UserMixin, db.Model):
    #Create table users
    __tablename__ = "users"
    
    productkey = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100), primary_key=True)
    password_hash = db.Column(db.String())
 
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
     
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    #Return username if queried
    def get_id(self):
        return self.username
 
 
@login.user_loader
def load_user(username):
    return UserModel.query.get(username)