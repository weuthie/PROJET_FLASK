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
from flask_sqlalchemy import SQLAlchemy,Pagination
import folium
from creationbd import *
import requests 
from helpers import *



app = Flask(__name__)
app.config['SECRET_KEY'] = 'groupe4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupe4:test123@localhost/projetflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = false
# db = SQLAlchemy(app)

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
        
    
    # pagination

        
    # page = request.args.get('page',1, type=int)
    # users_paginate = Users.query.paginate(page=page, per_page = 5)
    # if nb <= 5:
    users = Users.query.all()
    nbuser =len(users)

    return render_template('pagePrincipal.html',users=users,nbuser=nbuser, nb=nb,formulair=formulair)


        # pagination
    # page = request.args.get('page',1, type=int)
    # users = Users.query.paginate(page=page, per_page = 5)
    # users = Users.query.filter_by(archive=1).all()
    # nbuser =len(users)
    # return render_template('pagePrincipal.html',users = users,nb=nb, nbuser=nbuser, formulair=formulair)

    
@app.route('/archiver/<int:userid>', methods=["POST","GET"])
def archiver(userid):
    user =  Users.query.get_or_404(userid)
    if request.method == "POST":
        user.archive = 0
        commit()
    # print(user)
    return redirect('/pagePrincipal')

@app.route('/pageUser')
def pageUser():
    if 'userid' in session:
        user = Users.query.filter_by(userid= session['userid']).first()

        return render_template('pageUser.html' , users=user)
# ----------------------------------------------------
@app.route('/userPost')
def userPost():
    if 'userid' in session:
        page = request.args.get('page', 1, type=int)
        posts = Posts.query.filter_by(userid=session['userid']).paginate(page=page, per_page=3)
        # posts = Posts.query.filter_by(userid= session['userid'])
        return render_template('userPost.html', posts=posts)
    else:
        flash("Chargez votre user et connectez vous")

        return redirect('/pagePrincipal')

@app.route('/addAlbum', methods=["POST","GET"])
def addAlbum():
    if request.method == 'POST':
        title = request.form['title']
        donnee_Albums = Albums(albumid = gestionIdForManullayInsertion(Albums, Albums.albumid, 'albums')+1, albumtitle = title,userid= session['userid'])
        addRows(donnee_Albums)
    commit()
    return redirect('/album/')


@app.route('/album/', methods=["GET","POST"])
def album():     
    if 'userid' in session:
        page = request.args.get('page', 1, type=int)
        albums = Albums.query.filter_by(userid=session['userid']).paginate(page=page, per_page=10)
        # albums = Albums.query.filter_by(userid= session['userid'])
        return render_template('album.html',albums=albums)
    else:
        flash("Chargez votre user et connectez vous")

        return redirect('/pagePrincipal')

@app.route('/addPhoto', methods=["POST","GET"])
def addPhotos():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        thumb = request.form['thumbnailUrl']
        donnee_Photo = Photos(photoid = gestionIdForManullayInsertion(Photos,Photos.photoid,'photos')+1, phototitle = title, photourl = url, photothumbnailurl = thumb)
        addRows(donnee_Photo)
    # commit()
    return redirect('/photo')
@app.route('/photo/',methods=["GET","POST"])
def photo():
    id = request.form["id"] 
    
    if 'userid' in session:
        albums = Albums.query.filter_by(userid= session['userid'])

        page = request.args.get('page', 1, type=int)
        photos = Photos.query.filter_by(albumid=id).paginate(page=page, per_page=8)
        # photos = Photos.query.filter_by(albumid=id)
        return render_template('photo.html',photos=photos,page=page,id=id)
    else:
        flash("Chargez votre user et connectez vous")

        return redirect('/pagePrincipal')


@app.route('/deleteTodo/<int:id>')
def deleteTodo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/todo')

@app.route('/addTodo', methods=["POST","GET"])
def addTodo():
    if request.method == 'POST':
        title = request.form['title']
        etat = request.form['etat']
        if etat == "In Progress":
            etat = 'false'
        else:
            etat = 'true'
        donnee_todo = Todo(todoid = gestionIdForManullayInsertion(Todo, Todo.todoid, 'todos')+1, todotitle = title,userid= session['userid'],todoetat=etat)
        addRows(donnee_todo)
    commit()
    return redirect('/todo')

