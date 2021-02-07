from django.core import paginator
from django.shortcuts import render
from function import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from web.models import *
from rest_framework import status
from rest_framework.response import Response
import random
from .serializers import *
import string
from datetime import datetime
from monify import *
from utility import *

# Create your views here.
MyClass = Main()
User = get_user_model()
mon = Monnify()
uti = Utility()

ex = 100

@api_view(['GET'])
@permission_classes([])
def Check(request, mobile):
    resp = MyClass.CheckUser(mobile)
    data = {
        "code": status.HTTP_200_OK,
        "status": "success",
        "reason": resp
    }
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([])
def signup(request):
    mobile = request.data.get('mobile')
    pwd = request.data.get('pwd')
    role = request.data.get('role')

    if User.objects.filter(mobile=mobile).exists():
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Mobile number is a register member"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    elif len(mobile) > 11 or len(mobile) < 11:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Wrong Mobile Number Format"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    elif mobile[0] != '0':
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Wrong Mobile Number Formats"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    elif len(pwd) > 4:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Pin Can't be more than 4 digit"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    else:
        MyClass.Signup(mobile, pwd, role)
        data = {
            "code": status.HTTP_200_OK,
            "status": "success",
            "reason": "Account created"
        }
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([])
def account(request, mobile):
    try:
        bal = MyClass.GetWalletBall(mobile)

        data = {
            "code": status.HTTP_200_OK,
            "bal": f'{bal.bal}',
            "acctNo": f'{bal.acctno}',
            "bank": f'{bal.bank}'
        }
        return Response(data=data, status=status.HTTP_200_OK)
    
    except:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Account doestn't exist within the system"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([])
