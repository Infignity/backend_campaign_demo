'''importing the usable libraries'''
from rest_framework import serializers
from .models import Company


# company data serializer
class CompanySerializer(serializers.ModelSerializer):
    '''a serializer for the company model'''
    class Meta:
        '''sampling the fields'''
        model = Company
        fields = "__all__"