from creationbd import *
from requests import get

def gestionIdForManullayInsertion(tableName, colName, enpoint):
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