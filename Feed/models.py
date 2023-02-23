from xmlrpc.client import _iso8601_format
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder 

class Posts(models.Model):
    title_english = models.CharField(max_length=255)
    title_telugu = models.CharField(max_length=255,blank=True, null=True)
    category = models.CharField(max_length=255)
    description_english = models.TextField(blank=True, null=True)
    description_telugu = models.TextField(blank=True, null=True)

    source_link = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)

    shares_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)

    liked_users = models.JSONField(default=dict)
    bookmarked_users = models.JSONField(default=dict)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
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
    user_name = models.CharField(max_length=255)
    blocked = models.BooleanField(default=False)

    class Meta:
        db_table = 'Comments'


class Likes(models.Model):
    liked_by = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True) 
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'Likes'


class Bookmarks(models.Model):
    bookmarked_by = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'Bookmarks'



class Stories(models.Model):
    title_english = models.CharField(max_length=255)
    title_telugu = models.CharField(max_length=255,blank=True, null=True)
    source_link = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField()
    published = models.BooleanField(default=False)
    thumbnail = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Stories'


class Banners(models.Model):
    title_english = models.CharField(max_length=255)
    source_link = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    user_id = models.IntegerField()
    published = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Banners'


class Polls(models.Model):
    question_english = models.TextField()
    options_english = models.JSONField(default=dict)
    start_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)
    question_telugu = models.TextField()
    options_telugu = models.JSONField(default=dict)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    polled_users = models.JSONField(default=dict)
    thoughts = models.JSONField(default=dict)
    published = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Polls'