from app import db,login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import ForeignKey


@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)

# usermixin is only used fo login and logout functions
class User(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(20), unique=True, nullable=False)
    email= db.Column(db.String(50),unique=True, nullable=False)
    password= db.Column(db.String(256), nullable=False)
    date_created= db.Column(db.DateTime, nullable= False, default=datetime.utcnow)
    #this references all the posts the user has created
    #the backref is what allows us to get the info from the post to link to the user
    posts=db.relationship('Post', backref='user')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User|{self.username}>"

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Post( db.Model):
     id= db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(100), nullable= False)
     body = db.Column(db.String(1000), nullable= False)
     date_created= db.Column(db.DateTime, nullable= False, default=datetime.utcnow)
     # need an author to assign to the post. Foriegn key??
     #ondelete will get rid of all posts that the user has created
     user_id= db.Column (db.Integer,db.ForeignKey('user.id'), nullable=False)

     def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

     def __repr__(self):
         return f"<Post | {self.title}>"

     def get_user(self):
         return User.query.filter_by(id=self.user_id).first().username





     
   
