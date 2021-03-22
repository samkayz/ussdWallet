from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model, authenticate, login as dj_login, logout as s_logout
from django.contrib.auth import user_logged_in
from django.dispatch.dispatcher import receiver
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from api.models import *
from web.models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.paginator import Paginator
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
from bank.getbanks import *
from monify import *
bnk = GetBank()
func = Main()
NewFunt = Main()
moni = Monnify()




def user_required(login_url=None):
    return user_passes_test(lambda u: u.is_user, login_url=login_url)


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


def login(request):
    if request.user.is_authenticated:
        return redirect('/home')
    if request.method == 'POST':
        mobile = request.POST['mobile']
        password = request.POST['password']
        resp = func.UserLogin(request, mobile, password)
        return resp
    else:
        return render(request, 'signin.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('/home')
    return render(request, 'signup.html')


@user_required(login_url='/login')
def home(request):
    mobile = request.user.mobile
    user_wallet = func.ShowUserWallet(mobile)
    show = func.ShowUserLog(mobile).order_by('-id')[:5]
    return render(request, 'home.html',{'user_wallet':user_wallet, 'show':show})


@user_required(login_url='/login')
def sendmoney(request):
    mobile = request.user.mobile
    user_wallet = func.ShowUserWallet(mobile)
    if request.method == "POST":
        acctno = request.POST['acctno']
        data = bnk.GetLikeBank(accountNumber=acctno)
        # print(data)
        return JsonResponse(data, safe=False)
    return render(request, 'sendmoney.html',{'user_wallet':user_wallet})


@user_required(login_url='/login')
def history(request):
    mobile = request.user.mobile
    user_wallet = func.ShowUserWallet(mobile)
    show = func.ShowUserLog(mobile).order_by('-id')
    paginator = Paginator(show, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'history.html',{'user_wallet':user_wallet, 'show':page_obj})


@user_required(login_url='/login')
def settings(request):
    mobile = request.user.mobile
    user_wallet = func.ShowUserWallet(mobile)
    return render(request, 'settings.html',{'user_wallet':user_wallet})


@user_required(login_url='/login')
def bankverify(request):
    if request.method == "POST":
        banks = request.POST['banks']
        acctno = request.POST['acctno']
        bankinfo = moni.VerifyAccount(acctno, banks)
        try:
            acctNo = bankinfo['responseBody']['accountNumber']
            acctName = bankinfo['responseBody']['accountName']
            data = {
                "fullname": acctName,
                "acctNos": acctNo,
                "fee": f'₦ {30.0}'
                }
            return JsonResponse(data)
        except:
            data = {
                "fullname": "Wrong Account Number",
                "acctNos": "Wrong Account Number",
                "fee": f'₦ {30.0}'
                }
            return JsonResponse(data)


@user_required(login_url='/login')
def walletverify(request):
    user_mobile = request.user.mobile
    if request.method == "POST":
        mobile = request.POST['mobile']
        try:
            alluser = User.objects.all().get(mobile=mobile)
            if alluser.mobile == user_mobile:
                data = {
                    "fullname": "You can't send money to yourself",
                    "acctNos": mobile,
                    "fee": f'₦ {0.0}'
                    }
                return JsonResponse(data)
            else:
                data = {
                    "fullname": alluser.fullname,
                    "acctNos": mobile,
                    "fee": f'₦ {0.0}'
                    }
                return JsonResponse(data)
        except:
            data = {
                    "fullname": "Wrong Wallet ID",
                    "acctNos": mobile,
                    "fee": f'₦ {0.0}'
                    }
            return JsonResponse(data)



def logout(request):
    resp = func.UserLogout(request)
    return resp


def aboutus(request):
    return render(request, 'about.html')


def privacy_policy(request):
    return render(request, 'privacy-policy.html')

def terms_and_condition(request):
    return render(request, 'term-condition.html')