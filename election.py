from google.cloud import datastore as gcDS
import datastore
import result

def getCurrentActiveElection():
  query = gcDS.Client().query(kind='Election')
  query.add_filter(filter=gcDS.query.PropertyFilter('status','=','active'))
  return list(query.fetch())

def isCurrentActiveElection():
  if(len(getCurrentActiveElection()) > 0):
    return True
  return False  

def startNewElection(electionInfo):
  if(electionInfo == None or 'electionName' not in electionInfo or electionInfo['electionName'] == '' or 
     'electionYear' not in electionInfo or electionInfo['electionYear'] == ''):
    return {'error':'electionName and electionYear are required to start an election!!'}

  if(isCurrentActiveElection()):
    return {'error':'There is a current active election. Cannot start a new election!!'}
  electionObj = datastore.get('Election',electionInfo['electionName'] + electionInfo['electionYear'])
  if(electionObj != None):
    return {'error':'There is an election with ' + electionInfo['electionName'] + 'and' + electionInfo['electionYear']}
  datastore.save('Election',electionInfo['electionName'] + electionInfo['electionYear'],
                 {'electionName':electionInfo['electionName'],'electionYear':electionInfo['electionYear'],'status':'active'})
  return {'message':'New Election Started!!'}

def endCurrentElection():
  electionObjs = getCurrentActiveElection()
  if(len(electionObjs) == 0):
    return {'error':'There is no current active election!!'}
  if(len(electionObjs) > 1):
    return {'error':'Internal Error found more than 1 current active election!!'}
  electionObj = electionObjs[0]
  retObj = result.tabulateResult(electionObj)
  if('error' in retObj):
    return retObj
  users = datastore.getAll('UserAccount')
  for userObj in users:
    userObj['voted'] = 'no'
    retObj = datastore.save('UserAccount',userObj['email'],userObj)
    if('error' in retObj):
      return retObj
  datastore.save('Election',electionObj['electionName'] + electionObj['electionYear'],
                 {'electionName':electionObj['electionName'],'electionYear':electionObj['electionYear'],'status':'ended'})
  return {'message':'Current Election Ended!!'}