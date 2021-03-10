from django.shortcuts import *
from function import *
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.auth import get_user_model, authenticate, login as dj_login, logout as s_logout
func = Main()
User = get_user_model()

# Create your views here.

def merchant_required(login_url=None):
    return user_passes_test(lambda u: u.is_merchant, login_url=login_url)


def register(request):
    if request.user.is_authenticated:
        return redirect('/merchant/home')
    elif request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        passw = request.POST['password']
        if User.objects.filter(mobile=mobile).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Email/Mobile Number has been used")
            return render(request, 'merchant/register.html', {'fullname':fullname, 'email':email, 'mobile':mobile})
        else:
            func.MerchantSignup(mobile, passw, fullname, email)
            messages.success(request, "Account Created")
            return redirect('/merchant/register')
    else:
        return render(request, 'merchant/register.html')
    

def login(request):
    if request.user.is_authenticated and request.user.is_merchant == True:
        return redirect('/merchant/home')
    elif request.method == "POST":
        email = request.POST['email']
        passw = request.POST['password']
        if '@' not in email:
            messages.error(request, 'Not an Email')
            return redirect('/merchant/login')
        elif User.objects.filter(email=email, is_merchant=False).exists():
            messages.error(request, 'You are not permitted')
            return redirect('/merchant/login')
        else:
            user = authenticate(mobile=email, password=passw)
            if user is not None:
                dj_login(request, user)
                # request.session.set_expiry(1200)
                fullname = request.user.fullname
                messages.success(request, f'Welcome Back {fullname}')
                response = redirect('/merchant/home')
                return response
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('/merchant/login')
    else:
        return render(request, 'merchant/login.html')
    

@merchant_required(login_url='/merchant/login')
def home(request):
    mobile = request.user.mobile
    bal = func.GetWalletBall(mobile)
    return render(request, 'merchant/home.html', {'bal':bal})


def logout(request):
    s_logout(request)
    messages.success(request, "Logout Successfully")
    resp = redirect('/merchant/login')
    return resp

@merchant_required(login_url='/merchant/login')
def transactions(request):
    show = func.GetLog(request)
    return render(request, 'merchant/transactions.html',{'show':show})


@merchant_required(login_url='/merchant/login')
def business_settings(request):
    mobile = request.user.mobile
    if request.method == "POST":
        bus_name = request.POST['bus_name']
        bus_address = request.POST['bus_address']
        callbackurl = request.POST['callbackurl']
        if bus_name == 'None' or bus_address == 'None':
            messages.error(request, "Please you can't have None Value as your business name or business address")
            return redirect('/merchant/business_settings')
        else:
            upd_business = Merchant.objects.filter(mobile=mobile)
            upd_business.update(done=True, bus_name=bus_name, bus_address=bus_address, callbackurl=callbackurl)
            messages.success(request, "Business Settings Updated. Kindly get Your API for Integration")
            return redirect('/merchant/api_settings')
    else:
        alld = func.GetBusinessDetails(request)
        return render(request, 'merchant/settings.html',{'alld':alld})

@merchant_required(login_url='/merchant/login')
def api_settings(request):
    mobile = request.user.mobile
    if func.BusinessDone(request) == False:
        messages.error(request, "Please you have to complete your business settings")
        return redirect('/merchant/business_settings')
    else:
        api_test = uuid.uuid4().hex[:20].lower()
        api_live = uuid.uuid4().hex[:20].lower()
        if request.method == "POST":
           apikey = MerchantKey.objects.filter(mobile=mobile)
           apikey.update(live_key=api_live, test_key=api_test)
           messages.success(request, "API Successful")
           return redirect('/merchant/api_settings')   
        api = func.GetAPIDetails(request)
        return render(request, 'merchant/api.html', {'api':api})