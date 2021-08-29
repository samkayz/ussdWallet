from django.http import request
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
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
import io
import csv
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.utils.html import strip_tags
from django.db.models import Sum
from setup.settings import EMAIL_FROM





class Main:
    def AdminLogin(self, request, email, password):
        if '@' not in email:
            messages.error(request, 'Not an Email')
            return redirect('/web/')
        user = authenticate(mobile=email, password=password)
        if User.objects.filter(mobile=email, is_superuser=False).exists():
            messages.error(request, 'You are not permitted')
            return redirect('/web/')
        elif user is not None:
            dj_login(request, user)
            request.session.set_expiry(1200)
            response = redirect('/web/home')
            return response
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('/web/')

    def AdminLogout(self, request):
        s_logout(request)
        messages.success(request, "Logout Successfully")
        resp = redirect('/web/')
        return resp

    
    def ShowTransLog(self):
        show = Log.objects.filter()
        return show

    def GetUser(self):
        users = User.objects.filter()
        lists = []
        for i in users:
            datas = {}
            if User.objects.filter(mobile=i.mobile, is_superuser=True): continue
            u = get_object_or_404(Wallet, mobile=i.mobile)
            datas['fullname'] = i.fullname
            datas['mobile'] = i.mobile
            datas['email'] = i.email
            datas['bal'] = u.bal
            datas['bank'] = u.bank
            datas['accountno'] = u.acctno
            datas['is_active'] = i.is_active
            datas['role'] = i.is_merchant
            lists.append(datas)
        return lists
    
    def GetWallet(self):
        wallet = Wallet.objects.filter()
        return wallet