@app.route('/todo')
def todo():
    if 'userid' in session:
        # todos = Todo.query.filter_by(userid= session['userid'])

        page = request.args.get('page', 1, type=int)
        todos = Todo.query.filter_by(userid= session['userid']).paginate(page=page, per_page=6)
        return render_template('todo.html', todos=todos)

    else:
        flash("Chargez votre user et connectez vous")

        return redirect('/pagePrincipal')

@app.route('/map')
def map():
    if 'userid' in session:
        return render_template('map.html')
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

@app.route('/logout')
def logout():
    session.clear()
    return redirect('pagePrincipal')

        
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

            donne_personnel= Users(userid = iduser, name = name, username = username, phone=phone,email=email,website=website, password=12)

            addres = Address(addressid = iduser, street = street, suite = suite, city = city, zipcode = zipcode, geo_lat = latitude, geo_lng = longitude, userid = iduser)

            company = Company(companyid = iduser, 
            companyname = companyname, companycatchphrase = catchPhrase, companybs = bs, userid = iduser)

        else:
            donne_personnel= Users(userid = maxid, name = name , username = username,phone=phone,email=email,website=website, password=12)
            
            addres = Address(addressid = maxid, street = street, suite = suite, city = city, zipcode = zipcode, geo_lat = latitude, geo_lng = longitude, userid = maxid)
        
            company = Company(companyid = maxid, companyname = companyname, companycatchphrase = catchPhrase, companybs = bs, userid = maxid)
        
        try:
            db.session.add(donne_personnel)
            db.session.add(addres)
            db.session.add(company)
            commit()
            return  redirect('/pagePrincipal') 
        except:
            db.session.rollback()
            return  "erreur"
    else:
        return render_template('formulairedajout.html')
# --------------------ADD BY DEME-----------------------

@app.route('/addPost', methods=['POST'])
def addPost():
    postid = gestionIdForManullayInsertion(Posts, Posts.postid,'posts')
    if 'userid' in session:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            donnee_posts = Posts(postid = postid+1, posttitle = title, postbody = content, userid = session['userid'])
            addRows(donnee_posts)
        commit()
    return redirect('/userPost')

@app.route('/pageComment',methods=["POST","GET"])
def pageComment():
    id = request.form["id"] 

    if 'userid' in session:
        posts = Posts.query.filter_by(userid= session['userid'])
        # comments = Comment.query.filter_by(postid=id)
        page = request.args.get('page', 1, type=int)
        comments = Comment.query.filter_by(postid=id).paginate(page=page, per_page=3)

        return render_template('pageComment.html',comments=comments,posts=posts,id=id)
    else:
        flash("Chargez votre user et connectez vous")

        return redirect('/pagePrincipal')


  
@app.route('/editPost/<int:id>',methods=["POST","GET"])
def editPost(id):
    post = Posts.query.get_or_404(id)
    # print("title   ",posts.posttitle)

    if request.method == "POST":
        post.posttitle = request.form["title"]
        post.postbody = request.form["content"]
        db.session.commit()
        # print('Nouveau title :',Posts.query.get(id).posttitle)
        return redirect("/userPost")
        
    else:
        return render_template('editpost.html', post=post)  


@app.route('/deletePost/<int:id>')
def deletePost(id):
    post = Posts.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/userPost')

@app.route('/editTodo/<int:id>',methods=["POST","GET"])
def editTodo(id):
    todo = Todo.query.get_or_404(id)
    if request.method == "POST":
        todo.todotitle = request.form["title"]
        todo.todoetat = request.form["etat"]
        db.session.commit()
        return redirect("/todo") 
    else:
        return render_template('editTodo.html', todo=todo)


@app.route('/dashbord')
def dashbord():
    posts= Posts.query.all()
    users=Users.query.all()
    list_user=[]
    list_post=[]
    for user in users:
        v=(user.username,len(user.posts))
        list_user.append(v)
    for post in posts:
        c=(post.postid,len(post.comments))
        list_post.append(c)
    
    d_false= db.session.query(db.func.count(Todo.todoetat)).filter_by(todoetat = 'false').first()
    d_true= db.session.query(db.func.count(Todo.todoetat)).filter_by(todoetat = 'true').first()
    # d_= db.session.query(db.func.count(Todo.todoetat)).first()
    


    

    return redirect('/')

# --------------------------END--------------------------

db.init_app(app)
app.run(debug=True)
