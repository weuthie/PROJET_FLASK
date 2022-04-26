from crypt import methods
import email
import re
from wsgiref.validate import validator
from click import password_option
from flask import Flask, flash, redirect ,render_template , request, session  
from flask_wtf import FlaskForm
from wtforms import StringField ,PasswordField ,IntegerField ,SubmitField
from sqlalchemy import false, null
from wtforms import StringField ,PasswordField
from wtforms.validators import InputRequired,Email,Length,ValidationError
from flask import Flask, render_template, url_for ,request
from flask_sqlalchemy import SQLAlchemy
from creationbd import  *
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'groupe4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupe4:test123@localhost/projetflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = false
db = SQLAlchemy(app)

#### Validation formulaire Dabakh #######

class Login(FlaskForm):
    email = StringField('email', validators=[InputRequired(),Email()])
    pwd = PasswordField('pwd')
# render_template('formulaire_de__connxion.html')
    # def validation_email(self,email):
    #     if email.data == "root@domain.com":
    #         raise ValidationError("cette email est déja enrégistrer")


#formulaire pour gerer l'entreer

class Gerenmbre(FlaskForm):
    nbchoix=IntegerField('',validators=[InputRequired()])
    btn = SubmitField('Charger')



@app.route('/')
def index():
    session.pop('userid',None)
    return render_template('pageindex.html')

@app.route('/pagePrincipal', methods=["POST","GET"])
def pagePrincipal():
    nb = 0
    users=[]
    nbuser = 0
    formulair= Gerenmbre()
    if formulair.validate_on_submit():
        nb = formulair.nbchoix.data
        users = Users.query.all()
        nbuser =len(users)
    return render_template('pagePrincipal.html',users=users,nb=nb,nbuser=nbuser,formulair=formulair)


@app.route('/pageUser')
def pageUser():
    users = Users.query.all()
    return render_template('pageUser.html' , users=users)
# ----------------------------------------------------
@app.route('/userPost')
def userPost():
    
    return render_template('userPost.html')

# ---------------------------------------------------


@app.route('/album/')
def album():
    if 'userid' in session:
        return render_template('album.html')
    else:
        return redirect('/pagePrincipal')

@app.route('/photo')
def photo():
    if 'userid' in session:
        return render_template('photo.html')
    else:
        return redirect('/pagePrincipal')
@app.route('/todo')

def todo():
    if 'userid' in session:
        return render_template('todo.html')
    else:
        return redirect('/pagePrincipal')
@app.route('/profil')
def profil():
    if 'userid' in session:
        return render_template('profil.html')
    else:
        return redirect('/pagePrincipal')
# ----------------END DOING BY LOUFA---------------
@app.route('/singin/<int:userid>', methods=['GET','POST'])
def form(userid):

    users = Users.query.get_or_404(userid)
    info_user = Login()
    if info_user.pwd.data == users.password:
        session["userid"]=users.userid
        return render_template('pageUser.html',users=users) 
    
    return render_template('formulaire_de__connxion.html', info_user = info_user,users=users )

@app.route('/adduser', methods=["GET","POST"])
def adduser():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        website = request.form['website']
        street = request.form['street']
        suite = request.form['suite']
        city = request.form['city']
        zipcode = request.form['zipcode']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        companyname = request.form['companyname']
        catchPhrase = request.form['catchPhrase']
        bs = request.form['bs']
        donne_personnel= Users(name = name , username = username,phone=phone,email=email,website=website, password=12)

        try:
            db.session.add(donne_personnel)
            db.session.commit()
            return  redirect('/pagePrincipal') 
        except:
            db.session.rollback()
            return  "erreur"
    else:
        return render_template('formulairedajout.html')
# --------------------ADD BY DEME-----------------------
def addPost():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        donnee_posts = Posts(posttitle = title, comments = content)


def addTodo():
    if request.method == 'POST':
        title = request.form['title']
        etat = request.form['etat']
        donnee_todo = Todo(todotitle = title)

def addAlbums():
    if request.method == 'POST':
        title = request.form('title')
        donnee_Albums = Albums(albumtitle = title)

def addPhotos():
    if request.method == 'POST':
        title = request.form('title')
        url = request.form('url')
        thumb = request.form('thumbnailUrl')
        donnee_Photo = Photos(phototitle = title, photourl = url, photothumbnailurl = thumb)


        

# --------------------------END--------------------------
app.run(debug=True)

