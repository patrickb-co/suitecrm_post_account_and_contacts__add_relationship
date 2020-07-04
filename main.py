import requests

# sample account data / replace with data from chosen endpoint
randomusers = 'https://api.randomuser.me'
def getUsers(endpoint):
    r = requests.get(endpoint)
    
    results_first = format(r.json()["results"][0]["name"]["first"])
    results_last = format(r.json()["results"][0]["name"]["last"])
    full_name = " ".join([results_first, results_last])
    return full_name

#suitecrm api request data:
instance_api_url = "http://localhost:8888/SuiteCRM-7.11.13/Api/"
module_name = "Accounts"
auth_url = instance_api_url + "access_token"
modules_url = instance_api_url + "V8/module/" + module_name #get requests
post_url = instance_api_url + "V8/module"


client_id = "a662b808-243e-9ec3-332d-5eedb828fcac"
client_secret = "12345678"
username = "admin"
password = "12345678"
data_account = '{"data": {"type": "' + module_name + '","attributes": {"name":"' + getUsers(randomusers) + '"}}}'
data_contact = '{"data": {"type": "' + "Contacts" + '","attributes": {"first_name":"' + getUsers(randomusers) + '"}}}'


def authenticateSuiteCRM(auth_url, client_id, client_secret, username, password):  
    payload = {"grant_type":"password","client_id":client_id,"client_secret":client_secret,"username":username,"password":password}
    auth_request = requests.post(auth_url,data = payload)
    crm_token = format(auth_request.json()["access_token"])
    
    return crm_token

def getAccounts(url):
    request = requests.get(url, headers = {'Content-Type': 'application/json','Authorization': 'Bearer ' + authenticateSuiteCRM(auth_url,client_id,client_secret,username,password) })
    return format(request.json())
def postAccount(url): 
    request = requests.post(url, headers = {'Content-Type': 'application/json','Authorization': 'Bearer ' + authenticateSuiteCRM(auth_url,client_id,client_secret,username,password) }, data = data_account)
    return request.json()["data"]["id"]
def postContact(url):
    request = requests.post(url, headers = {'Content-Type': 'application/json','Authorization': 'Bearer ' + authenticateSuiteCRM(auth_url,client_id,client_secret,username,password) }, data = data_contact)
    return request.json()["data"]["id"]


def postRelationship(module_name_A, module_name_B, base_url):
    
    url = base_url + "/Api/V8/module/" + module_name_A + "/"+postAccount(post_url)+"/relationships"

    payload = "{\n  \"data\": {\n    \"type\": \"" + module_name_B + "\",\n    \"id\": \""+postContact(post_url)+"\"\n  }\n}"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + authenticateSuiteCRM(auth_url,client_id,client_secret,username,password) }

    response = requests.request("POST", url, headers=headers, data = payload)
    print(response.text.encode('utf8'))   



#print(getAccounts(modules_url))
#print(postAccount(post_url))
#print(postContact(post_url))
#print(authenticateSuiteCRM(auth_url,client_id,client_secret,username,password))
postRelationship("Accounts","Contacts","http://localhost:8888/SuiteCRM-7.11.13")