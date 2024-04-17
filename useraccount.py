import datastore
import hashlib

def login(userAccount):
    if ('email' not in userAccount or 'password' not in userAccount or userAccount['email'] == '' or userAccount['password'] ==''):
     return {'error':"Email, Password are required!!"}
    dbUserAcct = datastore.get('UserAccount',userAccount['email'])
    if(dbUserAcct == None):
      return {'error':'Login Failed User does not exist!!'}
    hasedPassword = hashlib.sha256(userAccount['password'].encode()).hexdigest()
    if(dbUserAcct['password'] == hasedPassword):
      retObj = {'message':'Login Successful!!', 'name':dbUserAcct['name']}
      if(dbUserAcct['isCouncilMember'] == 'yes'):
        retObj['councilMemberCode'] = dbUserAcct['councilMemberCode']
      retObj['voted'] = 'no'
      if('voted' in dbUserAcct):
        retObj['voted'] = dbUserAcct['voted']
      return retObj
    return {'error':'Login Failed!!'}

def hasVoted(userAccount):
  if (userAccount == None or 'email' not in userAccount or userAccount['email'] == ''):
     return {'error':"Email required!!"}  
  dbUserAcct = datastore.get('UserAccount',userAccount['email'])
  if(dbUserAcct == None):
    return {'error':"No User Exists for " + userAccount['email']}
  if('voted' in dbUserAcct):
    return {'voted':dbUserAcct['voted']}
  return {'voted':'no'}
    

def signup(userAccount):
  if ('name' not in userAccount or 'password' not in userAccount or 'email' not in userAccount or
     'repassword' not in userAccount):
     return {'error':"Name, Email, Password repassword are required!!"}
  else:
    if (userAccount['name'] == '' or userAccount['password'] == '' or userAccount['email'] == '' or 
        userAccount['repassword'] == ''):
     return {'error':"Name, Email, Password repassword cannot be empty!!"}
  isCouncilMember = 'no'
  if('isCouncilMember' in userAccount and userAccount['isCouncilMember'] == 'on'):
     isCouncilMember = 'yes'
     if('councilMemberCode' not in userAccount or userAccount['councilMemberCode'] == ''):
       return {'error':"Council Member code is mandatory for council members!!"}
  if(userAccount['password'] != userAccount['repassword']):
     return {'error':"Password and repassword are not same!!"}
  dbUserAcct = datastore.get('UserAccount',userAccount['email'])
  if(dbUserAcct != None):
    return {'error':'Account Already Exists'}
  retData = datastore.save('UserAccount',userAccount['email'],
                               {'email':userAccount['email'],'name':userAccount['name'],
                                'password':hashlib.sha256(userAccount['password'].encode()).hexdigest(),
                                'isCouncilMember':isCouncilMember,'councilMemberCode':userAccount['councilMemberCode']})
  return retData
