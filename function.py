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
import datetime
import time
from monify import *


mon = Monnify()


class Main:

    def CheckUser(self, mobile):
        if User.objects.filter(mobile=mobile).exists() == True:
            return True
        else:
            return False

            
    def Signup(self, mobile, pwd, role):
        res = mon.ReserveAccount(mobile)
        
        status = res[1]
        if status == True:
            accountNumber = res[0]['accountNumber']
            bankName = res[0]['bankName']

            user = User.objects.create_user(email="", mobile=mobile, password=pwd, role=role)
            wal = Wallet(mobile=mobile, acctno=accountNumber, bank=bankName)
            pin = Pins(mobile=mobile, pin=pwd)
            user.save()
            wal.save()
            pin.save()
            pass

        else:
            print(status)
            pass

    
    def GetWalletBall(self, mobile):
        bal = Wallet.objects.all().get(mobile=mobile)
        return bal


    def CreateLog(self, mobile, rmobile, ref, amount, date, status, desc, fee):
        clog = Log(mobile=mobile, rmobile=rmobile, ref=ref, amount=amount, date=date, status=status, desc=desc, fee=fee)
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
