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


# *384*13028#

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

        steps = text.split('*')
        print(steps)
        step = steps[-1]
        #print(phoneNumber)
        count = steps.index(step)
        print(count)
        m = phoneNumber[4:]
        mobile = f'{0}{m}'


        check = usd.Check(mobile)
        
        # if  check['reason'] == False:
        #     response = "CON WELCOME TO JUST USSD\n"
        #     response += "Enter Transaction Pin to complete your Registration"
        # elif text == f'{steps[0]}':
        #     pin = steps[0]
        #     print(pin)
        if text == '':
            response  = "CON WELCOME TO JUST USSD \n"
            if check['reason'] == True:
                response += "1. My Account \n"
                response += "2. Send Money \n"
                response += "3. Buy Airtime"
            else:
                response += "0. Register"
        elif text == '0':
            response = "CON \n"
            response += "Enter Security PIN"
        elif text == f'0*{step}':
            pins = steps[1]
            res = usd.SignUp(mobile, pins)
            reason = res['reason']
            response = "END " + f'{reason}'
        elif text == '1':
            response = "CON Choose account information you want to view \n"
            response += "1. Account Number \n"
            response += "2. Account balance"
        elif text == f'1*1':
            resp = usd.CheckBalance(mobile)
            acctno = resp['acctNo']
            bank = resp['bank']
            accountNumber  = f'{acctno}\n {bank}'
            response = "END Your account number is " + accountNumber
        elif text == '1*2':
            resp = usd.CheckBalance(mobile)
            bal = resp['bal']
            balance  = f'{bal}'
            response = "END Your balance is " + balance
        elif text == '2':
            response = "CON Transaction Type \n"
            response += "1. Send to Wallet \n"
            response += "2. Send to Bank"
        elif text == '2*1':
            response = "CON \n"
            response += "Enter Reciever Number"
        elif text == f'2*1*{step}':
            print(text)
            nno = text[4:]
            mob = f'{nno}'
            response = "CON \n"
            response += "Amount"
        elif text == f'2*1*{steps[2]}*{step}':
            response = "CON \n"
            response += "PIN"
        elif text == f'2*1*{steps[2]}*{steps[3]}*{step}':
            rec = steps[2]
            amt = steps[3]
            pin = steps[4]
            print(pin)
            rep = usd.SendMoney(amt, rec, pin, mobile)
            reason = rep['reason']
            print(reason)
            response = "END " + f'{reason}'
        elif text == '3':
            pass
        return HttpResponse(response)
