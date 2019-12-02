import requests
import cypher
import json


def post(url):
    res = requests.get(url).text
    return res

email = 'abc@gmail.com'
response = post('http://127.0.0.1:5000/getChallenge?email='+email)
rawResponse = response.replace("\'", "\"")
json_response = json.loads(rawResponse)
print(json_response,"\nVerification Sucess.\n") #printing Response just for Reference

if json_response["status"]=="failed":
    print(json_response["reason"])
    exit()
else:
    enc = cypher.AESCipher(key="qwertyuioplkjhgf").encrypt(json_response["challenge"])
    response = enc.decode()

rawResponse = post('http://127.0.0.1:5000/setChallenge?response=' + response)
rawResponse = rawResponse.replace("\'", "\"")
json_response = json.loads(rawResponse)
print(json_response,"\nValidation Sucess.\n") #printing Response just for Reference

if json_response["status"] == "success":
    print("Authentication successful\n File Transfer in Process:")
    token = json_response["token"]
    filename = 'file1.txt'
    fileResponse = post('http://127.0.0.1:5000/getFile?filename=' + filename + "&token=" + token)
    print(fileResponse)
else:
    print("Failed to authenticate")
    exit()
