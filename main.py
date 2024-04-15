from functools import wraps
import os
from flask import Flask, redirect, render_template, request,session, url_for, flash
import useraccount, candidate, vote


app = Flask(__name__)
app.secret_key = 'd6766119bd84887af1a0d5e1f544487cc6ad1772ab309aafbd630edd66811e96'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    name = ''
    email = ''
    council = False
    loggedIn = False
    admin = True
    runningForPresident = False
    if('name' in session):
        name = session['name']
    if('email' in session):
        email = session['email']
        loggedIn = True
    print('Printing Session',session)
    if('councilMemberCode' in session):
        council = True
        candidateInfo = candidate.getCandidateInfo({'email':session['email']})
        print('Candidate info printing',candidateInfo)
        if(candidateInfo == None or 'error' in candidateInfo):
            runningForPresident = False
        else:
            runningForPresident = True
    else:
        council=False
        runningForPresident=False

    data = {'name':name,'email':email}
    voted = False
    if('voted' in session):
      voted = True
    return render_template('index.html', loggedIn = loggedIn, data = data, voted=voted, council = council, runningForPresident = runningForPresident, admin = admin)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    cleanUp()
    if (request.method == 'POST'):
        retData = useraccount.signup(request.form)
        if('error' in retData):
            return render_template('signup.html',message=retData['error'])
        if('message' in retData):
            return render_template('login.html',message=retData['message']+' Login now to continue!!')
        else:
            return render_template('signup.html',message='Some Other error')        
    else:
       return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    cleanUp()
    if (request.method == 'POST'):
        retData = useraccount.login(request.form)
        if('error' in retData):
            return render_template('login.html',message=retData['error'])
        if('message' in retData):
            session['name'] = retData['name']
            session['email'] = request.form['email']
            if('councilMemberCode' in retData):
                session['councilMemberCode'] = retData['councilMemberCode']
            return redirect(url_for('index'))
        else:
            return render_template('login.html',message='Some Other error')
    else:
       return render_template('login.html')    

@app.route('/voting', methods=['GET', 'POST'])
@login_required
def voting():
    voted = True
    if (request.method == 'POST'):
        retData = vote.vote(request.form)
        if('error' in retData):
            flash(retData['error'])
            return redirect(url_for('index'))
        if('message' in retData):
            flash('Thank you for your vote')
            session['voted'] = 'yes'
            return redirect(url_for('index'))        
        else:
            return render_template('election.html',message='Some Other error')        
    else:
      candidates = candidate.getCandidates()
      if('voted' in session):
          voted = True
      else:
          voted=False
      return render_template('voting.html',candidates = candidates, voterEmail = session['email'], voted = voted, loggedIn = True)

@app.route('/statistics')
@login_required
def statistics():
    candidates = candidate.getCandidates()
    votes = []
    names = []
    for x in candidates:
      names.append(x['name'])
      votes.append(x['votes'])
    
    return render_template('statistics.html', votes=votes, names=names, loggedIn = True)

@app.route('/election', methods=['GET', 'POST'])
@login_required
def election():
    if (request.method == 'POST'):
        retData = candidate.runForElection(request.form)
        if('error' in retData):
            flash(retData['error'])
            return redirect(url_for('index'))
        if('message' in retData):
            flash(retData['message'])
            return redirect(url_for('index'))        
        else:
            return render_template('election.html',message='Some Other error')        
    else:
       if('councilMemberCode' not in session):
           return redirect(url_for('index'))
       candidateInfo = candidate.getCandidateInfo({'email':session['email']})
       if(candidateInfo == None or 'error' in candidateInfo or 'councilMemberCode' not in session):
            runningForPresident = False
       else:
            runningForPresident = True
       return render_template('election.html',loggedIn = True, name=session['name'], email=session['email'], runningForPresident=runningForPresident)

@app.route('/results')
def results():
    logedIn = False
    if('email' in session):
        loggedIn = True
    # id has to be unique, and the votes have to be ints, rest of it does not really matter
    results = [{'year':2000,'id':'result2000','votes':[3,2],'names':['max','bob']},
               {'year':2001,'id':'result2001','votes':[5,7],'names':['bob','max']},
               {'year':2017,'id':'result2017','votes':[10,7,3],'names':['chris','john','jake']}]
    return render_template('results.html',results=results, loggedIn = loggedIn)

@app.route('/logout')
@login_required
def logout():
    cleanUp()
    return render_template('login.html',message='Successfully Logged out!!')

def setEnvVars():
  if('GAE_ENV' not in os.environ):
    os.environ['DATASTORE_DATASET'] = 'voting-system'
    os.environ['DATASTORE_DATASET'] = 'voting-system'
    os.environ['DATASTORE_EMULATOR_HOST'] = 'localhost:8081'
    os.environ['DATASTORE_EMULATOR_HOST_PATH'] = 'localhost:8081/datastore'
    os.environ['DATASTORE_HOST'] = 'http://localhost:8081'
    print('Running on local')
  else:
      print('Running in GAE')

def cleanUp():
    session.pop('name',None)
    session.pop('email',None)
    session.pop('councilMemberCode',None)
    session.pop('voted',None)

def isLoggedIn():
    if('email' in session):
        return True
    return False

if __name__ == '__main__':
    setEnvVars()
    app.run(debug=True)
