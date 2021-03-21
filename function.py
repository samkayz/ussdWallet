from pay.models import PayToken
from django.dispatch.dispatcher import receiver
from web.models import *
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login as dj_login, logout as s_logout
from django.contrib.auth import user_logged_in
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
User = get_user_model()
import os
import random
import string
import uuid
from datetime import datetime
import time
from sms import *
from monify import *

send_sms = SMS()
mon = Monnify()


class Main:

    def CheckUser(self, mobile):
        if User.objects.filter(mobile=mobile).exists() == True:
            return True
        else:
            return False

            
    def Signup(self, mobile, pwd):
        res = mon.ReserveAccount(mobile)
        
        status = res[1]
        if status == True:
            accountNumber = res[0]['accountNumber']
            bankName = res[0]['bankName']

            user = User.objects.create_user(email="", mobile=mobile, password=pwd, is_user=True)
            wal = Wallet(mobile=mobile, acctno=accountNumber, bank=bankName)
            pin = Pins(mobile=mobile, pin=pwd)
            user.save()
            wal.save()
            pin.save()
            msg = f'Welcome {mobile}, \n\n Your Registration was successful.\n ACCNO: {accountNumber}\n Bank: {bankName}\n PIN: {pwd}\n\n. Thank you.'
            # send_sms.SendSMS(mobile, msg)
            pass

        else:
            print(status)
            pass
        
        
    def MerchantSignup(self, mobile, pwd, fullname, email):
        res = mon.ReserveAccount(mobile)
        
        status = res[1]
        if status == True:
            accountNumber = res[0]['accountNumber']
            bankName = res[0]['bankName']

            user = User.objects.create_user(email=email, mobile=mobile, password=pwd, is_merchant=True, fullname=fullname)
            wal = Wallet(mobile=mobile, acctno=accountNumber, bank=bankName)
            pin = Pins(mobile=mobile, pin=pwd)
            merc = Merchant(mobile=mobile)
            mercKey = MerchantKey(mobile=mobile)
            merc.save()
            mercKey.save()
            user.save()
            wal.save()
            pin.save()
            msg = f'Welcome {fullname}, \n\n Your Registration was successful.\n ACCNO: {accountNumber}\n Bank: {bankName}\n PIN: {pwd}\n\n. Thank you.'
            # send_sms.SendSMS(mobile, msg)
            pass

        else:
            print(status)
            pass

    
    def GetWalletBall(self, mobile):
        bal = Wallet.objects.all().get(mobile=mobile)
        return bal


    def CreateLog(self, mobile, rmobile, ref, txntype, amount, date, status, desc, fee):
        clog = Log(mobile=mobile, rmobile=rmobile, ref=ref, txntype=txntype, amount=amount, date=date, status=status, desc=desc, fee=fee)
        clog.save()
        pass

    def UpdateWallet(self, mobile, amount):
        amt = float(amount)
        prevBal = Wallet.objects.values('bal').get(mobile=mobile)['bal']
        newBal = (amt + prevBal)
        wal = Wallet.objects.filter(mobile=mobile)
        wal.update(bal=newBal)
        pass

    def CheckPin(self, mobile, pin):
        if Pins.objects.filter(mobile=mobile).exists():
            cpin = Pins.objects.values('pin').get(mobile=mobile)['pin']
            if cpin == pin:
                return True
            else:
                return False
        else:
            pass

    def CheckBal(self, mobile, amount):
        amt = float(amount)
        bal = Wallet.objects.values('bal').get(mobile=mobile)['bal']
        if bal >= amt:
            return True
        else:
            return False

    def SendMoney(self, amount, sender, rec):
        amt = float(amount)
        sbal = Wallet.objects.values('bal').get(mobile=sender)['bal']
        rbal = Wallet.objects.values('bal').get(mobile=rec)['bal']

        ##### Update Sender ######
        newSenderBal = sbal - amt
        sendr = Wallet.objects.filter(mobile=sender)
        sendr.update(bal=newSenderBal)

        ##### Update Sender ######
        newrecBal = rbal + amt
        recr = Wallet.objects.filter(mobile=rec)
        recr.update(bal=newrecBal)
        pass


    def BankTransfer(self, mobile, amount):
        amt = float(amount)
        bal = Wallet.objects.values('bal').get(mobile=mobile)['bal']
        newBal = (bal - amt)
        sendr = Wallet.objects.filter(mobile=mobile)
        sendr.update(bal=newBal)
        pass

    def GetUtility(self, scode):
        show = Utility.objects.filter(service_id=scode)
        return show

    def GetBank(self):
        show = Banks.objects.filter()
        return show

    
    def CreditSMS(self, mobile, rec, amt, txid):
        base_date_time = datetime.now()
        now = (datetime.strftime(base_date_time, "%Y-%m-%d %H:%M %p"))
        rbal = Wallet.objects.values('bal').get(mobile=rec)['bal']
        msg = f'{txid}\n Hi {rec}, \n You just receive N{amt} from  {mobile} on {now}.\n Bal: N{rbal} \n\nThank you!'
        send_sms.SendSMS(rec, msg)
        pass

    def DebitSMS(self, mobile, rec, amt, txid):
        base_date_time = datetime.now()
        now = (datetime.strftime(base_date_time, "%Y-%m-%d %H:%M %p"))
        sbal = Wallet.objects.values('bal').get(mobile=mobile)['bal']
        msg = f'{txid}\n Hi {mobile}, \n You just sent N{amt} to  {rec} on {now}.\n Bal: N{sbal} \n\nThank you!'
        send_sms.SendSMS(mobile, msg)
        pass

    def GetTvDetail(self, variation_code):
        amount = Utility.objects.values('variation_amount').get(variation_code=variation_code)['variation_amount']
        service_id = Utility.objects.values('service_id').get(variation_code=variation_code)['service_id']
        return amount, service_id

    def SendToken(self, mobile, token):
        msg = f'Hi {mobile}, \n Here is your electricity token\n\n{token} \n\nThank you!'
        send_sms.SendSMS(mobile, msg)
        pass
    
    
    def GetLog(self, request):
        mobile = request.user.mobile
        show = Log.objects.filter(Q(mobile=mobile) | Q(rmobile=mobile))
        return show
    
    def BusinessDone(self, request):
        mobile = request.user.mobile
        done = Merchant.objects.values('done').get(mobile=mobile)['done']
        return done
    
    def GetBusinessDetails(self, request):
        mobile = request.user.mobile
        allbd = Merchant.objects.all().get(mobile=mobile)
        return allbd
    
    def GetAPIDetails(self, request):
        mobile = request.user.mobile
        api = MerchantKey.objects.all().get(mobile=mobile)
        return api
    
    def GetMerchantName(self, apikey):
        merch_number = MerchantKey.objects.values('mobile').get(Q(live_key=apikey) | Q(test_key=apikey))['mobile']
        merch_name = Merchant.objects.values('bus_name').get(mobile=merch_number)['bus_name']
        return merch_name
    
    def CheckPayCode(self, paycode):
        if PayToken.objects.filter(paycode=paycode).exists():
            return True
        else:
            return False
        
    def CheckLoginUser(self, mobile):
        if User.objects.filter(mobile=mobile).exists():
            return True
        else:
            return False
        
    
    def UpdatePaymentToken(self, paycode):
        token_update = PayToken.objects.filter(paycode=paycode)
        token_update.update(status=True, paid=True)
        pass

    def Notification(self, callback, callback_data):
        response = requests.post(callback, json=callback_data)
        return response