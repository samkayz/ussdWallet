from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from web.models import *
from setup.settings import EMAIL_FROM
import random
import string
import uuid
import datetime
from django.utils import timezone
from datetime import timedelta
from . models import *
from function import *
funct = Main()
from random import randint

refid = uuid.uuid4().hex
P = 6
paycode = ''.join(random.choices(string.digits, k=P))

def save_token(amount, apikey, desc):
    tok = PayToken(paycode=paycode, token=refid, amount=amount, apikey=apikey, desc=desc)
    tok.save()
    pass
__name__ == "__main__"


@csrf_exempt
def initiate(request):
    if request.method == "POST":
        apikey = request.POST['apikey']
        amount = request.POST['amount']
        desc = request.POST['desc']
        save_token(amount, apikey, desc)
        return redirect(f'final/{refid}')


def final(request, token):
    time_now = timezone.now()
    alltoken = get_object_or_404(PayToken, token=token)
    merch_name = funct.GetMerchantName(alltoken.apikey)
    left = alltoken.datetime - (time_now - timedelta(minutes=20))
    seconds_in_day = 24 * 60 * 60
    lefts = int(divmod(left.days * seconds_in_day + left.seconds, 60)[0])
    seconds = int(divmod(left.days * seconds_in_day + left.seconds, 60)[1])
    print(seconds)
    timelefts = int((lefts * 60) / 10 )
    
    sec = timelefts * 10 
    
    secs = sec % 60
    print(secs)
    ## Check if payment has been made successfully
    if alltoken.status == True and alltoken.paid == True:
        msg = "Payment has been paid"
        return render(request, 'pay/response.html', {'msg':msg})
    
    ## Check if the token have expired or payment have been terminated
    elif alltoken.status == True and alltoken.paid == False:
        msg = "Time Expired"
        return render(request, 'pay/response.html', {'msg':msg})
    
    ### Check if the Time for To make the payment have elapses
    elif alltoken.datetime <= (time_now - timedelta(minutes=20)) or lefts == 0:
        update_status = PayToken.objects.filter(token=token)
        update_status.update(status=True)
        msg = "Time Expired"
        return render(request, 'pay/response.html', {'msg':msg})
    
    else:
        return render(request, 'pay/index.html', {'paycode': alltoken.paycode, 'amount':alltoken.amount, 
                                              'desc': alltoken.desc, 'merch_name':merch_name, 
                                              'timelefts': timelefts, 'sec':seconds, 'tok':token})