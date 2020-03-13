
# Cisco SNTC Qapps User Guide

## Use Case Introduction

This Qapp will retrieve **Cisco** device maintenance information from Cisco cloud SNTC service and display it on NetBrain map as Data View (Cisco SNTC Qapp.xapp) or generate an overview report (Cisco SNTC Report.xapp).<br>
**The Data View includes:**
1. EOLProductID
2. EndOfSaleDate
3. EndOfServiceContractRenewal
4. LastDateOfSupport
5. ProductIDDescription
6. EOX_Migration_Details<br>
    a. MigrationInformation<br>
    b. MigrationOptions<br>
    c. MigrationProductId<br>
    d. MigrationProductInfoURL<br>
    e. MigrationProductName<br>
    f. MigrationStrategy<br>
    g. PIDActiveFlag<br>

**The report includes:**
1. EOLProductID
2. EndOfSaleDate
3. EndOfServiceContractRenewal
4. LastDateOfSupport
5. ProductIDDescription<br>

**Note: If there is no issue data available from the SNTC service, the Data View and report will display No Date/No Description/No Data, etc.**

## Setup Guide

### Create API Plugin

1.	Go to the System Management page.
2.	Click on the API Plugin Manager tab.
3.	Click on Add to add a new API Plugin.<br>
    a.	Set the name of the plugin as “Cisco SNTC API Plugin”.<br>
    b.	Copy and paste the following code into the Script field.<br>



```python
import requests
import requests.packages.urllib3 as urllib3
import json
import pythonutil
 
urllib3.disable_warnings()

import time
import threading

# provide a Locks class to avoid multithread API calling conflict.
class Locks:
    __instance = None
    __lock = threading.Lock()
    @staticmethod
    def getInstance():
        """ Static access method. """
        instance = Locks.__instance
        if instance == None:
            Locks.__lock.acquire()
            instance = Locks.__instance
            if instance == None:
                Locks.__instance = instance = Locks()
        return instance
    def __init__(self):
        """ Virtually private constructor. """
        if Locks.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Locks.__instance = self
            self.endpoint2locks = {}
            self.lock = threading.Lock()
    def update_lock(self, endpoint):
        self.lock.acquire()
        if not endpoint in self.endpoint2locks:
            self.endpoint2locks[endpoint] = threading.Lock()
        self.lock.release()
    def request_access(self, endpoint):
        lock = self.endpoint2locks[endpoint]
        lock.acquire()
        time.sleep(0.3)
        lock.release()
 
# First API call to get token from SNTC server.
def GetTokenClient(params, full_url, header, payload_id, payload_secret):
    apiServerId = params['apiServerId']
    servInfo = pythonutil.GetApiServerInfo(apiServerId)
    client_id = servInfo['username']
    client_secret = servInfo['password']
    payload=payload_id+client_id+payload_secret+client_secret
    #predefine the status code for lock function.
    status_code = 403
    #define the initial value for re-call counter.
    counter = 1
    #initial the lock function
    locks = Locks.getInstance()
    #apply which url should be locked in current call.
    locks.update_lock(full_url)
    response = {}
    try:
        #provide a while loop when we face conflict and with three times re-call.
        while status_code == 403 and counter < 4:
            # apply the lock to token API call.
            locks.request_access(full_url)
            response = requests.post(full_url, data=payload, headers=header, verify=False)
            status_code = response.status_code
            counter += 1
        if status_code == 200:
            result = response.json()
            token = result["token_type"] + " " + result["access_token"]
            return token
        else:
            print("Get Token Failed with API Response: " + response.text + " -- And API Header: " + response.headers)
    except Exception as e: print(str(e))
 
def GetWarrantyByID(token, sn, params):
    header = {'Authorization': token, 'Accept':'application/json'}
    apiServerId = params['apiServerId']
    servInfo = pythonutil.GetApiServerInfo(apiServerId)
    base_url = servInfo['endpoint']
    full_url = base_url + sn
    status_code = 403
    counter = 1
    locks = Locks.getInstance()
    locks.update_lock(base_url)
    response = {}
 
    try:
        while status_code == 403 and counter < 4:
            locks.request_access(base_url)
            response = requests.get(full_url, headers=header, verify=False)
            status_code = response.status_code
            counter += 1
        if status_code == 200:
            result = response.json()
            return result["EOXRecord"]
        else:
            print("Get Token Failed with API Response: " + response.text + " -- And API Header: " + response.headers)
    except Exception as e: print(str(e))

def _test(param):
    get_param = json.loads(param)
    client_id = get_param['username']
    client_secret = get_param['password']
    endpoint  = get_param['endpoint']
    full_url = "https://cloudsso.cisco.com/as/token.oauth2"
    
    header = {"Content-Type": "application/x-www-form-urlencoded", 'Accept':'application/json'}
    payload_id = "grant_type=client_credentials&client_id="
    payload_secret = "&client_secret="
    payload=payload_id+client_id+payload_secret+client_secret
    if endpoint == "https://api.cisco.com/supporttools/eox/rest/5/EOXBySerialNumber/1/":
        try:
            response = requests.post(full_url, data=payload, headers=header, verify=False)
            if response.status_code == 200:
                result = response.json()
                token = result['access_token']
                rtn = {"isFailed":False, "msg":"Connection Works! "+ "Token ID: "+ token}
                return json.dumps(rtn)
            elif response.status_code == 401:
                json_response = response.json()
                rtn = {'isFailed':True, 'msg':json_response['error_description']}
                return json.dumps(rtn)
        except Exception as e: print(str(e))
    else:
        rtn = {"isFailed":True, "msg":"Please verify your endpoint"}
        return json.dumps(rtn)
```

