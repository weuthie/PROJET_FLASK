from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/pagePrincipal')
def pagePrincipal():
    return render_template('pagePrincipal.html')