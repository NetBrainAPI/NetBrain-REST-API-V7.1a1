import orionsdk
import json
 
class APIPlugin:
     
    def __init__(self, user, pwd, url):
        #test
        self._usr = user
        self._pwd = pwd
 
    def _test(self):
        paras = 'test'
        return self.samplefunction(paras)
         
    def samplefunction(self, params):
        result='Plugin executed function successfully'
        return result
        
        
# API Domain Manager Test function definition.
def _test(param):
    if isinstance(param, str):
        param = json.loads(param)

    username = param['username']
    password = param['password']
    endpoint = param['endpoint']

    api = APIPlugin(username, password, endpoint)
    result = api._test()
    rtn = {"isFailed":False, "msg":str(result)}
    return json.dumps(rtn)         