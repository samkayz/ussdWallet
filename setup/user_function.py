from django.http import request
from web.models import *
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
import io
import csv
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.utils.html import strip_tags
from django.db.models import Sum
from setup.settings import EMAIL_FROM
from function import *

NewFunct = Main()





class Main:
    def UserLogin(self, request, mobile, password):
        url = request.get_host()
        if NewFunct.CheckUser(mobile) == True:
            user = authenticate(mobile=mobile, password=password)
            if User.objects.filter(mobile=mobile, is_superuser=True).exists():
                messages.error(request, 'You are not permitted')
                return redirect('/login')
            elif user is not None:
                dj_login(request, user)
                # request.session.set_expiry(1200)
                response = redirect('/home')
                return response
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('/login')
        else:
            messages.error(request, "User does not exist. SignUp here " + f'http://{url}/signup')
            return redirect('/login')

    def UserLogout(self, request):
        s_logout(request)
        messages.success(request, "Logout Successfully")
        resp = redirect('/login')
        return resp

    
    def ShowUserWallet(self, mobile):
        user_wallet = Wallet.objects.all().get(mobile=mobile)
        return user_wallet