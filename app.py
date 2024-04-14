import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    loggedIn = True
    data = {'name':'John','email':'John@gmail.com'}
    council = False
    return render_template('index.html', loggedIn = loggedIn, data = data, council = council)
@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/voting')
def voting():
    voted = True
    dummyCandidates = [{'name':'John','position':'President','slogan':'YOUR voice. YOUR choice. Vote John today.'},
                       {'name':'Max','position':'President','slogan':'Students Need Their Own Voice. So Make The Right Choice.'}]
    return render_template('voting.html',candidates = dummyCandidates, voted = voted)
@app.route('/statistics')
def statistics():
    votes = [3,4,2,3,1]
    names = ["john", "bob", "max", "alex", "chris"]
    return render_template('statistics.html', votes=votes, names=names)
@app.route('/election')
def election():
    return render_template('election.html')
if __name__ == '__main__':
    app.run(debug=True)
