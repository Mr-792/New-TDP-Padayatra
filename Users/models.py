from django.db import models
# Create your models here.

class Users(models.Model):
    phone = models.CharField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    dob=models.DateField()
    age=models.PositiveIntegerField()

    create_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    whatsapp = models.CharField(max_length=255)
    profession = models.CharField(max_length=255, blank=True, null=True)

    district = models.CharField(max_length=255)
    assembly = models.CharField(max_length=255)
    village=models.CharField(max_length=255)
    pin_code=models.PositiveIntegerField()
  
 
    facebook = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Users'

from Admins.models import PadayatraSchedule

class PadayatraRegistration(models.Model):
    pass