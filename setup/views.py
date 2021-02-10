from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model, authenticate, login as dj_login, logout as s_logout
from django.contrib.auth import user_logged_in
from django.dispatch.dispatcher import receiver
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from api.models import *
from web.models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from setup.settings import EMAIL_FROM
from django.db.models import Sum
import random
import string
import uuid
import datetime
import requests
import json
from django.db.models import Q
from django.http import HttpResponse
from datetime import datetime
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import JsonResponse
User = get_user_model()
from function import *
from .user_function import *
func = Main()
NewFunt = Main()





@require_POST
@csrf_exempt
def confirm(request):
    request_json = request.body.decode('utf-8')
    body = json.loads(request_json)
    amountPaid = body['amountPaid']
    paidOn = body['paidOn']
    desc = body['paymentDescription']
    stat = body['paymentStatus']
    mobile = body['product']['reference']
    ref = body['paymentReference']
    if stat == "PAID":
        NewFunt.UpdateWallet(mobile, amountPaid)
        NewFunt.CreateLog(mobile, mobile, ref, amountPaid, paidOn, stat, desc, fee='0')
        return HttpResponse(request_json, status=200)
    else:
        return HttpResponse(request_json, status=400)


def index(request):
    return render(request, 'index.html')


def landing(request):
    return render(request, 'mobile/landing.html')

def login(request):
    if request.method == 'POST':
        mobile = request.POST['mobile']
        password = request.POST['password']
        resp = func.UserLogin(request, mobile, password)
        return resp
    else:
        return render(request, 'mobile/login.html')

def signup(request):
    return render(request, 'mobile/signup.html')


@login_required(login_url='/login')
def home(request):
    mobile = request.user.mobile
    user_wallet = func.ShowUserWallet(mobile)
    return render(request, 'mobile/home.html',{'user_wallet':user_wallet})


def logout(request):
    resp = func.UserLogout(request)
    return resp