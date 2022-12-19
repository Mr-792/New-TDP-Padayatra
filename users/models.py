from django.db import models
from django.utils import timezone


class Districts(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'Districts'

class Assemblies(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'Assemblies'


class Users(models.Model):
    phone = models.CharField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    whatsapp = models.CharField(max_length=255)
    profession = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255)
    assembly_constituency = models.CharField(max_length=255)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Users'

class Otp(models.Model):
    phone = models.CharField(max_length=50)
    otp = models.CharField(max_length=5)
    expiry = models.DateTimeField()
    
    class Meta:
        db_table = 'Otp'
