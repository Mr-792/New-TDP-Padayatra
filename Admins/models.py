from django.db import models

class Admins(models.Model):
    user_name=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    is_superadmin=models.BooleanField(default=False)
    is_supervisor=models.BooleanField(default=False)
    is_manager=models.BooleanField(default=False)

    class Meta:
        db_table='Admins'


class PadayatraSchedule(models.Model):
    title=models.TextField()
    district=models.CharField(max_length=255)
    source_link = models.TextField(default="")
    assembly=models.CharField(max_length=255)
    village=models.CharField(max_length=255,blank=True)
    start_point=models.TextField()
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    status=models.CharField(max_length=100)
    registered_users = models.JSONField(default=dict)
    registered_users_count=models.PositiveBigIntegerField(default=0)
    padayatra_link = models.TextField(default="")


    class Meta:
        db_table='Padayatra_Schedule'


class YoutubeURLs(models.Model):
    live_url=models.TextField(blank=True,null=True)
    Addational_Video_url1 = models.TextField(blank=True,null=True)
    Addational_Video_url2 = models.TextField(blank=True,null=True)
    Addational_Video_url3 = models.TextField(blank=True,null=True)
    Addational_Video_url4 = models.TextField(blank=True,null=True)
    Addational_Video_url5 = models.TextField(blank=True,null=True)

    class Meta:
        db_table='YoutubeURLs'
