import requests
import json
username = input('Username: ')
password = input('Password: ')


#Create consent
consent_res = requests.post('https://api.mockbank.io/v1/consents', json.dumps({
        'access': {
            'allPsd2': 'allAccounts',
        },
        'frequencyPerDay': 0,
        'recurringIndicator': 'false',
        'validUntil': '2030-10-10'
        }), headers={'Content-Type':'application/json', 'X-Request-ID': '3d1afce9-f7fe-4b3a-89cb-cd03b7820b63', 'PSU-ID': username}).json()
print("--DEBUG--")
print(consent_res)
print(consent_res['_links'].keys())
print("---------")
print(consent_res['consentId'])

start_auth_res = requests.post(consent_res['_links']['startAuthorisation']['href'],json.dumps({
                    'psuData': {
                        'password': password
                    }
                }), headers={'Content-Type':'application/json', 'X-Request-ID': 'e5b654ab-c95e-4014-be4f-1e043e714bca', 'PSU-ID': username}).json()
print("--DEBUG--")
print(start_auth_res)
print("---------")

method = input('Auth method id: ')
code = input('Pin code: ')

choose_auth_res = requests.put(start_auth_res['_links']['updatePsuAuthentication']['href'],json.dumps({
                    'authenticationMethodId': method
                }), headers={'Content-Type':'application/json', 'X-Request-ID': 'e5b654ab-c95e-4014-be4f-1e043e714bca', 'PSU-ID': username}).json()

print("--DEBUG--")
print(choose_auth_res)
print("---------")

finish_auth_res = requests.put(start_auth_res['_links']['updatePsuAuthentication']['href'],json.dumps({
                    'scaAuthenticationData': code
                }), headers={'Content-Type':'application/json', 'X-Request-ID': 'e5b654ab-c95e-4014-be4f-1e043e714bca', 'PSU-ID': username}).json()

print("--DEBUG--")
print(finish_auth_res)
print("---------")

print("You can use: ",consent_res['consentId'])



