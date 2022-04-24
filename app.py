from crypt import methods
import email
from wsgiref.validate import validator
from click import password_option
from flask import Flask, redirect ,render_template , request
from flask_wtf import FlaskForm
from sqlalchemy import false
from wtforms import StringField ,PasswordField
from wtforms.validators import InputRequired,Email,Length,ValidationError
from flask import Flask, render_template, url_for ,request
from flask_sqlalchemy import SQLAlchemy
from creationbd import  Users , Address,Company


app = Flask(__name__)
app.config['SECRET_KEY'] = 'groupe4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupe4:test123@localhost/projetflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = false
db = SQLAlchemy(app)

#### Validation formulaire Dabakh #######

class Login(FlaskForm):
    email = StringField('email', validators=[InputRequired(),Email()])
    pwd = PasswordField('pwd',validators = [InputRequired(),Length(min=4,max=10)])

    def validation_email(self,email):
        if email.data == "root@domain.com":
            raise ValidationError("cette email est déja enrégistrer")


# recuperation des donne de l'api

@app.route('/')
def index():
    return render_template('pageindex.html')

@app.route('/pagePrincipal')
def pagePrincipal():
    users= Users.query.all()
    return render_template('pagePrincipal.html',users=users)


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

@app.route('/profil')
def profil():
    return render_template('profil.html')

# ----------------END DOING BY LOUFA---------------
@app.route('/singin', methods=['GET','POST'])
def form():
    info_user = Login()
    if info_user.validate_on_submit():
        return "valide"
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
        try:
            db.session.add(donne_personnel)
            db.session.commit()
            return  redirect('/pagePrincipal') 
        except:
            db.session.rollback()
            return  "erreur"
    else:
        return render_template('formulairedajout.html')
app.run(debug=True)

