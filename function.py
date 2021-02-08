import json
import requests


baseurl = 'https://justussd.savitechnig.com'

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
            "role": 'user'
            }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
        resp = json.loads(response.text)
        return resp

    
    def GetBank(self, page):
        url = f'{baseurl}/api/getBank?page={page}'

        payload={}
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        bank = json.loads(response.text)
        return bank

    
    def VerifyBank(self, acct, bnkcode):
        url = f'{baseurl}/api/accountVerify'

        payload={
            "accountNumber":f'{acct}',
            "bankCode":f'{bnkcode}'
            }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data = json.dumps(payload))

        vbnk = json.loads(response.text)
        return vbnk

    
    def BankTranfer(self, mobile, amount, acctno, bnkcode, upin):
        url = f'{baseurl}/api/btranfer/{mobile}'

        payload={
            "amount":f'{amount}',
            "accountNumber":f'{acctno}',
            "bankCode": f'{bnkcode}',
            "pin":f'{upin}'
            }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data= json.dumps(payload))

        btranfer = json.loads(response.text)
        return btranfer
    

    def BuyAirtime(self, mobile, amount, recno, netw, pins):
        url = f'{baseurl}/api/buyAirtime/{mobile}'

        payload = {
            "amount": f'{amount}',
            "number": f'{recno}',
            "network": f'{netw}',
            "pin": f'{pins}'
            }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data = json.dumps(payload))

        resp = json.loads(response.text)
        return resp


    def VerifyPower(self, serviceType, serviceID, meterNumber):
        url = f'{baseurl}/api/verifyPower'

        payload = {
            "serviceType": serviceType,
            "serviceID": serviceID,
            "meterNumber": meterNumber
            }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data = json.dumps(payload))

        resp = json.loads(response.text)
        return resp

    def PayPower(self, mobile, variation_code, serviceID, amount, meterNumber, pin):
        url = f'{baseurl}/api/buypower/{mobile}'

        payload = {
            "variation_code": variation_code,
            "serviceID": serviceID,
            "amount": amount,
            "meterNumber": meterNumber,
            "pin":pin
            }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data = json.dumps(payload))

        resp = json.loads(response.text)
        return resp