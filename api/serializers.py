from rest_framework import serializers
from web.models import *



class UtilitySerializers(serializers.ModelSerializer):
    class Meta:
        many = True
        model = Utility
        fields = "__all__"