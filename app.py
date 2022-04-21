from crypt import methods
import email
from flask import Flask ,render_template , request
from flask_wtf import FlaskForm
from wtforms import StringField ,PasswordField
from wtforms.validators import InputRequired
from flask import Flask, render_template, url_for ,request
from flask_sqlalchemy import SQLAlchemy
from creationbd import  Users , Address,Company


app = Flask(__name__)
app.config['SECRET_KEY'] = 'groupe4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupe4:test123@localhost/projetflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Login(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    pwd = PasswordField('pwd')


# @app.route('/')
@app.route('/pagePrincipal')
def pagePrincipal():
    return render_template('pagePrincipal.html')


@app.route('/singin', methods=['GET','POST'])
def form():
    info_user = Login()
    if info_user.validate_on_submit():
        return "valide"
    return render_template('formulaire_de__connxion.html', info_user = info_user)

@app.route('/')
def index():
    return render_template('formulairedajout.html')

@app.route('/adduser', methods=["GET","POST"])
def adduser():
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
    # donne_personnel= Users(name = name , username = username,phone=phone,email=email,website=website)
    # db.session.add(donne_personnel)
    # db.commit()



    return  name 

app.run(debug=True)
# @app.route('/adduser', methods=['get','POST'])
# def adduser():
#     name = request.form['name']
#     username = request.form['username']

