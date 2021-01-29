import json
import requests


baseurl = 'https://23bccae6424d.ngrok.io'

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
    

    def SendMoney(self, amount, rec, pin):
        url = f'{baseurl}/api/transfer/08022301477'

        payload = {
            "amount": f'{amount}',
            "reciever":f'{rec}',
            "pin": f'{pin}'
            }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        resp = json.loads(response.text)
        return resp