from crypt import methods
import email
from pickletools import OpcodeInfo
from wsgiref.validate import validator
from click import password_option
from flask import Flask, redirect ,render_template , request, session, url_for, flash  
from flask_wtf import FlaskForm
from wtforms import StringField ,PasswordField ,IntegerField ,SubmitField
from sqlalchemy import false, null
from wtforms import StringField ,PasswordField
from wtforms.validators import InputRequired,Email,Length,ValidationError
# from flask import Flask, render_template, url_for ,request
from flask_sqlalchemy import SQLAlchemy
import folium 


from creationbd import  *
import requests 
from requests import get



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

        getAndInsertDataFromApi('users', nb)

        users = Users.query.all()
        nbuser =len(users)
    return render_template('pagePrincipal.html',users=users,nb=nb,nbuser=nbuser,formulair=formulair)

# -------------------BEGIN API PROCESS--------------------

def commitInsert(dataForTable):
    try:
        db.session.add(dataForTable)
        # db.session.commit()
    except:
        db.session.rollback()
        return "erreur"


URL = 'https://jsonplaceholder.typicode.com/'
def getAndInsertDataFromApi(endpoint, nbelt):
    isEmpty = Users.query.all()
    userDataFromApi = get(URL+endpoint)
    data = userDataFromApi.json()
    # if len(isEmpty) == 0:
    if len(isEmpty) == 0:
        # dataFromApi = get('https://jsonplaceholder.typicode.com/'+endpoint)
        # data = dataFromApi.json()
        if nbelt > len(data):
            stepApi = len(data)
        else:
            stepApi = nbelt
        for i in range(stepApi):

            personalDataFromApi = Users(userid = data[i].get('id'), name = data[i].get('name') , username = data[i].get('username'),phone=data[i].get('phone'),email=data[i].get('email'),website=data[i].get('website'), password=12)
            
            addresFromApi = Address(addressid = data[i].get('id'), street = data[i]['address']['street'], suite = data[i]['address']['suite'], city = data[i]['address']['city'], zipcode = data[i]['address']['zipcode'], geo_lat = data[i]['address']['geo']['lat'], geo_lng = data[i]['address']['geo']['lat'], userid = data[i].get('id'))

            companyFromApi = Company(companyid = data[i].get('id'), companyname = data[i]['company']['name'], companycatchphrase = data[i]['company']['catchPhrase'], companybs = data[i]['company']['bs'], userid = data[i].get('id'))

            userPostFromApi = get(URL+endpoint+'/'+str(i+1)+'/posts')
            postData = userPostFromApi.json()
            userAlbumFromApi = get(URL+endpoint+'/'+str(i+1)+'/albums')
            albumData = userAlbumFromApi.json()
            userTodoFromApi = get(URL+endpoint+'/'+str(i+1)+'/todos')
            todoData = userTodoFromApi.json()

            for j in range(len(postData)):
                postFromApi = Posts(postid = postData[j].get('id'), posttitle = postData[j].get('title'), postbody = postData[j].get('body'), userid = postData[j].get('userId'))

                # postCommentFromApi = get(URL+'posts/'+str(j+1)+'/comments')
                # commentData = postCommentFromApi.json()
                # for k in range(len(commentData)):
                #     commentFromApi = Comment(commentid = commentData[k].get('id'),commentname = commentData[k].get('name'),commentemail = commentData[k].get('email'),commentbody = commentData[k].get('body'), postid = commentData[k].get('postId'))

                #     commitInsert(commentFromApi)
                commitInsert(postFromApi)

                # try:
                #     db.session.add(postFromApi)
                # except:
                #     db.session.rollback()
                #     return "erreur"
            for j in range(len(albumData)):
                albumFromApi = Albums(albumid = albumData[j].get('id'), albumtitle = albumData[j].get('title'), userid = albumData[j].get('userId'))

                commitInsert(albumFromApi)
                # try:
                #     db.session.add(albumFromApi)
                # except:
                #     db.session.rollback()
                #     return "erreur"

            for j in range(len(todoData)):
                todoFromApi  = Todo(todoid = todoData[j].get('id'),todotitle = todoData[j].get('title'),todoetat = todoData[j].get('completed'), userid = todoData[j].get('userId') )

                commitInsert(todoFromApi)
                # try:
                #     db.session.add(todoFromApi)
                # except:
                #     db.session.rollback()
                #     return "erreur"

            try:
                db.session.add(personalDataFromApi)
                db.session.add(addresFromApi)
                db.session.add(companyFromApi)
                db.session.commit()
            except:
                db.session.rollback()
                return  "erreur"
    else:
        userOfId = Users.query.all()
        listOfId = {0}
        for i in range(len(userOfId)):
            listOfId.add(userOfId[i].userid)

        nextStepApi = len(Users.query.all())
        if nbelt >  nextStepApi:
            if nextStepApi+nbelt < len(data):
                endIndex = nextStepApi + nbelt
            else:
                endIndex = len(data)
            # userDataFromApi = get('https://jsonplaceholder.typicode.com/'+endpoint)
            # data = userDataFromApi.json()
            for i in range(nextStepApi,endIndex):
                if data[i].get('id') not in listOfId:

                    personalDataFromApi = Users(userid = data[i].get('id'), name = data[i].get('name') , username = data[i].get('username'),phone=data[i].get('phone'),email=data[i].get('email'),website=data[i].get('website'), password=12)

                    addresFromApi = Address(addressid = data[i].get('id'), street = data[i]['address']['street'], suite = data[i]['address']['suite'], city = data[i]['address']['city'], zipcode = data[i]['address']['zipcode'], geo_lat = data[i]['address']['geo']['lat'], geo_lng = data[i]['address']['geo']['lat'], userid = data[i].get('id'))

                    companyFromApi = Company(companyid = data[i].get('id'), companyname = data[i]['company']['name'], companycatchphrase = data[i]['company']['catchPhrase'], companybs = data[i]['company']['bs'], userid = data[i].get('id'))
