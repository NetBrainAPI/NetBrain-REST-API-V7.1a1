import requests
import json
import urllib3
from orionsdk import SwisClient
import re
import pythonutil
   
urllib3.disable_warnings()
  
class APIPlugin:
    _headers = {"Content-Type": "application/json",
                "Accept": "application/json"}
   
    def __init__(self, user, pwd, url):
        self._user = user
        self._pwd = pwd
        self.auth = (self._user, self._pwd)
 
        if re.search('http://(.+)', url):
            stripped = re.search('http://(.+)', url)
            url = stripped.group(1)
        self._swis = SwisClient(url, user, pwd)
  
    #Define a customized RESTful Get function template.        
    def _query(self, query, deviceName):
        #urlParams = {}
        #if 'urlParams' in param:
        #    urlParams=param['urlParams']
        try:
            response = self._swis.query(query,id=deviceName)
            return response
        except Exception as e:
            return str(e)
    
    # API Plugin Test function definition. The sample test function random retrieves an incident number from ServiceNow to verify the connection.
    #def _test(self):
    #    query = 'SELECT NodeID,IPAddress,CPULoad,PercentMemoryUsed,Uri FROM Orion.Nodes WHERE Caption LIKE @id'
    #    deviceName='NBUSDC-SW1'
    #    print(deviceName)
    #    print(query)
    #    print(self._swis)
    #    result = self._swis.query(query,id=deviceName)
    #    #result = str(self._query(query, deviceName))
    #    print(result)
    #    return result
  
    
 
 # The NetBrain initial parameters with customized fields.
def extract_param(param):
    # The NetBrain initial parameters with customized fields.
    if isinstance(param, str):
        param = json.loads(param)
  
    #username, password, endpoint are build-in keywords in initial param.
    username = ''
    password = ''
    endpoint = ''
    #callParam is customized fields.
    callParam = {}
  
    apiServerId = ''
    servInfo = {}
    if 'apiServerId' in param:
        apiServerId = param['apiServerId']
        servInfo = pythonutil.GetApiServerInfo(apiServerId)
        username = servInfo['username']
        password = servInfo['password']
        endpoint = servInfo['endpoint']
    else:
        if 'username' in param:
            username = param['username']
        if 'password' in param:
            password = param['password']
        if 'endpoint' in param:
            endpoint = param['endpoint']

    if 'query' in param:
        query = param['query']
    if 'deviceName' in param:
        deviceName = param['deviceName']   
  
    return (username, password, endpoint, query, deviceName)
 
# API Domain Manager Test function definition.
def _test(param):
    if isinstance(param, str):
        param = json.loads(param)

    username = param['username']
    password = param['password']
    endpoint = param['endpoint']

    api = APIPlugin(username, password, endpoint)
    #print(api)
    #print("Test: "+str(param))
    deviceName='NBUSMA-SW1'
    query='SELECT NodeID,IPAddress,CPULoad,PercentMemoryUsed,Uri FROM Orion.Nodes WHERE Caption LIKE @id'
    result = api._query(query, deviceName)
    #print(result)
    #"isFailed" and "msg" key fileds are the required.
    rtn = {"isFailed":False, "msg":str(result)}
    return json.dumps(rtn) 




# Public function for API parser.
def getData(param):
    username, password, endpoint, query , deviceName= extract_param(param)
    ap = APIPlugin(username, password, endpoint)
    #paramdict={"query":query, "deviceName": deviceName}
    rtn = ap._query(query, deviceName)
    return json.dumps(rtn)
 
 
param = {'deviceName': 'NBUSMA-SW1', 'endpoint': 'http://192.168.31.99', 'password': 'Netbrain1', 'query': 'SELECT NodeID,IPAddress,CPULoad,PercentMemoryUsed,Uri FROM Orion.Nodes WHERE Caption LIKE @id', 'username': 'admin'}
#print(getData(param))
print(_test(param))