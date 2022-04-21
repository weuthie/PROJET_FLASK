from flask import Flask, render_template, url_for ,request

app = Flask(__name__)

# @app.route('/')
@app.route('/pagePrincipal')
def pagePrincipal():
    return render_template('pagePrincipal.html')

# @app.route('/adduser', methods=['get','POST'])
# def adduser():
#     name = request.form['name']
#     username = request.form['username']

