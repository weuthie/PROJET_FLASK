from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupe4:test123@localhost/projetflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Users(db.Model):
    userid = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    username = db.Column(db.String(255),nullable = False)
    email = db.Column(db.String(255),nullable = False)
    phone = db.Column(db.String(255))
    website = db.Column(db.String(255))
    password = db.Column(db.String(10))
    posts = db.relationship('Posts', backref = 'users')
    address = db.relationship('Address', backref = 'users')
    todo = db.relationship('Todo', backref = 'users')
    albums = db.relationship('Albums', backref = 'users')
    company = db.relationship('Company', backref = 'users')
    archive = db.Column(db.Integer,default=1)




class Posts(db.Model):
    postid = db.Column(db.Integer(), primary_key = True) 
    posttitle = db.Column(db.String(255), nullable = False)
    postbody = db.Column(db.String(1000),nullable = False)
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'))
    comments = db.relationship('Comment', backref = 'posts')
    archive = db.Column(db.Integer,default=1)


class Address(db.Model):
    addressid = db.Column(db.Integer(), primary_key = True)
    street = db.Column(db.String(255),nullable = False)
    suite = db.Column(db.String(255),nullable = False)
    city = db.Column(db.String(255),nullable = False)
    zipcode = db.Column(db.String(255),nullable = False)
    geo_lat = db.Column(db.Float(),nullable = False)
    geo_lng = db.Column(db.Float(),nullable = False)
    userid = db.Column(db.Integer(), db.ForeignKey('users.userid'))
    archive = db.Column(db.Integer,default=1)

class Todo(db.Model):
    todoid = db.Column(db.Integer(), primary_key = True) 
    todotitle = db.Column(db.String(255),nullable = False)
    todoetat = db.Column(db.String(20), nullable = False) 
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'))
    archive = db.Column(db.Integer,default=1)


class Albums(db.Model):
    albumid = db.Column(db.Integer(), primary_key = True)
    albumtitle = db.Column(db.String(255),nullable = False)
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'))
    photos = db.relationship('Photos', backref = 'albums')
    archive = db.Column(db.Integer,default=1)



class Photos(db.Model):
    photoid = db.Column(db.Integer(), primary_key = True) 
    phototitle = db.Column(db.String(255),nullable = False)
    photourl = db.Column(db.String(255),nullable = False)
    photothumbnailurl = db.Column(db.String(255),nullable = False)
    albumid = db.Column(db.Integer, db.ForeignKey('albums.albumid'))
    archive = db.Column(db.Integer,default=1)



class Company(db.Model):
    companyid = db.Column(db.Integer(), primary_key = True) 
    companyname =  db.Column(db.String(255),nullable = False)
    companycatchphrase = db.Column(db.String(255),nullable = False)
    companybs = db.Column(db.String(255),nullable = False)
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'))
    archive = db.Column(db.Integer,default=1)

class Comment(db.Model):
    commentid = db.Column(db.Integer(), primary_key = True) 
    commentname =  db.Column(db.String(255),nullable = False)
    commentemail = db.Column(db.String(255),nullable = False)
    commentbody = db.Column(db.Text(),nullable = False)
    postid = db.Column(db.Integer, db.ForeignKey('posts.postid'))
    archive = db.Column(db.Integer,default=1)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()




