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
                    response += "3. Buy Airtime \n"
                    response += "4. Buy Data \n"
                    response += "5. TV"
                else:
                    response += "0. Register"
            if text == '0':
                response = "CON \n"
                response += "Enter Security PIN"
            elif text == f'0*{step}':
                pins = steps[1]
                res = usd.SignUp(mobile, pins)
                reason = res['reason']
                response = "END " + f'{reason}'
            if text == '1':
                response = "CON Choose account information you want to view \n"
                response += "1. Account Number \n"
                response += "2. Account balance"
            if text == f'1*1':
                resp = usd.CheckBalance(mobile)
                acctno = resp['acctNo']
                bank = resp['bank']
                accountNumber  = f'{acctno}\n {bank}'
                response = "END Your account number is " + accountNumber
            if text == '1*2':
                resp = usd.CheckBalance(mobile)
                bal = resp['bal']
                balance  = f'{bal}'
                response = "END Your balance is " + balance
            if text == '2':
                response = "CON Transaction Type \n"
                response += "1. Send to Wallet \n"
                response += "2. Send to Bank"
            if text == '2*2':
                response = "CON Select Bank\n"
                page = 1
                bnk = usd.GetBank(page)
                for i in bnk['results']:
                    code = i['code']
                    name = i['name']
                    response += f'{code}. {name} \n'
                response += "00. Next"
            if text == f'2*2*{step}':
                response = "CON Select Bank\n"
                page = 2
                bnk = usd.GetBank(page)
                for i in bnk['results']:
                    code = i['code']
                    name = i['name']
                    response += f'{code}. {name} \n'
                response += "00. Next"
            if text == f'2*2*{steps[2]}*{step}':
                response = "CON Select Bank\n"
                page = 3
                bnk = usd.GetBank(page)
                for i in bnk['results']:
                    code = i['code']
                    name = i['name']
                    response += f'{code}. {name} \n'
                response += "00. Next"
            if text == f'2*2*{steps[2]}*{steps[3]}*{step}':
                response = "CON Select Bank\n"
                page = 4
                bnk = usd.GetBank(page)
                for i in bnk['results']:
                    code = i['code']
                    name = i['name']
                    response += f'{code}. {name} \n'
                response += "00. Next"
            elif count == 6 and step != '00':
                # text == f'2*2*{steps[2]}*{steps[3]}*{steps[4]}*{step}' and step is not '00' and count == 6
                print(step)
                response = "CON \n"
                response += "Enter Account Number"
            elif count == 7 and step != '00':
                bnkcode = steps[5]
                acct = step
                vbnk = usd.VerifyBank(acct, bnkcode)
                acctname = vbnk['accountName']
                response = f'CON {acctname} \n'
                response += "Amount"
            elif count == 8 and step != '00':
                bnkcode = steps[5]
                acct = steps[6]
                amt = step
                vbnk = usd.VerifyBank(acct, bnkcode)
                acctname = vbnk['accountName']
                response = f'CON You are sending {amt} to {acctname} \n'
                response += "Enter PIN"
            elif count == 9 and step != '00':
                bnkcode = steps[5]
                acct = steps[6]
                amt = steps[7]
                upin =step
                btransfer = usd.BankTranfer(mobile, amt, acct, bnkcode, upin)
                reason = btransfer['reason']
                response = "END " + f'{reason}'
            elif count == 6 and step == '00':
                response = "CON Select Bank\n"
                page = 5
                bnk = usd.GetBank(page)
                for i in bnk['results']:
                    code = i['code']
                    name = i['name']
                    response += f'{code}. {name} \n'
                response += "99. Back"
            elif text == f'2*2*{steps[2]}*{steps[3]}*{steps[4]}*{steps[5]}*{step}':
                response = "CON \n"
                response += "Enter Account Number"
            elif text == f'2*2*{steps[2]}*{steps[3]}*{steps[4]}*{steps[5]}*{steps[6]}*{step}':
                bnkcode = steps[6]
                acct = step
                vbnk = usd.VerifyBank(acct, bnkcode)
                acctname = vbnk['accountName']
                response = f'CON {acctname} \n'
                response += "Amount"
            elif text == f'2*2*{steps[2]}*{steps[3]}*{steps[4]}*{steps[5]}*{steps[6]}*{steps[7]}*{step}':
                bnkcode = steps[6]
                acct = steps[7]
                amt = step
                vbnk = usd.VerifyBank(acct, bnkcode)
                acctname = vbnk['accountName']
                response = f'CON You are sending {amt} to {acctname} \n'
                response += "Enter PIN"
            elif text == f'2*2*{steps[2]}*{steps[3]}*{steps[4]}*{steps[5]}*{steps[6]}*{steps[7]}*{steps[8]}*{step}':
                bnkcode = steps[6]
                acct = steps[7]
                amt = steps[8]
                upin =step
                btransfer = usd.BankTranfer(mobile, amt, acct, bnkcode, upin)
                reason = btransfer['reason']
                response = "END " + f'{reason}'
            if text == '2*1':
                response = "CON \n"
                response += "Enter Reciever Number"
            if text == f'2*1*{step}':
                print(text)
                nno = text[4:]
                mob = f'{nno}'
                response = "CON \n"
                response += "Amount"
            if text == f'2*1*{steps[2]}*{step}':
                response = "CON \n"
                response += "PIN"
            if text == f'2*1*{steps[2]}*{steps[3]}*{step}':
                rec = steps[2]
                amt = steps[3]
                pin = steps[4]
                rep = usd.SendMoney(amt, rec, pin, mobile)
                reason = rep['reason']
                response = "END " + f'{reason}'
            return HttpResponse(response)
        except:
            return HttpResponse(response)
