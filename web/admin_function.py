from django.http import request
from .models import *
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