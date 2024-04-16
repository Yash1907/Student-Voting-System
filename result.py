import datastore

def tabulateResult(electionInfo):
  if(electionInfo == None or 'electionName' not in electionInfo or electionInfo['electionName'] == '' or 
     'electionYear' not in electionInfo or electionInfo['electionYear'] == ''):
    return {'error':'electionName and electionYear are required to tabulate election results!!'}
  candidates = datastore.getAll('CandidateInfo')
  for candidateInfo in candidates:
    votes = 0
    if('votes' in candidateInfo):
      votes = candidateInfo['votes'] 
    electionTabulation = {'electionName':electionInfo['electionName'],
                          'electionYear':electionInfo['electionYear'],
                          'email':candidateInfo['email'],'name':candidateInfo['name'],
                          'position':candidateInfo['position'],'slogan':candidateInfo['slogan'],'votes':votes}
    key = electionInfo['electionName'] + electionInfo['electionYear'] + candidateInfo['email']
    retObj = datastore.save('ElectionResult',key,electionTabulation)
    if('error' in retObj):
      return retObj
    retObj = datastore.delete('CandidateInfo',candidateInfo['email'])
    if('error' in retObj):
      return retObj
  return {'message':'Election Result Tabulation Successful'}

def getAllResults():
  return datastore.getAll('ElectionResult')