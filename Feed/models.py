from xmlrpc.client import _iso8601_format
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder 

class Posts(models.Model):
    title_english = models.CharField(max_length=255)
    title_telugu = models.CharField(max_length=255,blank=True, null=True)
    category = models.CharField(max_length=255)
    description_english = models.TextField(blank=True, null=True)
    description_telugu = models.TextField(blank=True, null=True)

    source_link = models.TextField()
    tags = models.CharField(max_length=255, blank=True, null=True)

    shares_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)

    liked_users = models.JSONField(default=dict)
    bookmarked_users = models.JSONField(default=dict)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=1000, blank=True, null=True)
    post_type = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField()
    published = models.BooleanField(default=False)

    
    class Meta:
        db_table = 'Posts'


class Comments(models.Model):
    comment = models.CharField(max_length=10000, blank=True, null=True)
    commented_by = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Comments'


class Likes(models.Model):
    liked_by = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True) 
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Likes'


class Bookmarks(models.Model):
    bookmarked_by = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Bookmarks'



