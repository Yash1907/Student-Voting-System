import datastore

def vote(candidateInfo):
    if ('email' not in candidateInfo or candidateInfo['email'] == '' or
        'voterEmail' not in candidateInfo or candidateInfo['voterEmail'] == '' ):
     return {'error':"Candidate Email, Voter Email are required!!"}
    
    dbUserAcct = datastore.get('UserAccount',candidateInfo['voterEmail'])
    
    if(dbUserAcct == None):
      return {'error':'Invalid Voter ' + candidateInfo['voterEmail'] + ' !!'}
    
    if('voted' in dbUserAcct and dbUserAcct['voted'] == 'yes'):
      return {'error':'You have voted already !!'}
    else:
      dbUserAcct['voted'] = 'yes'
      retData = datastore.save('UserAccount',dbUserAcct['email'],dbUserAcct)
    
    dbCandidateInfo = datastore.get('CandidateInfo',candidateInfo['email'])

    if(dbCandidateInfo == None):
      return {'error':'Invalid Candidate ' + candidateInfo['email'] + ' !!'}    

    if('votes' not in dbCandidateInfo):
      dbCandidateInfo['votes'] = 1
    else:
      dbCandidateInfo['votes'] = dbCandidateInfo['votes'] + 1

    retData = datastore.save('CandidateInfo',candidateInfo['email'],dbCandidateInfo)
    return retData

