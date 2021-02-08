from typing import Text
from django.shortcuts import render
import json
import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from function import *
from getbank import *
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
                    response += "3. Bank Transfer \n"
                    response += "4. Buy Airtime \n"
                    response += "5. Buy Data \n"
                    response += "6. Pay Bills \n"
                    response += "7. WebPay (soon) \n"
                else:
                    response += "99. Register"
                
            elif text == '1':
                response  = "CON \n"
                response += "1. Balance \n"
                response += "2. Account Number \n"
            elif text == '1*1':
                resp = usd.CheckBalance(mobile)
                if resp['code'] == 200:
                    bal = resp['bal']
                    response = "END Account Balance\n" + bal
                else:
                    reason = resp['reason']
                    response = "END " + reason
            elif text == '1*2':
                resp = usd.CheckBalance(mobile)
                if resp['code'] == 200:
                    acctNo = resp['acctNo']
                    bank = resp['bank']
                    response = "END Account Details\n" + f'{acctNo} \n {bank}'
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
            elif text == '3':
                response  = "CON \n"
                response += "Enter Account Number \n"
                
            elif steps[0] == '3' and count == 2:
                response  = "CON Select Bank\n"
                acctNo = steps[1]
                if acctNo == '':
                    response = "END Please Enter Account"
                else:
                    banks = GetLikeBank(acctNo)
                    for bnk in banks:
                        code = bnk['code']
                        name = bnk['name']
                        response += f'{code}. {name}\n'
    
            elif steps[0] == '3' and count == 3:
                acno = steps[1]
                bcode = steps[2]
                verify = usd.VerifyBank(acno, bcode)
                status = verify['code']
                if status == 200:
                    acctname = verify['accountName']
                    response  = f'CON {acctname}\n'
                    response += "Enter Amount \n"
                else:
                    reason = verify['reason']
                    response = "END " + reason
                    
            elif steps[0] == '3' and count == 4:
                acno = steps[1]
                bcode = steps[2]
                amt = steps[3]
                if amt == '':
                    response = "END Enter Valid Account"
                else:
                    verify = usd.VerifyBank(acno, bcode)
                    acctname = verify['accountName']
                    response  = f'CON {acctname} - N{amt}\n'
                    response += "Enter PIN \n"
            elif steps[0] == '3' and count == 5:
                acno = steps[1]
                bcode = steps[2]
                amt = steps[3]
                pins = steps[4]
                btransfer = usd.BankTranfer(mobile, amt, acno, bcode, pins)
                status = btransfer['code']
                verify = usd.VerifyBank(acno, bcode)
                acctname = verify['accountName']
                if status == 200:
                    reason = btransfer['reason']
                    response  = f'CON SUCCESSFUL\n'
                    response = "END " + f'{reason}\n {acctname}'
                else:
                    reason = btransfer['reason']
                    response  = f'CON FAIL\n'
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
            elif steps[0] == '99':
                response  = "CON \n"
                response += "Enter You Personal PIN "
                if steps[0] == '99' and count == 2:
                    pins = steps[1]
                    resp = usd.SignUp(mobile, pins)
                    reason = resp['reason']
                    response = "END " + f'{reason}'
            elif steps[0] == '6':
                response  = "CON \n"
                response += "1. Buy Power \n"
                response += "2. TV \n"
                if steps[0] == '6' and steps[1] == '1':
                    response  = "CON \n"
                    response += "1. Ikeja Electric \n"
                    response += "2. Eko Electric \n"
                    response += "3. Kano Electric \n"
                    response += "4. P.Harcourt Electric \n"
                    response += "5. Ibadan Electric \n"
                    response += "6. Kaduna Electric \n"
                    response += "7. Abuja Electric \n"
                    if steps[0] == '6' and steps[1] == '1' and steps[2] == '1':
                        response  = "CON \n"
                        response += "1. Postpaid \n"
                        response += "2. Prepaid \n"
                        if steps[0] == '6' and steps[1] == '1' and steps[2] == '1' and steps[3] == '1':
                            response  = "CON \n"
                            response += "Enter Meter NO "
                            if steps[0] == '6' and steps[1] == '1' and steps[2] == '1' and steps[3] == '1' and count == 5:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='ikeja-electric', serviceType='postpaid', meterNumber=f'{meterNumber}')
                                if resp['status'] == 200:
                                    customerName = resp['customerName']
                                    response  = f'CON {customerName}\n'
                                    response += "Enter Amount "
                                else:
                                    ends = resp['data']['message']
                                    response = f'END {ends}'
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '1' and steps[3] == '1' and count == 6:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='ikeja-electric', serviceType='postpaid', meterNumber=f'{meterNumber}')
                                customerName = resp['customerName']
                                response  = f'CON {customerName}\n'
                                response += "Enter PIN "
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '1' and steps[3] == '1' and count == 7:
                                meterNumber = steps[4]
                                amount = steps[5]
                                pin = step
                                resp = usd.PayPower(mobile, variation_code='postpaid', serviceID='ikeja-electric', amount=f'{amount}', meterNumber=f'{meterNumber}', pin=f'{pin}')
                                reas = resp['reason']
                                response = f'END {reas}'
                        elif steps[0] == '6' and steps[1] == '1' and steps[2] == '1' and steps[3] == '2':
                            response  = "CON \n"
                            response += "Enter Meter NO "
                            if steps[0] == '6' and steps[1] == '1' and steps[2] == '1' and steps[3] == '2' and count == 5:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='ikeja-electric', serviceType='prepaid', meterNumber=f'{meterNumber}')
                                if resp['status'] == 200:
                                    customerName = resp['customerName']
                                    response  = f'CON {customerName}\n'
                                    response += "Enter Amount "
                                else:
                                    ends = resp['data']['message']
                                    response = f'END {ends}'
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '1' and steps[3] == '2' and count == 6:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='ikeja-electric', serviceType='prepaid', meterNumber=f'{meterNumber}')
                                customerName = resp['customerName']
                                response  = f'CON {customerName}\n'
                                response += "Enter PIN "
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '1' and steps[3] == '2' and count == 7:
                                meterNumber = steps[4]
                                amount = steps[5]
                                pin = step
                                resp = usd.PayPower(mobile, variation_code='prepaid', serviceID='ikeja-electric', amount=f'{amount}', meterNumber=f'{meterNumber}', pin=f'{pin}')
                                reas = resp['reason']
                                response = f'END {reas}'
                    
                    elif steps[0] == '6' and steps[1] == '1' and steps[2] == '2':
                        response  = "CON \n"
                        response += "1. Postpaid \n"
                        response += "2. Prepaid \n"
                        if steps[0] == '6' and steps[1] == '1' and steps[2] == '2' and steps[3] == '1':
                            response  = "CON \n"
                            response += "Enter Meter NO "
                            if steps[0] == '6' and steps[1] == '1' and steps[2] == '2' and steps[3] == '1' and count == 5:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='eko-electric', serviceType='postpaid', meterNumber=f'{meterNumber}')
                                if resp['status'] == 200:
                                    customerName = resp['customerName']
                                    response  = f'CON {customerName}\n'
                                    response += "Enter Amount "
                                else:
                                    ends = resp['data']['message']
                                    response = f'END {ends}'
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '2' and steps[3] == '1' and count == 6:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='eko-electric', serviceType='postpaid', meterNumber=f'{meterNumber}')
                                customerName = resp['customerName']
                                response  = f'CON {customerName}\n'
                                response += "Enter PIN "
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '2' and steps[3] == '1' and count == 7:
                                meterNumber = steps[4]
                                amount = steps[5]
                                pin = step
                                resp = usd.PayPower(mobile, variation_code='postpaid', serviceID='eko-electric', amount=f'{amount}', meterNumber=f'{meterNumber}', pin=f'{pin}')
                                reas = resp['reason']
                                response = f'END {reas}'

                        elif steps[0] == '6' and steps[1] == '1' and steps[2] == '2' and steps[3] == '2':
                            response  = "CON \n"
                            response += "Enter Meter NO "
                            if steps[0] == '6' and steps[1] == '1' and steps[2] == '2' and steps[3] == '2' and count == 5:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='eko-electric', serviceType='prepaid', meterNumber=f'{meterNumber}')
                                if resp['status'] == 200:
                                    customerName = resp['customerName']
                                    response  = f'CON {customerName}\n'
                                    response += "Enter Amount "
                                else:
                                    ends = resp['data']['message']
                                    response = f'END {ends}'
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '2' and steps[3] == '2' and count == 6:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='eko-electric', serviceType='prepaid', meterNumber=f'{meterNumber}')
                                customerName = resp['customerName']
                                response  = f'CON {customerName}\n'
                                response += "Enter PIN "
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '2' and steps[3] == '2' and count == 7:
                                meterNumber = steps[4]
                                amount = steps[5]
                                pin = step
                                resp = usd.PayPower(mobile, variation_code='prepaid', serviceID='eko-electric', amount=f'{amount}', meterNumber=f'{meterNumber}', pin=f'{pin}')
                                reas = resp['reason']
                                response = f'END {reas}'

                    elif steps[0] == '6' and steps[1] == '1' and steps[2] == '3':
                        response  = "CON \n"
                        response += "1. Postpaid \n"
                        response += "2. Prepaid \n"
                        if steps[0] == '6' and steps[1] == '1' and steps[2] == '3' and steps[3] == '1':
                            response  = "CON \n"
                            response += "Enter Meter NO "
                            if steps[0] == '6' and steps[1] == '1' and steps[2] == '3' and steps[3] == '1' and count == 5:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='kano-electric', serviceType='postpaid', meterNumber=f'{meterNumber}')
                                if resp['status'] == 200:
                                    customerName = resp['customerName']
                                    response  = f'CON {customerName}\n'
                                    response += "Enter Amount "
                                else:
                                    ends = resp['data']['message']
                                    response = f'END {ends}'
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '3' and steps[3] == '1' and count == 6:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='kano-electric', serviceType='postpaid', meterNumber=f'{meterNumber}')
                                customerName = resp['customerName']
                                response  = f'CON {customerName}\n'
                                response += "Enter PIN "
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '3' and steps[3] == '1' and count == 7:
                                meterNumber = steps[4]
                                amount = steps[5]
                                pin = step
                                resp = usd.PayPower(mobile, variation_code='postpaid', serviceID='kano-electric', amount=f'{amount}', meterNumber=f'{meterNumber}', pin=f'{pin}')
                                reas = resp['reason']
                                response = f'END {reas}'

                        elif steps[0] == '6' and steps[1] == '1' and steps[2] == '3' and steps[3] == '2':
                            response  = "CON \n"
                            response += "Enter Meter NO "
                            if steps[0] == '6' and steps[1] == '1' and steps[2] == '3' and steps[3] == '2' and count == 5:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='kano-electric', serviceType='prepaid', meterNumber=f'{meterNumber}')
                                if resp['status'] == 200:
                                    customerName = resp['customerName']
                                    response  = f'CON {customerName}\n'
                                    response += "Enter Amount "
                                else:
                                    ends = resp['data']['message']
                                    response = f'END {ends}'
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '3' and steps[3] == '2' and count == 6:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='kano-electric', serviceType='prepaid', meterNumber=f'{meterNumber}')
                                customerName = resp['customerName']
                                response  = f'CON {customerName}\n'
                                response += "Enter PIN "
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '3' and steps[3] == '2' and count == 7:
                                meterNumber = steps[4]
                                amount = steps[5]
                                pin = step
                                resp = usd.PayPower(mobile, variation_code='prepaid', serviceID='kano-electric', amount=f'{amount}', meterNumber=f'{meterNumber}', pin=f'{pin}')
                                reas = resp['reason']
                                response = f'END {reas}'

                    elif steps[0] == '6' and steps[1] == '1' and steps[2] == '4':
                        response  = "CON \n"
                        response += "1. Postpaid \n"
                        response += "2. Prepaid \n"
                        if steps[0] == '6' and steps[1] == '1' and steps[2] == '4' and steps[3] == '1':
                            response  = "CON \n"
                            response += "Enter Meter NO "
                            if steps[0] == '6' and steps[1] == '1' and steps[2] == '4' and steps[3] == '1' and count == 5:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='portharcourt-electric', serviceType='postpaid', meterNumber=f'{meterNumber}')
                                if resp['status'] == 200:
                                    customerName = resp['customerName']
                                    response  = f'CON {customerName}\n'
                                    response += "Enter Amount "
                                else:
                                    ends = resp['data']['message']
                                    response = f'END {ends}'
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '4' and steps[3] == '1' and count == 6:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='portharcourt-electric', serviceType='postpaid', meterNumber=f'{meterNumber}')
                                customerName = resp['customerName']
                                response  = f'CON {customerName}\n'
                                response += "Enter PIN "
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '4' and steps[3] == '1' and count == 7:
                                meterNumber = steps[4]
                                amount = steps[5]
                                pin = step
                                resp = usd.PayPower(mobile, variation_code='postpaid', serviceID='portharcourt-electric', amount=f'{amount}', meterNumber=f'{meterNumber}', pin=f'{pin}')
                                reas = resp['reason']
                                response = f'END {reas}'

                        elif steps[0] == '6' and steps[1] == '1' and steps[2] == '4' and steps[3] == '2':
                            response  = "CON \n"
                            response += "Enter Meter NO "
                            if steps[0] == '6' and steps[1] == '1' and steps[2] == '4' and steps[3] == '2' and count == 5:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='portharcourt-electric', serviceType='prepaid', meterNumber=f'{meterNumber}')
                                if resp['status'] == 200:
                                    customerName = resp['customerName']
                                    response  = f'CON {customerName}\n'
                                    response += "Enter Amount "
                                else:
                                    ends = resp['data']['message']
                                    response = f'END {ends}'
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '4' and steps[3] == '2' and count == 6:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='portharcourt-electric', serviceType='prepaid', meterNumber=f'{meterNumber}')
                                customerName = resp['customerName']
                                response  = f'CON {customerName}\n'
                                response += "Enter PIN "
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '4' and steps[3] == '2' and count == 7:
                                meterNumber = steps[4]
                                amount = steps[5]
                                pin = step
                                resp = usd.PayPower(mobile, variation_code='prepaid', serviceID='portharcourt-electric', amount=f'{amount}', meterNumber=f'{meterNumber}', pin=f'{pin}')
                                reas = resp['reason']
                                response = f'END {reas}'

                    elif steps[0] == '6' and steps[1] == '1' and steps[2] == '5':
                        response  = "CON \n"
                        response += "1. Postpaid \n"
                        response += "2. Prepaid \n"
                        if steps[0] == '6' and steps[1] == '1' and steps[2] == '5' and steps[3] == '1':
                            response  = "CON \n"
                            response += "Enter Meter NO "
                            if steps[0] == '6' and steps[1] == '1' and steps[2] == '5' and steps[3] == '1' and count == 5:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='ibadan-electric', serviceType='postpaid', meterNumber=f'{meterNumber}')
                                if resp['status'] == 200:
                                    customerName = resp['customerName']
                                    response  = f'CON {customerName}\n'
                                    response += "Enter Amount "
                                else:
                                    ends = resp['data']['message']
                                    response = f'END {ends}'
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '5' and steps[3] == '1' and count == 6:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='ibadan-electric', serviceType='postpaid', meterNumber=f'{meterNumber}')
                                customerName = resp['customerName']
                                response  = f'CON {customerName}\n'
                                response += "Enter PIN "
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '5' and steps[3] == '1' and count == 7:
                                meterNumber = steps[4]
                                amount = steps[5]
                                pin = step
                                resp = usd.PayPower(mobile, variation_code='postpaid', serviceID='ibadan-electric', amount=f'{amount}', meterNumber=f'{meterNumber}', pin=f'{pin}')
                                reas = resp['reason']
                                response = f'END {reas}'

                        elif steps[0] == '6' and steps[1] == '1' and steps[2] == '5' and steps[3] == '2':
                            response  = "CON \n"
                            response += "Enter Meter NO "
                            if steps[0] == '6' and steps[1] == '1' and steps[2] == '5' and steps[3] == '2' and count == 5:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='ibadan-electric', serviceType='prepaid', meterNumber=f'{meterNumber}')
                                if resp['status'] == 200:
                                    customerName = resp['customerName']
                                    response  = f'CON {customerName}\n'
                                    response += "Enter Amount "
                                else:
                                    ends = resp['data']['message']
                                    response = f'END {ends}'
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '5' and steps[3] == '2' and count == 6:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='ibadan-electric', serviceType='prepaid', meterNumber=f'{meterNumber}')
                                customerName = resp['customerName']
                                response  = f'CON {customerName}\n'
                                response += "Enter PIN "
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '5' and steps[3] == '2' and count == 7:
                                meterNumber = steps[4]
                                amount = steps[5]
                                pin = step
                                resp = usd.PayPower(mobile, variation_code='prepaid', serviceID='ibadan-electric', amount=f'{amount}', meterNumber=f'{meterNumber}', pin=f'{pin}')
                                reas = resp['reason']
                                response = f'END {reas}'

                    elif steps[0] == '6' and steps[1] == '1' and steps[2] == '6':
                        response  = "CON \n"
                        response += "1. Postpaid \n"
                        response += "2. Prepaid \n"
                        if steps[0] == '6' and steps[1] == '1' and steps[2] == '6' and steps[3] == '1':
                            response  = "CON \n"
                            response += "Enter Meter NO "
                            if steps[0] == '6' and steps[1] == '1' and steps[2] == '6' and steps[3] == '1' and count == 5:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='kaduna-electric', serviceType='postpaid', meterNumber=f'{meterNumber}')
                                if resp['status'] == 200:
                                    customerName = resp['customerName']
                                    response  = f'CON {customerName}\n'
                                    response += "Enter Amount "
                                else:
                                    ends = resp['data']['message']
                                    response = f'END {ends}'
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '6' and steps[3] == '1' and count == 6:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='kaduna-electric', serviceType='postpaid', meterNumber=f'{meterNumber}')
                                customerName = resp['customerName']
                                response  = f'CON {customerName}\n'
                                response += "Enter PIN "
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '6' and steps[3] == '1' and count == 7:
                                meterNumber = steps[4]
                                amount = steps[5]
                                pin = step
                                resp = usd.PayPower(mobile, variation_code='postpaid', serviceID='kaduna-electric', amount=f'{amount}', meterNumber=f'{meterNumber}', pin=f'{pin}')
                                reas = resp['reason']
                                response = f'END {reas}'

                        elif steps[0] == '6' and steps[1] == '1' and steps[2] == '6' and steps[3] == '2':
                            response  = "CON \n"
                            response += "Enter Meter NO "
                            if steps[0] == '6' and steps[1] == '1' and steps[2] == '6' and steps[3] == '2' and count == 5:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='kaduna-electric', serviceType='prepaid', meterNumber=f'{meterNumber}')
                                if resp['status'] == 200:
                                    customerName = resp['customerName']
                                    response  = f'CON {customerName}\n'
                                    response += "Enter Amount "
                                else:
                                    ends = resp['data']['message']
                                    response = f'END {ends}'
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '6' and steps[3] == '2' and count == 6:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='kaduna-electric', serviceType='prepaid', meterNumber=f'{meterNumber}')
                                customerName = resp['customerName']
                                response  = f'CON {customerName}\n'
                                response += "Enter PIN "
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '6' and steps[3] == '2' and count == 7:
                                meterNumber = steps[4]
                                amount = steps[5]
                                pin = step
                                resp = usd.PayPower(mobile, variation_code='prepaid', serviceID='kaduna-electric', amount=f'{amount}', meterNumber=f'{meterNumber}', pin=f'{pin}')
                                reas = resp['reason']
                                response = f'END {reas}'

                    elif steps[0] == '6' and steps[1] == '1' and steps[2] == '7':
                        response  = "CON \n"
                        response += "1. Postpaid \n"
                        response += "2. Prepaid \n"
                        if steps[0] == '6' and steps[1] == '1' and steps[2] == '7' and steps[3] == '1':
                            response  = "CON \n"
                            response += "Enter Meter NO "
                            if steps[0] == '6' and steps[1] == '1' and steps[2] == '7' and steps[3] == '1' and count == 5:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='abuja-electric', serviceType='postpaid', meterNumber=f'{meterNumber}')
                                if resp['status'] == 200:
                                    customerName = resp['customerName']
                                    response  = f'CON {customerName}\n'
                                    response += "Enter Amount "
                                else:
                                    ends = resp['data']['message']
                                    response = f'END {ends}'
                                response += "Enter Amount "
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '7' and steps[3] == '1' and count == 6:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='abuja-electric', serviceType='postpaid', meterNumber=f'{meterNumber}')
                                customerName = resp['customerName']
                                response  = f'CON {customerName}\n'
                                response += "Enter PIN "
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '7' and steps[3] == '1' and count == 7:
                                meterNumber = steps[4]
                                amount = steps[5]
                                pin = step
                                resp = usd.PayPower(mobile, variation_code='postpaid', serviceID='abuja-electric', amount=f'{amount}', meterNumber=f'{meterNumber}', pin=f'{pin}')
                                reas = resp['reason']
                                response = f'END {reas}'

                        elif steps[0] == '6' and steps[1] == '1' and steps[2] == '7' and steps[3] == '2':
                            response  = "CON \n"
                            response += "Enter Meter NO "
                            if steps[0] == '6' and steps[1] == '1' and steps[2] == '7' and steps[3] == '2' and count == 5:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='abuja-electric', serviceType='prepaid', meterNumber=f'{meterNumber}')
                                if resp['status'] == 200:
                                    customerName = resp['customerName']
                                    response  = f'CON {customerName}\n'
                                    response += "Enter Amount "
                                else:
                                    ends = resp['data']['message']
                                    response = f'END {ends}'
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '7' and steps[3] == '2' and count == 6:
                                meterNumber = steps[4]
                                resp = usd.VerifyPower(serviceID='abuja-electric', serviceType='prepaid', meterNumber=f'{meterNumber}')
                                customerName = resp['customerName']
                                response  = f'CON {customerName}\n'
                                response += "Enter PIN "
                            elif steps[0] == '6' and steps[1] == '1' and steps[2] == '7' and steps[3] == '2' and count == 7:
                                meterNumber = steps[4]
                                amount = steps[5]
                                pin = step
                                resp = usd.PayPower(mobile, variation_code='prepaid', serviceID='abuja-electric', amount=f'{amount}', meterNumber=f'{meterNumber}', pin=f'{pin}')
                                reas = resp['reason']
                                response = f'END {reas}'

                    else:
                        response = "END Invalid Option"
                else:
                        response = "END Invalid Option"
            elif steps[0] == '7':
                response = "END Web Payment\n Coming Soon"
                    
            elif steps[0] != '1' or steps[0] != '2' or steps[0] != '3' or steps[0] != '4' or steps[0] != '5' or steps[0] != '6' or steps[0] != '7' or steps[0] != '99':
                response = "END Invalid Operation Number"
            return HttpResponse(response)
        except:
            return HttpResponse(response)
