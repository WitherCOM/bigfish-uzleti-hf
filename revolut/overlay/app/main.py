import os
from dotenv import load_dotenv
from fastapi import FastAPI
import requests
from datetime import datetime, timedelta
import json
import mysql.connector
import jwt

load_dotenv()

ACCESS_TOKEN = None
EXPIRE_AT = datetime.now()

DB_HOST = os.environ.get("DB_HOST","localhost")
DB_USER = os.environ.get("DB_USER","")
DB_PASS = os.environ.get("DB_PASS","localhost")
DB_NAME = os.environ.get("DB_NAME","localhost")

AUTH_URL = os.environ.get("AUTH_URL", "https://sandbox-oba-auth.revolut.com/token")
UI_URL = os.environ.get("UI_URL","https://sandbox-oba.revolut.com/ui/index.html")
CONSENT_URL = os.environ.get("CONSENT_URL", "https://sandbox-oba.revolut.com/account-access-consents")
KID = os.environ.get("KID", "mykidrevotest")
N_CLAIM = os.environ.get("N_CLAIM", "")
CLIENT_ID = os.environ.get("CLIENT_ID","asd")
REDIRECT_URI = os.environ.get("REDIRECT_URI", "asd")


def requestToken():
    global AUTH_URL
    global ACCESS_TOKEN
    global EXPIRE_AT
    if ACCESS_TOKEN != None and datetime.now() < EXPIRE_AT:
        return
    response = requests.post(AUTH_URL,cert= ('/certs/transport.pem', '/certs/private.key'),
                             headers = {'Content-Type': 'application/x-www-form-urlencoded'}, 
                             data = {'grant_type': 'client_credentials', 'scope': 'accounts'},verify=False)
    if response.status_code == 403:
        raise Exception("Cannot get token")
    ACCESS_TOKEN = response.json()['access_token']
    EXPIRE_AT = datetime.now() + timedelta(seconds=int(response.json()['expires_in']))

def setupHeader():
    requestToken()
    return  {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-fapi-financial-id': '001580000103UAvAAM',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }


def accountConsent():
    global CONSENT_URL
    payload = json.dumps({
        "Data": {
            "Permissions": [
                "ReadAccountsBasic",
                "ReadAccountsDetail",
                "ReadTransactionsBasic",
                "ReadTransactionsCredits",
                "ReadTransactionsDebits",
                "ReadTransactionsDetail"
            ],
            "ExpirationDateTime": "2024-12-02T00:00:00+00:00",
        },
        "Risk": {}
    })
    response = requests.post(CONSENT_URL, headers=setupHeader(), data=payload)
    return response.json()["Data"]["ConsentId"]


def defineBaseStructure():
    global DB_USER
    global DB_HOST
    global DB_PASS
    global DB_NAME
    cnx = mysql.connector.connect(user=DB_USER, password=DB_PASS,
                              host=DB_HOST,
                              database=DB_NAME)
    cursor = cnx.cursor()
    try:
        with open('init.sql') as file:
            cursor.execute(file.read(),multi=True)
    except mysql.connector.Error as err:
        print(err)
    
    cursor.close()
    cnx.close()

def insertAccess(id, token, expires_in):
    global DB_USER
    global DB_HOST
    global DB_PASS
    global DB_NAME
    cnx = mysql.connector.connect(user=DB_USER, password=DB_PASS,
                              host=DB_HOST,
                              database=DB_NAME)
    cursor = cnx.cursor(dictionary=True)
    try:
        cursor.execute("INSERT INTO revolut_users (token_id, access_token, expires_at) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE access_token=%s, expires_at=%s;",(id, token, datetime.now()+timedelta(seconds=expires_in),token,datetime.now()+timedelta(seconds=expires_in)))
        cnx.commit()
    except mysql.connector.Error as err:
        print(err)
    cursor.close()
    cnx.close()


if __name__ == "__main__":
    print("Generating db structure")
    defineBaseStructure()
app = FastAPI()

@app.get("/jwk")
def jwk():
    global KID
    global N_CLAIM
    return {
        "keys": [
            {
                "e": "AQAB",
                "n": N_CLAIM,
                "kid": KID,
                "kty": "RSA",
                "use": "sig"
            }
        ]
    }


@app.get('/authorization_url')
def formAuthURL():
    global CLIENT_ID
    global UI_URL
    global REDIRECT_URI
    with open('/certs/private.key') as file:
        private_key = file.read()
        file.close()
    jwToken = jwt.encode({
        "response_type": "code id_token",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "accounts",
        "claims": {
            "id_token": {
                "openbanking_intent_id": {
                    "value": accountConsent()
                }
            }
        }
    },private_key,algorithm="PS256", headers={"kid": KID})

    return {'authorization_url' :f"{UI_URL}?response_type=code%20id_token&scope=accounts&redirect_uri={REDIRECT_URI}&client_id={CLIENT_ID}&request={jwToken}&state=example_state"}


@app.get('/callback')
def callback(code: str, id_token: str, state: str):
    response = requests.post(AUTH_URL,cert= ('/certs/transport.pem', '/certs/private.key'),
                             headers = {'Content-Type': 'application/x-www-form-urlencoded'}, 
                             data = {'grant_type': 'authorization_code', 'code': code},verify=False).json()
    id = response['access_token_id']
    token = response['access_token']
    expires_in = int(response['expires_in'])

    insertAccess(id, token, expires_in)
    return {'status': 'ok'}

@app.get('/access')
def access():
    global DB_USER
    global DB_HOST
    global DB_PASS
    global DB_NAME
    cnx = mysql.connector.connect(user=DB_USER, password=DB_PASS,
                              host=DB_HOST,
                              database=DB_NAME)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM revolut_users;")
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()
    return rows
