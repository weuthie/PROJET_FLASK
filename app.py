from crypt import methods
import email
from flask import Flask ,render_template
from flask_wtf import FlaskForm
from wtforms import StringField ,PasswordField
from wtforms.validators import InputRequired
from flask import Flask, render_template, url_for ,request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'groupe4'

class Login(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    pwd = PasswordField('pwd')


# @app.route('/')
@app.route('/pagePrincipal')
def pagePrincipal():
    return render_template('pagePrincipal.html')

# ----------------------------------------------------
@app.route('/userPost')
def userPost():
    return render_template('userPost.html')

# ---------------------------------------------------


@app.route('/singin', methods=['GET','POST'])
def form():
    info_user = Login()
    if info_user.validate_on_submit():
        return "valide"
    return render_template('formulaire_de__connxion.html', info_user = info_user)


app.run(debug=True)
# @app.route('/adduser', methods=['get','POST'])
# def adduser():
#     name = request.form['name']
#     username = request.form['username']

