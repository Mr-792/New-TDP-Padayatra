from dataclasses import fields
from rest_framework import serializers
from .models import *

class DistrictsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Districts
        fields = '__all__'

class AssembliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assemblies
        fields = '__all__'
        
class UsersSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default='ENDUSER')
    class Meta:
        model = Users
        fields = '__all__'


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = '__all__'

class PadayatraRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PadayatraRegistration
        fields = '__all__'

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professions
        fields = '__all__'
