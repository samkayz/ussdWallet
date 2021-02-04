from django.shortcuts import render
from . admin_function import *
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
