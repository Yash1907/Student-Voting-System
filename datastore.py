from google.cloud import datastore

def getCount(entityName):
    dsClient = datastore.Client()
    if ( dsClient == None):
      return { 'error': 'Internal Error! Failed to get DB!!' }    
    if (entityName == None or entityName == ""):
      return { 'error': 'Entity Name is Required!!' }
    query = dsClient.query(kind=entityName)
    query.keys_only()
    data = query.fetch()
    return {'count': len(data)}

def getAll(entityName):
  dsClient = datastore.Client()
  if ( dsClient == None):
    return { 'error': 'Internal Error! Failed to get DB!!' }  
  if (entityName == None or entityName == ""):
    return { 'error': 'Entity Name is Required!!' }
  query = dsClient.query(kind=entityName)
  return list(query.fetch())

def get(entityName, entityKey):
  dsClient = datastore.Client()
  if ( dsClient == None):
    return { 'error': 'Internal Error! Failed to get DB!!' }  
  if (entityName == None or entityName == ""):
    return { 'error': 'Entity Name is Required!!' }
  if (entityKey == None or entityKey == ""):
    return { 'error': 'Entity Key is Required!!' }
  return dsClient.get(dsClient.key(entityName,entityKey))

def save(entityName, entityKey, entityData):
  dsClient = datastore.Client()
  if (dsClient == None):
    return { 'error': 'Internal Error! Failed to get DB!!' }  
  if (entityName == None or entityName == ""):
    return { 'error': 'Entity Name is Required!!' }
  if (entityKey == None or entityKey == ""):
    return { 'error': 'Entity Key is Required!!' }
  if (entityData == None):
    return { 'error': 'Entity Data is Required!!' }
  
  key = dsClient.key(entityName,entityKey)

  entity = dsClient.entity(key)
  for k in entityData:
    entity[k]=entityData[k]
  try:
    dsClient.put(entity)
    return {'message':entityName + ' Save Successful'}
  except:
    return {'error':'Datastore Save Failed!'}

def delete(entityName, entityKey):
  dsClient = datastore.Client()
  if (dsClient == None):
    return { 'error': 'Internal Error! Failed to get DB!!' }  
  if (entityName == None or entityName == ""):
    return { 'error': 'Entity Name is Required!!' }
  if (entityKey == None or entityKey == ""):
    return { 'error': 'Entity Key is Required!!' }
  
  key = dsClient.key(entityName,entityKey)
  try:
    dsClient.delete(key)
    return {'message':entityName + ' Delete Successful'}
  except:
    return { 'error': 'Entity Key is Required!!' }