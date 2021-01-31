import json
import requests


baseurl = 'https://6a9177178384.ngrok.io'

class Main:

    def CheckBalance(self, mobile):
        url = f'{baseurl}/api/account/{mobile}'

        payload  = {}
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data = payload)

        resp = json.loads(response.text)
        return resp
    

    def SendMoney(self, amount, rec, pin, mobile):
        url = f'{baseurl}/api/transfer/{mobile}'

        payload = {
            "amount": f'{amount}',
            "reciever":f'{rec}',
            "pin": f'{pin}'
            }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
        resp = json.loads(response.text)
        # print(resp)
        return resp


    def Check(self, mobile):
        url = f'{baseurl}/api/check/{mobile}'

        payload={}
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        resp = json.loads(response.text)
        return resp

    
    def SignUp(self, mobile, pin):
        url = f'{baseurl}/api/signup'

        payload = {
            "mobile": f'{mobile}',
            "pwd": f'{pin}',
            "role":"user"
            }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
        resp = json.loads(response.text)
        return resp