from crypt import methods
import email
from pickletools import OpcodeInfo
import re
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
from requests import get



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

        
    page = request.args.get('page',1, type=int)
    users_paginate = Users.query.paginate(page=page, per_page = 5)
    if nb <= 5:
        users = Users.query.all()
        nbuser =len(users)

    return render_template('pagePrincipal.html',users=users,nbuser=nbuser, nb=nb,users_paginate=users_paginate,formulair=formulair)



# -------------------BEGIN API PROCESS--------------------

def addRows(dataForTable):
    try:
        db.session.add(dataForTable)
        # commit()
    except:
        db.session.rollback()
        return "erreur"
def commit():
    return db.session.commit()

URL = 'https://jsonplaceholder.typicode.com/'
def getAndInsertDataFromApi(endpoint, nbelt):
    isEmpty = Users.query.all()
    userDataFromApi = get(URL+endpoint)
    data = userDataFromApi.json()
    # if len(isEmpty) == 0:
    if len(isEmpty) == 0:
        
        if nbelt > len(data):
            stepApi = len(data)
        else:
            stepApi = nbelt
        for i in range(stepApi):

            personalDataFromApi = Users(userid = data[i].get('id'), 
            name = data[i].get('name') , 
            username = data[i].get('username'),
            phone=data[i].get('phone'),
            email=data[i].get('email'),
            website=data[i].get('website'), 
            password=12)
            addRows(personalDataFromApi)
            
            addresFromApi = Address(addressid = data[i].get('id'), 
            street = data[i]['address']['street'], 
            suite = data[i]['address']['suite'], 
            city = data[i]['address']['city'], 
            zipcode = data[i]['address']['zipcode'], 
            geo_lat = data[i]['address']['geo']['lat'], 
            geo_lng = data[i]['address']['geo']['lat'], 
            userid = data[i].get('id'))
            addRows(addresFromApi)


            companyFromApi = Company(companyid = data[i].get('id'), 
            companyname = data[i]['company']['name'], 
            companycatchphrase = data[i]['company']['catchPhrase'], 
            companybs = data[i]['company']['bs'], 
            userid = data[i].get('id'))
            addRows(companyFromApi)

            userPostFromApi = get(URL+endpoint+'/'+str(data[i].get('id'))+'/posts')
            postData = userPostFromApi.json()
            userAlbumFromApi = get(URL+endpoint+'/'+str(data[i].get('id'))+'/albums')
            albumData = userAlbumFromApi.json()
            userTodoFromApi = get(URL+endpoint+'/'+str(data[i].get('id'))+'/todos')
            todoData = userTodoFromApi.json()

            for j in range(len(postData)):
                postFromApi = Posts(postid = postData[j].get('id'), 
                posttitle = postData[j].get('title'), 
                postbody = postData[j].get('body'), 
                userid = postData[j].get('userId'))
                addRows(postFromApi)
                
                postCommentFromApi = get(URL+'posts/'+str(postData[j].get('id'))+'/comments')
                commentData = postCommentFromApi.json()
                for k in range(len(commentData)):
                    commentFromApi = Comment(commentid = commentData[k].get('id'),
                    commentname = commentData[k].get('name'),
                    commentemail = commentData[k].get('email'),
                    commentbody = commentData[k].get('body'),
                    postid = commentData[k].get('postId'))
                    addRows(commentFromApi)
                
            for j in range(len(albumData)):
                albumFromApi = Albums(albumid = albumData[j].get('id'), 
                albumtitle = albumData[j].get('title'), 
                userid = albumData[j].get('userId'))
                addRows(albumFromApi)

                photoAlbulmFromApi = get(URL+'albums/'+str(albumData[j].get('id'))+'/photos')
                photoData = photoAlbulmFromApi.json()
                for l in range(len(photoData)):
                    photoFromApi  = Photos( photoid = photoData[l].get('id'), 
                    phototitle = photoData[l].get('title'), 
                    photourl = photoData[l].get('url'), 
                    photothumbnailurl = photoData[l].get('thumbnailUrl'), 
                    albumid = photoData[l].get('albumId'))
                    addRows(photoFromApi)

            for j in range(len(todoData)):
                todoFromApi  = Todo(todoid = todoData[j].get('id'),
                todotitle = todoData[j].get('title'),
                todoetat = todoData[j].get('completed'), 
                userid = todoData[j].get('userId') )

                addRows(todoFromApi)
        commit()
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
    
            for i in range(nextStepApi,endIndex):
                if data[i].get('id') not in listOfId:

                    personalDataFromApi = Users(userid = data[i].get('id'), 
                    name = data[i].get('name') , 
                    username = data[i].get('username'),
                    phone=data[i].get('phone'),
                    email=data[i].get('email'),
                    website=data[i].get('website'), 
                    password=12)
                    addRows(personalDataFromApi)

                    addresFromApi = Address(addressid = data[i].get('id'), 
                    street = data[i]['address']['street'], 
                    suite = data[i]['address']['suite'], 
                    city = data[i]['address']['city'], 
                    zipcode = data[i]['address']['zipcode'], 
                    geo_lat = data[i]['address']['geo']['lat'], 
                    geo_lng = data[i]['address']['geo']['lat'], 
                    userid = data[i].get('id'))
                    addRows(addresFromApi)

                    companyFromApi = Company(companyid = data[i].get('id'), 
                    companyname = data[i]['company']['name'], 
                    companycatchphrase = data[i]['company']['catchPhrase'], 
                    companybs = data[i]['company']['bs'], 
                    userid = data[i].get('id'))
                    addRows(companyFromApi)

                    userPostFromApi = get(URL+endpoint+'/'+str(data[i].get('id'))+'/posts')
                    postData = userPostFromApi.json()
                    userAlbumFromApi = get(URL+endpoint+'/'+str(data[i].get('id'))+'/albums')
                    albumData = userAlbumFromApi.json()
                    userTodoFromApi = get(URL+endpoint+'/'+str(data[i].get('id'))+'/todos')
                    todoData = userTodoFromApi.json()
                    for j in range(len(postData)):
                        postFromApi = Posts(postid = postData[j].get('id'), 
                        posttitle = postData[j].get('title'), 
                        postbody = postData[j].get('body'), 
                        userid = postData[j].get('userId'))
                        addRows(postFromApi)

                        postCommentFromApi = get(URL+'posts/'+str(postData[j].get('id'))+'/comments')
                        commentData = postCommentFromApi.json()
                        for k in range(len(commentData)):
                            commentFromApi = Comment(commentid = commentData[k].get('id'),
                            commentname = commentData[k].get('name'),
                            commentemail = commentData[k].get('email'),
                            commentbody = commentData[k].get('body'),
                            postid = commentData[k].get('postId'))
                            addRows(commentFromApi)

                    for j in range(len(albumData)):
                        albumFromApi = Albums(albumid = albumData[j].get('id'), 
                        albumtitle = albumData[j].get('title'), 
                        userid = albumData[j].get('userId'))
                        addRows(albumFromApi)

                        photoAlbulmFromApi = get(URL+'albums/'+str(albumData[j].get('id'))+'/photos')
                        photoData = photoAlbulmFromApi.json()
                        for l in range(len(photoData)):
                            photoFromApi  = Photos( photoid = photoData[l].get('id'), 
                            phototitle = photoData[l].get('title'), 
                            photourl = photoData[l].get('url'), 
                            photothumbnailurl = photoData[l].get('thumbnailUrl'), 
                            albumid = photoData[l].get('albumId'))
                            addRows(photoFromApi)

                    for j in range(len(todoData)):
                        todoFromApi  = Todo(todoid = todoData[j].get('id'),
                        todotitle = todoData[j].get('title'),
                        todoetat = todoData[j].get('completed'), 
                        userid = todoData[j].get('userId') )
                        addRows(todoFromApi)
                        
        commit()
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
        donnee_Albums = Albums(albumid = getionIdForManullayInsertion(Albums, Albums.albumid, 'albums')+1, albumtitle = title,userid= session['userid'])
        addRows(donnee_Albums)
    commit()
    return redirect('/album/')

