from rest_framework import serializers
from .models import Posts,Likes,Comments,Bookmarks


class PostsSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Posts
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'

class BookmarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmarks
        fields = '__all__'

