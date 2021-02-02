from typing import Text
from django.shortcuts import render
import json
import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from function import *
usd = Main()


# *384*1792#

@csrf_exempt
def ussd(request):
    # request_json = request.body.decode('utf-8')
    # body = json.loads(request_json)
    if request.method == "POST":
        global response
        sessionId = request.POST['sessionId']
        serviceCode = request.POST['serviceCode']
        phoneNumber = request.POST['phoneNumber']
        text = request.POST['text']

        try:
            print(text)
            steps = text.split('*')
            print(steps)
            step = steps[-1]
            #print(phoneNumber)
            count = len(steps)
            print(count)
            m = phoneNumber[4:]
            mobile = f'{0}{m}'


            if text == '':
                response  = "CON WELCOME TO JUST USSD \n"
                if usd.Check(mobile)['reason'] == True:
                    response += "1. My Account \n"
                    response += "2. Wallet Transfer \n"
                    response += "3. Wallet Transfer \n"
                    response += "4. Buy Airtime \n"
                    response += "5. Buy Data \n"
                    response += "6. TV \n"
                else:
                    response += "0. Register"
            elif text == '1':
                response  = "CON \n"
                response += "1. Balance \n"
                response += "2. Account Number \n"
            elif text == '1*1':
                resp = usd.CheckBalance(mobile)
                if resp['code'] == 200:
                    bal = resp['bal']
                    response = "END " + bal
                else:
                    reason = resp['reason']
                    response = "END " + reason
            elif text == '1*2':
                resp = usd.CheckBalance(mobile)
                if resp['code'] == 200:
                    acctNo = resp['acctNo']
                    bank = resp['bank']
                    response = "END " + f'{acctNo} \n {bank}'
                else:
                    reason = resp['reason']
                    response = "END " + reason
            elif text == '2':
                response  = "CON \n"
                response += "Enter Mobile Number \n"
            elif steps[0] == '2' and count == 2:
                response  = "CON \n"
                response += "Amount \n"
            elif steps[0] == '2' and count == 3:
                response  = "CON \n"
                response += "PIN \n"
            elif steps[0] == '2' and count == 4:
                recNo = steps[1]
                amt = steps[2]
                pins = steps[3]
                resp = usd.SendMoney(amt, recNo, pins, mobile)
                if resp['code'] == 200:
                    reason = resp['reason']
                    response = "END " + f'{reason}'
                else:
                    reason = resp['reason']
                    response = "END " + reason
            
            elif text == '4':
                response  = "CON \n"
                response += "Enter Mobile Number \n"
            elif steps[0] == '4' and count == 2:
                response  = "CON \n"
                response += "Airtime Amount \n"
            elif steps[0] == '4' and count == 3:
                response  = "CON SELECT NETWORK \n"
                response += "1. MTN \n"
                response += "2. GLO \n"
                response += "3. 9Mobile \n"
                response += "4. Airtel \n"
            elif steps[0] == '4' and count == 4:
                response  = "CON \n"
                response += "PINS \n"
            elif steps[0] == '4' and count == 5:
                mno = steps[1]
                amt = steps[2]
                network = steps[3]
                pins = steps[4]
                if network == '1':
                    netw = 'mtn'
                    resp = usd.BuyAirtime(mobile, amt, mno, netw, pins)
                    reason = resp['reason']
                    response = "END " + reason
                elif network == '2':
                    netw = 'glo'
                    resp = usd.BuyAirtime(mobile, amt, mno, netw, pins)
                    reason = resp['reason']
                    response = "END " + reason
                elif network == '3':
                    netw = 'etisalat'
                    resp = usd.BuyAirtime(mobile, amt, mno, netw, pins)
                    reason = resp['reason']
                    response = "END " + reason
                else:
                    netw = 'airtel'
                    resp = usd.BuyAirtime(mobile, amt, mno, netw, pins)
                    reason = resp['reason']
                    response = "END " + reason
                
            elif text == '0':
                response  = "CON ACCOUNT TYPE \n"
                response += "1. AGENT \n"
                response += "2. USER \n"
            elif steps[0] == '0' and count == 2:
                response  = "CON \n"
                response += "Enter You Personal PIN "
            elif steps[0] == '0' and count == 3:
                role = steps[1]
                pins = steps[2]
                
                if role == '1':
                    roles = 'agent'
                    resp = usd.SignUp(mobile, pins, roles)
                    reason = resp['reason']
                    response = "END " + f'{reason}'
                else:
                    roles = 'user'
                    resp = usd.SignUp(mobile, pins, roles)
                    reason = resp['reason']
                    response = "END " + f'{reason}'
                
            return HttpResponse(response)
        except:
            return HttpResponse(response)