def transfer(request, mobile):
    U = 6
    res = ''.join(random.choices(string.digits, k=U))
    txn = str(res)
    txt_id = "TX" + txn
    base_date_time = datetime.now()
    now = (datetime.strftime(base_date_time, "%Y-%m-%d %H:%M %p"))
    amount = request.data.get('amount')
    rec = request.data.get('reciever')
    pin = request.data.get('pin')
    checkPin = MyClass.CheckPin(mobile, pin)
    if checkPin == True:
        checkbal = MyClass.CheckBal(mobile, amount)
        if checkbal == True:
            if User.objects.filter(mobile=rec).exists():
                if mobile == rec:
                    data = {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "status": "fail",
                        "reason": "You can't send money to yourself"
                    }
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
                else:
                    amt = float(amount)
                    MyClass.SendMoney(amount, mobile, rec)
                    MyClass.DebitSMS(mobile, rec, amt, txt_id)
                    MyClass.CreditSMS(mobile, rec, amt, txt_id)
                    MyClass.CreateLog(mobile, rec, txt_id, amt, now, status="PAID", desc="Wallet Transfer", fee=0)
                    data = {
                        "code": status.HTTP_200_OK,
                        "status": "success",
                        "reason": f'{amt} was sent to {rec}'
                    }
                    return Response(data=data, status=status.HTTP_200_OK)
            else:
                data = {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "status": "fail",
                    "reason": "User not found"
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            data = {
                "code": status.HTTP_400_BAD_REQUEST,
                "status": "fail",
                "reason": "Insufficient balance"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Invalid Transaction Pin"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([])
def accountVerify(request):
    acctno = request.data.get('accountNumber')
    bcode = request.data.get('bankCode')

    verify = mon.VerifyAccount(acctno, bcode)
    stat = verify['requestSuccessful']
    if stat == True:
        body = verify['responseBody']
        acct = body['accountNumber']
        acctname = body['accountName']
        bankCode = body['bankCode']

        data = {
            "code": status.HTTP_200_OK,
            "status": "success",
            "accountNumber": acct,
            "accountName": acctname,
            "bankCode": bankCode,

        }
        return Response(data=data, status=status.HTTP_200_OK)
    
    else:
        msg = verify['responseMessage']
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": msg
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([])
def btranfer(request, mobile):
    U = 6
    res = ''.join(random.choices(string.digits, k=U))
    txn = str(res)
    txt_id = "TX" + txn
    base_date_time = datetime.now()
    now = (datetime.strftime(base_date_time, "%Y-%m-%d %H:%M %p"))
    amount = request.data.get('amount')
    rec = request.data.get('accountNumber')
    bcode = request.data.get('bankCode')
    pin = request.data.get('pin')
    desc = "USSD"
    stat = "PAID"
    checkPin = MyClass.CheckPin(mobile, pin)
    if User.objects.filter(mobile=mobile).exists() == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Account doestn't exist within the system"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    elif checkPin == True:
        ammt = (float(ex) + float(amount))
        checkbal = MyClass.CheckBal(mobile, ammt)
        if checkbal == True:
            trans = mon.BankTransfer(amount, txt_id, desc, bcode, rec )
            statrep = trans['requestSuccessful']
            if statrep == True:
                body = trans['responseBody']
                fee = float(body['totalFee'])
                amt = (fee + float(amount))
                MyClass.BankTransfer(mobile, amt)
                MyClass.DebitSMS(mobile, rec, amount, txt_id)
                MyClass.CreateLog(mobile, rec, txt_id, amount, now, stat, desc, fee)
                data = {
                    "code": status.HTTP_200_OK,
                    "status": "sucess",
                    "amount": amount,
                    "fee": fee,
                    "reason": f'You have sent {float(amount)} to {rec}'
                }
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                msg = trans['responseMessage']
                data = {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "status": "fail",
                    "reason": msg
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        else:
            data = {
                "code": status.HTTP_400_BAD_REQUEST,
                "status": "fail",
                "reason": "Insufficient balance"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Invalid Transaction Pin"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([])
def getData(request, scode):
    try:
        snippet = MyClass.GetUtility(scode)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    serializer = UtilitySerializers(instance=snippet, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([])
def getBank(request):
    try:
        snippet = MyClass.GetBank()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    paginator = PageNumberPagination()
    paginator.page_size = 5
    result_page = paginator.paginate_queryset(snippet, request)
    serializer = BankSerializers(instance=result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([])
def buyAirtime(request, mobile):
    base_date_time = datetime.now()
    now = (datetime.strftime(base_date_time, "%Y-%m-%d %H:%M %p"))
    network = request.data.get('network')
    recmobile = request.data.get('number')
    amount = request.data.get('amount')
    pin = request.data.get('pin')
    checkPin = MyClass.CheckPin(mobile, pin)
    if User.objects.filter(mobile=mobile).exists() == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Account doestn't exist within the system"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    elif checkPin == True:
        checkbal = MyClass.CheckBal(mobile, amount)
        if checkbal == True:
            buy = uti.buy_airtime(network, amount, recmobile)
            stat = buy['content']['transactions']['status']
            if stat == 'delivered':
                MyClass.BankTransfer(mobile, amount)
                body = buy['content']['transactions']
                tid = body['transactionId']
                amt = body['unit_price']
                rstat = "PAID"

                txt_id = f'{tid}'
                desc = body['product_name']
                rmobile = body['unique_element']
                MyClass.DebitSMS(mobile, rmobile, amount, txt_id)
                MyClass.CreateLog(mobile, rmobile, txt_id, amt, now, rstat, desc, fee=0)
                data = {
                    "code": status.HTTP_200_OK,
                    "status": "success",
                    "amount": amount,
                    "fee": 0,
                    "reason": f'You have sent {float(amount)} to {rmobile}'
                }
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                data = {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "status": "fail",
                    "reason": "Transaction fail"
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        else:
            data = {
                "code": status.HTTP_400_BAD_REQUEST,
                "status": "fail",
                "reason": "Insufficient balance"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Invalid Transaction Pin"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([])
def VerifyTv(request):
    cardNo = request.data.get('cardNumber')
    biller = request.data.get('biller')
    tv_resp = uti.tvVerify(cardNo, biller)
    bill = "startimes"
    if int(cardNo) or cardNo in tv_resp.values():
        cus_name = tv_resp['Customer_Name']
        #print(sno in tv_resp.values())
        if biller == bill:
            cus_id = tv_resp['Smartcard_Number']
            show = Utility.objects.filter(service_id=biller)

            data = {
                
                "status": status.HTTP_200_OK,
                "customerName": cus_name,
                "cardNumber": cardNo,
                "customerID": cus_id,
            }
            return Response(data=data, status=status.HTTP_200_OK)
        elif cus_name in tv_resp.values():
            cus_id = tv_resp['Customer_ID']
            data = {
                "status": status.HTTP_200_OK,
                "customerName": cus_name,
                "cardNumber": cardNo,
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            error = {
            "status": status.HTTP_400_BAD_REQUEST,
            "data": {
                "message": "Error"
            }
        }
        return Response(data=error, status=status.HTTP_400_BAD_REQUEST)
    else:
        error = {
            "status": status.HTTP_400_BAD_REQUEST,
            "data": {
                "message": "Invalid Card Number"
            }
        }
        return Response(data=error, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([])
def tvPay(request, mobile):
    charge = 100.0
    U = 6
    res = ''.join(random.choices(string.digits, k=U))
    txn = str(res)
    txt_id = "TX" + txn
    base_date_time = datetime.now()
    now = (datetime.strftime(base_date_time, "%Y-%m-%d %H:%M %p"))
    variation_code = request.data.get('variation_code')
    cardNo = request.data.get('cardNumber')
    pin = request.data.get('pin')

    amount = MyClass.GetTvDetail(variation_code)[0]
    service_id = MyClass.GetTvDetail(variation_code)[1]
    amt = (float(amount) + charge)
    checkPin = MyClass.CheckPin(mobile, pin)
    if User.objects.filter(mobile=mobile).exists() == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Account doestn't exist within the system"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    elif checkPin == True:
        checkbal = MyClass.CheckBal(mobile, amt)
        if checkbal == True:
            tv_resp = uti.PayTV(mobile, amount, variation_code, cardNo, service_id, txt_id)
            statu = tv_resp['status']
            if statu == "delivered":
                MyClass.BankTransfer(mobile, amt)
                p_name = tv_resp['product_name']
                trans_id = tv_resp['transactionId']

                rstat = "PAID"
                
                MyClass.DebitSMS(mobile, cardNo, amount, txt_id)
                MyClass.CreateLog(mobile, cardNo, f'{trans_id}/{txt_id}', amount, now, rstat, p_name, fee=charge)
                data = {
                    "code": status.HTTP_200_OK,
                    "status": "success",
                    "amount": amount,
                    "fee": 0,
                    "reason": f'You have sent {float(amount)} to {cardNo}'
                }
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                data = {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "status": "fail",
                    "reason": "Transaction fail"
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        else:
            data = {
                "code": status.HTTP_400_BAD_REQUEST,
                "status": "fail",
                "reason": "Insufficient balance"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Invalid Transaction Pin"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([])
def verifyPower(request):
    plan = request.data.get('serviceType')
    service_id = request.data.get('serviceID')
    meterno = request.data.get('meterNumber')

    p_resp = uti.powerVerify(meterno, service_id, plan)

    if 'error' in p_resp:
        error = {
            "status": status.HTTP_400_BAD_REQUEST,
            "data": {
                "message": p_resp['error']
            }
        }
        return Response(data=error, status=status.HTTP_400_BAD_REQUEST)
    else:
        if int(meterno) or meterno in p_resp.values():
            cus_name = p_resp['Customer_Name']
            if service_id == "ibadan-electric" or service_id == "jos-electric" or service_id == "portharcourt-electric":
                cus_name = p_resp['Customer_Name']
                MeterNumber = p_resp['MeterNumber']
                address = p_resp['Address']
                data = {
                    "status": status.HTTP_200_OK,
                    "customerName": cus_name,
                    "MeterNumber": MeterNumber,
                }
                return Response(data=data, status=status.HTTP_200_OK)
            elif p_resp['Customer_Name'] in p_resp.values():
                m_no = p_resp['Meter_Number'] 
                cus_dist = p_resp['Customer_District']
                address = p_resp['Address']
                data = {
                    "status": status.HTTP_200_OK,
                    "customerName": cus_name,
                    "MeterNumber": m_no,
                }
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                error = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": p_resp['error']
                }
                return Response(data=error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([])
def buypower(request, mobile):
    charge = 100.0
    U = 6
    res = ''.join(random.choices(string.digits, k=U))
    txn = str(res)
    txt_id = "TX" + txn
    base_date_time = datetime.now()
    now = (datetime.strftime(base_date_time, "%Y-%m-%d %H:%M %p"))
    plan = request.data.get('variation_code')
    service_id = request.data.get('serviceID')
    amount = request.data.get('amount')
    meterno = request.data.get('meterNumber')
    pin = request.data.get('pin')
    amt = (float(amount) + charge)
    checkPin = MyClass.CheckPin(mobile, pin)
    if User.objects.filter(mobile=mobile).exists() == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Account doestn't exist within the system"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    elif checkPin == True:
        checkbal = MyClass.CheckBal(mobile, amt)
        if checkbal == True:
            f = uti.Buy_Power(txt_id, service_id, meterno, plan, amount, mobile)
            po_resp = f[1]
            statu = po_resp['transactions']['status']
            desc = po_resp['transactions']['product_name']
            tran_id = po_resp['transactions']['transactionId']
            rstat = "PAID"
            if statu == "delivered":
                MyClass.BankTransfer(mobile, amt)
                if plan == "postpaid":
                
                    MyClass.DebitSMS(mobile, meterno, amount, txt_id)
                    MyClass.CreateLog(mobile, meterno, f'{tran_id}/{txt_id}', amount, now, rstat, desc, fee=charge)
                    data = {
                        "code": status.HTTP_200_OK,
                        "status": "success",
                        "amount": amount,
                        "fee": charge,
                        "reason": f'You have sent {float(amount)} to {meterno}'
                    }
                    return Response(data=data, status=status.HTTP_200_OK)
                
                else:
                    MyClass.DebitSMS(mobile, meterno, amount, txt_id)
                    MyClass.CreateLog(mobile, meterno, f'{tran_id}/{txt_id}', amount, now, rstat, desc, fee=charge)
                    code = f[6]
                    et = EToken(mobile=mobile, ref=f'{tran_id}/{txt_id}', token=code)
                    et.save()
                    data = {
                        "code": status.HTTP_200_OK,
                        "status": "success",
                        "amount": amount,
                        "fee": charge,
                        "token": code,
                        "reason": f'You have sent {float(amount)} to {meterno}'
                    }
                    MyClass.SendToken(mobile, code)
                    return Response(data=data, status=status.HTTP_200_OK)
            else:
                error = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": 'fail'
                }
                return Response(data=error, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {
                "code": status.HTTP_400_BAD_REQUEST,
                "status": "fail",
                "reason": "Insufficient balance"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Invalid Transaction Pin"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

            