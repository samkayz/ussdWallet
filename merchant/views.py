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
    if request.user.is_authenticated:
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
    return render(request, 'merchant/home.html')


def logout(request):
    s_logout(request)
    messages.success(request, "Logout Successfully")
    resp = redirect('/merchant/login')
    return resp