# --------------------------------------------------------------
                    userPostFromApi = get(URL+endpoint+'/'+str(i+1)+'/posts')
                    postData = userPostFromApi.json()
                    userAlbumFromApi = get(URL+endpoint+'/'+str(i+1)+'/albums')
                    albumData = userAlbumFromApi.json()
                    userTodoFromApi = get(URL+endpoint+'/'+str(i+1)+'/todos')
                    todoData = userTodoFromApi.json()

                    for j in range(len(postData)):
                        postFromApi = Posts(postid = postData[j].get('id'), posttitle = postData[j].get('title'), postbody = postData[j].get('body'), userid = postData[j].get('userId'))

                        # postCommentFromApi = get(URL+'posts/'+str(j+1)+'/comments')
                        # commentData = postCommentFromApi.json()
                        # for k in range(len(commentData)):
                        #     commentFromApi = Comment(commentid = commentData[k].get('id'),commentname = commentData[k].get('name'),commentemail = commentData[k].get('email'),commentbody = commentData[k].get('body'), postid = commentData[k].get('postId'))

                        #     commitInsert(commentFromApi)

                        commitInsert(postFromApi) 

                        # try:
                        #     db.session.add(postFromApi)
                        # except:
                        #     db.session.rollback()
                        #     return "erreur"
                    for j in range(len(albumData)):
                        albumFromApi = Albums(albumid = albumData[j].get('id'), albumtitle = albumData[j].get('title'), userid = albumData[j].get('userId'))

                        commitInsert(albumFromApi)
                        # try:
                        #     db.session.add(albumFromApi)
                        # except:
                        #     db.session.rollback()
                        #     return "erreur"

                    for j in range(len(todoData)):
                        todoFromApi  = Todo(todoid = todoData[j].get('id'),todotitle = todoData[j].get('title'),todoetat = todoData[j].get('completed'), userid = todoData[j].get('userId') )

                        commitInsert(todoFromApi)
                        # try:
                        #     db.session.add(todoFromApi)
                        # except:
                        #     db.session.rollback()
                        #     return "erreur"
# ----------------------------------------------------------------------------------------------
                try:
                    db.session.add(personalDataFromApi)
                    db.session.add(addresFromApi)
                    db.session.add(companyFromApi)
                    db.session.commit()
                except:
                    db.session.rollback()                    
                    return  "erreur"
    # db.session.commit()
# ---------------------END API PROCESS------------------------

@app.route('/pageUser')
def pageUser():
    if 'userid' in session:
        user = Users.query.filter_by(userid= session['userid']).first()

        return render_template('pageUser.html' , users=user)
# ----------------------------------------------------
@app.route('/userPost')
def userPost():
    if 'userid' in session:
        return render_template('userPost.html')
    else:
        flash("Chargez votre user et connectez vous")

        return redirect('/pagePrincipal')

# ---------------------------------------------------


@app.route('/album/')
def album():
    if 'userid' in session:
        return render_template('album.html')
    else:
        flash("Chargez votre user et connectez vous")

        return redirect('/pagePrincipal')

@app.route('/photo')
def photo():
    if 'userid' in session:
        return render_template('photo.html')
    else:
        flash("Chargez votre user et connectez vous")

        return redirect('/pagePrincipal')
@app.route('/todo')

def todo():
    if 'userid' in session:
        return render_template('todo.html')
    else:
        flash("Chargez votre user et connectez vous")

        return redirect('/pagePrincipal')
@app.route('/profil')
def profil():
    if 'userid' in session:
        user = Users.query.filter_by(userid= session['userid']).first()
        address = Address.query.filter_by(userid= session['userid']).first()
        company = Company.query.filter_by(userid= session['userid']).first()
        coordonne =(address.geo_lat , address.geo_lng)
        map= folium.Map(location=coordonne,zoom_start=2)
        folium.Marker(location=coordonne,popup=f"user:{user.name}",tooltip="appuiyez ici").add_to(map)
        map.save('templates/map.html')
        return render_template('profil.html',user=user,address=address, company=company)
    else:
        flash("Chargez votre user et connectez vous")

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
        # donne_personnel= Users(name = name , username = username,phone=phone,email=email,website=website, password=12)
        userid = Users.query.all()
        listId = {0}
        for i in range(len(userid)):
            listId.add(userid[i].userid)
        maxid = max(listId)+1
        if len(userid) <= 10 and 11 not in listId:
            iduser = 11

            donne_personnel= Users(userid = iduser, name = name , username = username,phone=phone,email=email,website=website, password=12)

            addres = Address(addressid = iduser, street = street, suite = suite, city = city, zipcode = zipcode, geo_lat = latitude, geo_lng = longitude, userid = iduser)

            company = Company(companyid = iduser, companyname = companyname, companycatchphrase = catchPhrase, companybs = bs, userid = iduser)

        else:
            donne_personnel= Users(userid = maxid, name = name , username = username,phone=phone,email=email,website=website, password=12)
            
            addres = Address(addressid = maxid, street = street, suite = suite, city = city, zipcode = zipcode, geo_lat = latitude, geo_lng = longitude, userid = maxid)
        
            company = Company(companyid = maxid, companyname = companyname, companycatchphrase = catchPhrase, companybs = bs, userid = maxid)
        
        try:
            db.session.add(donne_personnel)
            db.session.add(addres)
            db.session.add(company)
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
