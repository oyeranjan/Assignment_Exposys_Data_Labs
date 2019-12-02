import hashlib
import random
from flask import Flask
from flask import request
from flask import Response
import cypher

app = Flask(__name__)

emails = ["abc@gmail.com", "xyz@gmail.com", "pqr@gmail.com"]
lst = ["ABC", "XYZ", "PQR"]
key = random.choice(lst)
token = hashlib.md5(b"Rajeev1234").hexdigest()


@app.route("/")
def init():
    return "Server is online"

#---------------VERIFICATION-----------------
@app.route("/getChallenge")
def get_challenge():
    email = request.args.get('email')
    response = {}
    if email in emails:
        response = {'status': 'success', 'challenge': key}
    else:
        response = {'status': 'failed', 'reason': 'Bad Client'}
    return Response(str(response), mimetype="text/plain")

#-------------------VALIDATION------------------------
@app.route("/setChallenge", methods=['GET'])
def set_challenge():
    response = request.args.get('response')
    aesCypher = cypher.AESCipher(key="qwertyuioplkjhgf")
    print(len(response))
    orig = aesCypher.decrypt(response)
    print(type(response), type(orig))
    print(key, orig)
    auth_response = {}
    if key == orig:
        auth_response = {'status': 'success', 'token': token}
    else:
        auth_response = {'status': 'failed'}
    return str(auth_response)

#-----------------------AUTHENTICATION--------------------
@app.route("/getFile", methods=['GET'])
def set_file():
    filename = request.args.get('filename')
    received_token = request.args.get('token')
    if token == received_token:
        file = open(filename, "r")
        data = file.readlines()
        return str(data)
    else:
        return "Invalid token"
