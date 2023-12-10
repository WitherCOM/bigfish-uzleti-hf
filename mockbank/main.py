import os
from dotenv import load_dotenv
from fastapi import FastAPI
import requests
from datetime import datetime, timedelta
import sqlite3
import jwt
from base64 import b64encode 




CLIENT_ID = "bme1952"
CLIENT_SECRET = "bme1952secret"
REDIRECT_URI = "http://localhost:8000/callback"

def defineBaseStructure():
    conn = sqlite3.connect("mockbank.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE tokens(access_token, expires_in)")
    conn.close()

if __name__ == "__main__":
    print("Generating db structure")
    defineBaseStructure()

app = FastAPI()


@app.get('/authorization_url')
def formAuthURL():
    return {'authorization_url' :f"https://oauth.mockbank.io/oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"}


@app.get('/callback')
def callback(code: str):
    token  = str(b64encode(bytes(f'{CLIENT_ID}:{CLIENT_SECRET}','ascii')),'ascii')
    resp = requests.post('https://oauth.mockbank.io/oauth/token',{
        'redirect_uri': REDIRECT_URI,
        'code': code,
        'grant_type': 'authorization_code'
    }, headers = {'Authorization': f'Basic {token}'}).json()
    token = resp['access_token']
    expires_in = resp['expires_in']
    conn = sqlite3.connect("mockbank.db")
    cur = conn.cursor()
    cur.execute(f'INSERT INTO tokens VALUES("{token}",{expires_in})')
    conn.commit()
    conn.close()
    return {'status': 'ok'}

@app.get('/access')
def access():
    conn = sqlite3.connect("mockbank.db")
    cur = conn.cursor()
    res = cur.execute('SELECT * FROM tokens')
    data = res.fetchall()
    conn.close()
    return list(map(lambda row: {'access_token': row[0], 'expires_in': row[1]} , data))