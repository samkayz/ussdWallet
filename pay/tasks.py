from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab
from celery import shared_task
from .models import *
import string
import random
import datetime
import time
from datetime import timedelta


@periodic_task(run_every=timedelta(seconds=5))
def Hello():
    print("Good Afternoon")
    pass

   
   