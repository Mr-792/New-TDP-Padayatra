from django.db import models
from Admins.models import PadayatraSchedule
# Create your models here.

class Districts(models.Model):
    district = models.CharField(max_length=255)
    source_link = models.TextField(default="")
    
    class Meta:
        db_table = 'Districts'

class Assemblies(models.Model):
    district = models.CharField(max_length=255)
    assembly = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'Assemblies'
        
class Users(models.Model):
    phone = models.CharField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    dob=models.DateField()
    gender = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    whatsapp = models.CharField(max_length=255)
    profession = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255)
    assembly = models.CharField(max_length=255)
    village=models.CharField(max_length=255,blank=True, null=True)
    pincode=models.PositiveIntegerField()
    role = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=1000,blank=True,null=True)
    blocked_posts = models.TextField(default="")

    class Meta:
        db_table = 'Users'

class Otp(models.Model):
    phone = models.CharField(max_length=50)
    otp = models.CharField(max_length=5)
    expiry = models.DateTimeField()
    
    class Meta:
        db_table = 'Otp'

class PadayatraRegistration(models.Model):
    user_id = models.IntegerField()
    padayatra_id = models.ForeignKey(PadayatraSchedule, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Padayatra_Registration'


class Professions(models.Model):
    profession = models.CharField(max_length=50)

    class Meta:
        db_table = 'Professions'