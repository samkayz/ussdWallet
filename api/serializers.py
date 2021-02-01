from django.db.models import fields
from rest_framework import serializers
from web.models import *



class UtilitySerializers(serializers.ModelSerializer):
    class Meta:
        many = True
        model = Utility
        fields = "__all__"

class BankSerializers(serializers.ModelSerializer):

    class Meta:
        many = True
        model = Banks
        fields = "__all__"