from django.shortcuts import render
import json
import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt



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
        #print(phoneNumber)

        mobile = phoneNumber[1:]
        #print(mobile)
        url = f'http://68.183.120.74:8081/api/v1/bal/{mobile}'

        payload  = {}
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data = payload)

        resp = json.loads(response.text)
        #print(resp)
        bal = resp['bal']
        cur = resp['currency']
        if text == '':
            response  = "CON What would you want to check \n"
            response += "1. My Account \n"
            response += "2. Send Money \n"
            response += "3. My Wallet Number"
        elif text == '1':
            response = "CON Choose account information you want to view \n"
            response += "1. Wallet Number \n"
            response += "2. Account balance"
        elif text == '1*1':
            accountNumber  = f'{mobile}'
            response = "END Your account number is " + accountNumber
        elif text == '1*2':
            balance  = f'{cur} {bal}'
            response = "END Your balance is " + balance
        elif text == '2':
            response = "CON Transaction Type \n"
            response += "1. Wallet to Wallet \n"
            response += "2. Wallet to Bank"
        elif text == '2*1':
            response = "CON \n"
            response += "Enter Reciever Number"
        elif text == text:
            nno = text[4:]
            mob = f'{nno}'
            response = "CON The receiver is " + mob + "\n"
            response += "Amount"
        elif text == text + mob:
            print(text)
            response = "END Hello " + text
        elif text == '3':
            number = mobile
            response = "This is your phone number " + phoneNumber
        return HttpResponse(response)
