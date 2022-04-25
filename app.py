from crypt import methods
import email
from wsgiref.validate import validator
from click import password_option
from flask import Flask, redirect ,render_template , request
from flask_wtf import FlaskForm
from wtforms import StringField ,PasswordField ,IntegerField ,SubmitField
from sqlalchemy import false
from wtforms import StringField ,PasswordField
from wtforms.validators import InputRequired,Email,Length,ValidationError
from flask import Flask, render_template, url_for ,request
from flask_sqlalchemy import SQLAlchemy
from creationbd import  Users , Address,Company

from requests import get


app = Flask(__name__)
app.config['SECRET_KEY'] = 'groupe4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupe4:test123@localhost/projetflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = false
db = SQLAlchemy(app)

#### Validation formulaire Dabakh #######

class Login(FlaskForm):
    # email = StringField('email', validators=[InputRequired(),Email()])
    # pwd = PasswordField('pwd',validators = [InputRequired(),Length(min=4,max=10)])

    def validation_email(self,email):
        if email.data == "root@domain.com":
            raise ValidationError("cette email est déja enrégistrer")


#formulaire pour gerer l'entreer

class Gerenmbre(FlaskForm):
    nbchoix=IntegerField('',validators=[InputRequired()])
    btn = SubmitField('Charger')

# recuperation des donne de l'api

@app.route('/')
def index():
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

def getAndInsertDataFromApi(endpoint, nbelt):
    dataFromApi = get('https://jsonplaceholder.typicode.com/'+endpoint)
    data = dataFromApi.json()
    


@app.route('/pageUser')
def pageUser():
    return render_template('pageUser.html')
# ----------------------------------------------------
@app.route('/userPost')
def userPost():
    return render_template('userPost.html')

# ---------------------------------------------------


@app.route('/album')
def album():
    return render_template('album.html')

@app.route('/photo')
def photo():
    return render_template('photo.html')

@app.route('/todo')
def todo():
    return render_template('todo.html')

# @app.route('/addtodo')
# def addtodo():
#     if request.method == "POST":
#         title = request.form['title']
#         etat = request.form['etat']


@app.route('/profil')
def profil():
    return render_template('profil.html')

# ----------------END DOING BY LOUFA---------------
@app.route('/singin', methods=['GET','POST'])
def form():
    info_user = Login()
    if info_user.validate_on_submit():
        return render_template('pageUser.html')
    return render_template('formulaire_de__connxion.html', info_user = info_user)

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
        userid = Users.query.all()

        if len(userid) == 0:
            addres = Address(street = street, suite = suite, city = city, zipcode = zipcode, geo_lat = latitude, geo_lng = longitude, userid = 1)

            company = Company(companyname = companyname, companycatchphrase = catchPhrase, companybs = bs, userid = 1)

        else:
            addres = Address(street = street, suite = suite, city = city, zipcode = zipcode, geo_lat = latitude, geo_lng = longitude, userid = userid[-1].userid+1)
        
            company = Company(companyname = companyname, companycatchphrase = catchPhrase, companybs = bs, userid = userid[-1].userid+1)
        try:
            db.session.add(donne_personnel)
            db.session.add(addres)
            db.session.add(company)
            db.session.commit()
            return  redirect('/pagePrincipal') 
        except:
            db.session.rollback()
            print(userid[-1].userid)
            return  "erreur"
    else:
        return render_template('formulairedajout.html')

app.run(debug=True)

