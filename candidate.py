import datastore

def runForElection(candidateInfo):
    if ('email' not in candidateInfo or 'name' not in candidateInfo or 
        'position' not in candidateInfo or 'slogan' not in candidateInfo or 
        candidateInfo['email'] == '' or candidateInfo['name'] =='' or
        candidateInfo['position'] == '' or candidateInfo['slogan'] ==''):
     return {'error':"Email, Name, Position and Slogan are required!!"}
    
    dbCandidateInfo = datastore.get('CandidateInfo',candidateInfo['email'])
    
    if(dbCandidateInfo != None):
      return {'error':'YOu are already running for ' + candidateInfo['position'] + ' !!'}
    
    retData = datastore.save('CandidateInfo',candidateInfo['email'],
                               {'email':candidateInfo['email'],'name':candidateInfo['name'],
                                'position':candidateInfo['position'],
                                'slogan':candidateInfo['slogan']})
    return retData

def getCandidateInfo(candidateInfo):
  if ('email' not in candidateInfo or candidateInfo['email'] == ''):
    return {'error':"Email required!!"}
  return datastore.get('CandidateInfo',candidateInfo['email'])

def getCandidates():
  return datastore.getAll('CandidateInfo')

