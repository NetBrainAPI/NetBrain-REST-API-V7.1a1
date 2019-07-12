
# Change Management Approval Process API Design

## ***POST*** /V1/CM/Approval/State
This API call is used to set CM Runbook approval state example - approve or reject.

 

## Detail Information

 

> **Title** : Approve a change management request<br>

 

> **Version** : 06/26/2019.

 

> **API Server URL** : http(s)://IP address of NetBrain Web API Server/ServicesAPI/API/V1/CM/Approval/State  

 

> **Authentication** : 

 

|**Type**|**In**|**Name**|
|------|------|------|
|<img width=100/>|<img width=100/>|<img width=500/>|
|Bearer Authentication| Headers | Authentication token | 

 

 ## Request body(****required***)

 

|**Name**|**Type**|**Description**|
|------|------|------|
|<img width=100/>|<img width=100/>|<img width=500/>|
|runbookId* | string  | ID of the Change Management Runbook  |
|ticketId* | string  | Other vendor's ticket number  |
|vendor* | string  | Name of the vendor  |
|ticketName | string  | Change Management ticket ID  |
|state* | integer  | 0(planning)/1(pending)/2(approved) /3(rejected) /5(archived)  |

 

> ### ***Example***


```python
body = {
    'vendor': 'serviceNow',
    'ticketId': "00008",
    'runbookId': '7652cb62-c5e6-d0a3-3f22-29972d03ad4c',
    'ticketUrl': 'servicenow.com',
    'state': 2
}
```

 

## Headers

 

> **Data Format Headers**

 

|**Name**|**Type**|**Description**|
|------|------|------|
|<img width=100/>|<img width=100/>|<img width=500/>|
| Content-Type | string  | support "application/json" |
| Accept | string  | support "application/json" |

 

> **Authorization Headers**

 

|**Name**|**Type**|**Description**|
|------|------|------|
|<img width=100/>|<img width=100/>|<img width=500/>|
| token | string  | Authentication token, get from login API. |

 


## Response

 

|**Name**|**Type**|**Description**|
|------|------|------|
|<img width=100/>|<img width=100/>|<img width=500/>|
|statusCode| integer | Code issued by NetBrain server indicating the execution result.  |
|statusDescription| string | The explanation of the status code. |

 

> ***Example***
 


```python

```
