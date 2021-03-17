from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PayToken(models.Model):
    paycode = models.TextField()
    token = models.CharField(max_length=100)
    amount = models.FloatField(null=True,blank=True)
    apikey = models.TextField(null=True,blank=True)
    desc = models.TextField(null=True,blank=True)
    status = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pay_token'