from django.shortcuts import render
from . admin_function import *
from django.contrib.auth.decorators import permission_required
func = Main()
# Create your views here.


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email)
        resp = func.AdminLogin(request, email, password)
        return resp
    else:
        return render(request, 'web/login.html')


@permission_required('is_superuser', login_url='/web/')
def home(request):
    show = func.ShowTransLog().order_by('-id')[:5]
    return render(request, 'web/index.html', {'show':show})


@permission_required('is_superuser', login_url='/web/')
def log(request):
    show = func.ShowTransLog()
    return render(request, 'web/log.html', {'show':show})


@permission_required('is_superuser', login_url='/web/')
def user(request):
    users = func.GetUser()
    wallet = func.GetWallet()
    return render(request, 'web/user.html', {'users':users, 'wallet':wallet})


def logout(request):
    res = func.AdminLogout(request)
    return res