### Configure API Server Instance

1.	Go to the domain management page.
2.	Click on “Operations” and select API Server Manager.
3.	Press “Add” to add a new API server.<br>
    a.	Name the server “Cisco SNTC”.<br>
    b.	API Source Type should be “Cisco SNTC API Plugin” (previously created API Plugin).<br>
    c.	Put https://api.cisco.com/supporttools/eox/rest/5/EOXBySerialNumber/1/ into the Endpoint field. <br>
    d.	Put the Client ID and Client secret of your Cisco account in the “Username” and “Password” fields, respectively.<br>
    e.	Select an available Front Server.<br>
        **Note: If you have multiple Front Servers managing different group of devices, please repeat all steps to create API Server instance for each Front Server.**<br>
    f.	Press “OK” to finish creating the API Server.<br>
4.	Create a Device Group<br>
    a.	Go back to your NetBrain Desktop.<br>
    b.	Open the menu from the button in the top left corner.<br>
    c.	Click on “Device Group”.<br>
    d.	From the drop down from the folder “My Device Groups”, select “New Device Group”.<br>
    e.	Name your device group.<br>
    f.	Add the necessary devices through manual adding or Dynamic Search (these should be the devices that the Qapp is being used on).<br>
    g.	Select “OK” to finish the process.<br>
5.	Add API settings to device group.<br>
    a.	Open a map with one of the devices in the device group.<br>
    b.	Right click on the device and select “Shared Device Settings”.<br>
    c.	Click on the “API” tab and check the box for “Apply above Settings to device group”. In the drop down, select your device group.<br>
    d.	Check off the box next to “Cisco SNTC API Plugin”, and in the drop down select “Cisco SNTC API Plugin”.<br>
    e.	Click “Submit”.<br>

## How to Run The Qapp

**Cisco SNTC Qapp**<br>

1.	Open a NetBrain map.
2.	In the Runbook tab, press the “+” icon and select the “Cisco SNTC Qapp”. Make sure that the correct devices are in the queue by clicking on the top left of the Qapp tab. 
3.	For Data Source, select “Pull live data once”.
4.	Press Run.<br>

**Cisco SNTC Report**<br>

1. Navigate to Inventory Report.
2. Click on Go To Manage Reports Page>>.
3. Click on +New Inventory Report.
4. Fill out the forms, on Step 2 of 4, select Qapp Report.
5. Choose Cisco SNTC Report Qapp and pick "Pull live data once" as Data Source.
6. Click Finish.
7. Navigate back to Inventory Report and select Cisco SNTC Report.
8. Click on Run to upadte report with live data.
