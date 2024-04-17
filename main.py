from functools import wraps
import os
from flask import Flask, redirect, render_template, request,session, url_for, flash
import useraccount, candidate, vote, result, election


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
    admin = False
    runningForPresident = False
    electionActive = False
    voted = False
    electionActive = election.isCurrentActiveElection()
    
    if('name' in session):
        name = session['name']
    if('voted' in session):
      voted = True
    if('email' in session):
        email = session['email']
        loggedIn = True
        if(session['email'] == 'admin@voting.com'):
            admin = True
        hasVoted = useraccount.hasVoted({'email':session['email']})
        
        if('voted' in hasVoted and hasVoted['voted'] == 'yes'):
            session['voted'] = 'yes'
            voted = True
        else:
            session['voted'] = 'no'
            voted = False            
            
    if('councilMemberCode' in session):
        council = True
        candidateInfo = candidate.getCandidateInfo({'email':session['email']})
        if(candidateInfo == None or 'error' in candidateInfo):
            runningForPresident = False
        else:
            runningForPresident = True

    data = {'name':name,'email':email}
    return render_template('index.html', loggedIn = loggedIn, data = data, voted=voted, council = council, 
                           runningForPresident = runningForPresident, admin = admin, electionActive=electionActive)

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
            session['voted'] = retData['voted']
            if('councilMemberCode' in retData):
                session['councilMemberCode'] = retData['councilMemberCode']
            return redirect(url_for('index'))
        else:
            return render_template('login.html',message='Some Other error')
    else:
       return render_template('login.html')    

@app.route('/castVote', methods=['GET', 'POST'])
@login_required
def castVote():
    if(not election.isCurrentActiveElection()):
        flash('No Active Election to Vote!!')
        return redirect(url_for('index'))    
    voted = False
    if (request.method == 'POST'):
        retData = vote.vote(request.form)
        flashMessage = 'Some Error Occured!!'
        if('error' in retData):
            flashMessage = retData['error']
        elif('message' in retData):
            flashMessage = retData['message']
            session['voted'] = 'yes'
        flash(flashMessage)
        return redirect(url_for('index'))
    else:
      candidates = candidate.getCandidates()
      if('voted' in session and session['voted'] == 'yes'):
          voted = True

      return render_template('voting.html',candidates = candidates, voterEmail = session['email'], voted = voted, loggedIn = True)

@app.route('/statistics')
@login_required
def statistics():
    if(not election.isCurrentActiveElection()):
        flash('No Active Election to show stats!!')
        return redirect(url_for('index'))
    
    candidates = candidate.getCandidates()
    votes = []
    names = []
    for x in candidates:
      names.append(x['name'])
      voteCount = 0
      if('votes' in x):
          voteCount = x['votes']
      votes.append(voteCount)
    
    return render_template('statistics.html', votes=votes, names=names, loggedIn = True)

@app.route('/runForElection', methods=['GET', 'POST'])
@login_required
def runForElection():
    if(not election.isCurrentActiveElection()):
        flash('No Active Election to run!!')
        return redirect(url_for('index'))
    if('councilMemberCode' not in session):
        flash('Must be a council member to run!!')
        return redirect(url_for('index'))        
    if (request.method == 'POST'):
        retData = candidate.runForElection(request.form)
        flashMessage = 'Some Error Occured!!'
        if('error' in retData):
            flashMessage = retData['error']
        elif('message' in retData):
            flashMessage = retData['message']
        flash(flashMessage)
        return redirect(url_for('index'))        
    else:
       if('councilMemberCode' not in session):
           return redirect(url_for('index'))
       candidateInfo = candidate.getCandidateInfo({'email':session['email']})
       if(candidateInfo == None or 'error' in candidateInfo or 'councilMemberCode' not in session):
            runningForPresident = False
       else:
            runningForPresident = True
       return render_template('runForElection.html',loggedIn = True, name=session['name'], email=session['email'], runningForPresident=runningForPresident)

@app.route('/results', methods=['GET'])
@login_required
def results():
    loggedIn = False
    if('email' in session):
        loggedIn = True
    # id has to be unique, and the votes have to be ints, rest of it does not really matter
    resultsDummy = [{'year':2000,'id':'result2000','votes':[3,2],'names':['max','bob']},
               {'year':2001,'id':'result2001','votes':[5,7],'names':['bob','max']},
               {'year':2017,'id':'result2017','votes':[10,7,3],'names':['chris','john','jake']}]
    results = result.getAllResults()
    resultsOut = []
    prevElection = ''
    resultOutObj = {}
    for resultObj in results:
        if(prevElection == '' or prevElection != resultObj['electionName']+resultObj['electionYear']):
            if(prevElection != ''):
                resultsOut.append(resultOutObj)
                resultOutObj = {}            
            resultOutObj['name'] = resultObj['electionName']
            resultOutObj['year'] = resultObj['electionYear']
            resultOutObj['votes'] = []
            resultOutObj['names'] = []
            prevElection = resultObj['electionName']+resultObj['electionYear']
            resultOutObj['id'] = prevElection
        resultOutObj['names'].append(resultObj['name'])
        resultOutObj['votes'].append(resultObj['votes'])        
    resultsOut.append(resultOutObj)
    if(len(results) == 0):
        resultsOut = resultsDummy
    return render_template('results.html',results=resultsOut, loggedIn = loggedIn)

@app.route('/newElection', methods=['GET','POST'])
@login_required
def newElection():
    flashMessage = 'Some Error Occured!!'
    if(session['email'] != 'admin@voting.com'):
        flash('You are not authorized to perform this function')
        return redirect(url_for('index'))

    retData = election.startNewElection(request.form)
    if('error' in retData):
        flashMessage = retData['error']
    elif('message' in retData):
        flashMessage = retData['message']
    flash(flashMessage)
    return redirect(url_for('index'))

@app.route('/endElection')
@login_required
def endElection():
    if(session['email'] != 'admin@voting.com'):
        flash('You are not authorized to perform this function')
        return redirect(url_for('index'))
    retData = election.endCurrentElection()
    flashMessage = 'Some Error Occured!!'
    if('error' in retData):
        flashMessage = retData['error']
    elif('message' in retData):
        flashMessage = retData['message']
    flash(flashMessage)
    return redirect(url_for('index'))

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
