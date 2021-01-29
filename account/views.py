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
        #print(phoneNumber)

        m = phoneNumber[4:]
        mobile = f'{0}{m}'
        
        if text == '':
            response  = "CON WELCOME TO JUST USSD \n"
            response += "1. My Account \n"
            response += "2. Send Money \n"
            response += "3. Buy Airtime"
        elif text == '1':
            response = "CON Choose account information you want to view \n"
            response += "1. Account Number \n"
            response += "2. Account balance"
        elif text == '1*1':
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
        elif text == text:
            print(text)
            nno = text[4:]
            mob = f'{nno}'
            response = "CON \n"
            response += "Amount"
        elif steps.index(text) == '3':
            
            response = "CON \n"
            response += "PIN"
        return HttpResponse(response)