def getionIdForManullayInsertion(tableName, colName, enpoint):
    listOfIdTable = set()
    queryTable = tableName.query.with_entities(colName).all()
    if len(queryTable) != 0:
        for id in range(len(queryTable)):
            listOfIdTable.add(queryTable[id][0])
        maxId = max(listOfIdTable)
    else:
        getTable = get(URL+enpoint)
        tableList = getTable.json()
        maxId = len(tableList)
    return maxId

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
        donnee_Photo = Photos(photoid = getionIdForManullayInsertion(Photos,Photos.photoid,'photos')+1, phototitle = title, photourl = url, photothumbnailurl = thumb)
        addRows(donnee_Photo)
    # commit()
    return redirect('/photo')
@app.route('/photo/',methods=["GET","POST"])
def photo():
    
    if 'userid' in session:
        id = request.form["id"] 
        albums = Albums.query.filter_by(userid= session['userid'])

        page = request.args.get('page', 1, type=int)
        photos = Photos.query.filter_by(albumid=id).paginate(page=page, per_page=8)
        # photos = Photos.query.filter_by(albumid=id)
        return render_template('photo.html',photos=photos)
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
        if etat == 'In Progress':
            etat = 'false'
        else:
            etat = 'true'
        donnee_todo = Todo(todoid = getionIdForManullayInsertion(Todo, Todo.todoid, 'todos')+1, todotitle = title,userid= session['userid'],todoetat=etat)
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

            donne_personnel= Users(userid = iduser, 
            name = name , 
            username = username,
            phone=phone,
            email=email,
            website=website, 
            password=12)

            addres = Address(addressid = iduser, 
            street = street, 
            suite = suite, 
            city = city, 
            zipcode = zipcode, 
            geo_lat = latitude, 
            geo_lng = longitude, 
            userid = iduser)

            company = Company(companyid = iduser, 
            companyname = companyname, 
            companycatchphrase = catchPhrase, 
            companybs = bs, 
            userid = iduser)

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
    postid = getionIdForManullayInsertion(Posts, Posts.postid,'posts')
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
        comments = Comment.query.filter_by(postid=id)

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

# --------------------------END--------------------------

db.init_app(app)
app.run(debug=True)
