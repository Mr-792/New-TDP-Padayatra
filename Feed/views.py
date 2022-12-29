import requests
import time
import base64
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.core.exceptions import *
import datetime
import jwt
import json
import base64
import io
from datetime import datetime
import boto3
from django.utils.dateparse import parse_datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Users.models import Users


def post(request):
    if request.method == "POST":
        desc = request.POST.get('desc')
        print("description is==========", desc)
        pass
from django.views.decorators.csrf import csrf_exempt
import PIL.Image as Image
@csrf_exempt
def UploadPost(request):
    upload_data = {}
    upload_data['files']=[]
    if request.method == "POST":

        file = request.FILES['files']
        print(file)

      
        # for file in files_up:
        print(file.name)
        file_extension = file.name.split('.')[1]
        print(file_extension)
        file_type = 'IMAGE'


            # file_extension=
        data = base64.b64encode(file.read())
        data_dict = {}
        data_dict["file_extension"] = file_extension
        data_dict["file_type"] = file_type
        data_dict["data"] = data
        print("datadictionary is===============", data_dict.keys())
        upload_data['files'].append(data_dict)
        print("files=================", upload_data.keys())
        print(type(upload_data))
    
        req = requests.post(
            url="http://localhost:8000/feed/upload-file",
        files=upload_data
        )
        print(req.json())


class PostsApi(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    # authentication_classes = [CustomAuthentication]

    def upload(self, request, *args, **kwargs):
        ACCESS_KEY_ID = 'AKIA3EKDCQ7FVPPPQSYQ'
        SECRET_ACCESS_KEY = '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'
        Bucket = 'dev-tdp-be'
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID,
                          aws_secret_access_key=SECRET_ACCESS_KEY)

        url_data_set = []
        print("==============================================")
        files = request.data['files']
        print("***********************fuiles************",len(files))
        for i in files:
            file_extension = i['file_extension']
            file_type = i['file_type']
            data = i['data']
          
            print(file_extension, file_type, len(data))

            if 1:
                now = datetime.now()
                current_time_date = now.strftime("%y%m%d%M%H%S%f")
                file_name = current_time_date+"."+file_extension
                decoded_data = base64.b64decode(data)

                if file_type == 'IMAGE':
                    # converting the image to bytes data
                    bytes_data = io.BytesIO(decoded_data)
                    # we are checking if its a gif or animated
                    # if any of them becomes true, we are uploading it, without compressing

                    s3.upload_fileobj(bytes_data, Bucket, "images/"+file_name,
                                    ExtraArgs={'ContentType': "image/"+file_extension})
                    bucket_location = s3.get_bucket_location(Bucket=Bucket)
                    object_url = "https://{1}.s3.{0}.amazonaws.com/images/{2}".format(
                        bucket_location['LocationConstraint'], Bucket, file_name)

                elif file_type == 'VIDEO':
                    bytes_data = io.BytesIO(decoded_data)
                    s3.upload_fileobj(bytes_data, Bucket, "videos/"+file_name,
                                    ExtraArgs={'ContentType': "video/"+file_extension})
                    bucket_location = s3.get_bucket_location(Bucket=Bucket)
                    object_url = "https://{1}.s3.{0}.amazonaws.com/videos/{2}".format(
                        bucket_location['LocationConstraint'], Bucket, file_name)

                url_data_set.append(object_url)

            return Response({"message": "Uploaded successfully.", "data": url_data_set}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        # try:
        serializer = PostsSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"message": "Posted successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

        # except Exception as e:
        #     return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk, *args, **kwargs):
        # try:
        query_object1 = Posts.objects.filter(id=pk, published=True)
        unserialized_query_object1 = PostsSerializer(query_object1, many=True)

        # query_object2 = Likes.objects.filter(postid=pk)
        # unserialized_query_object2 = LikesSerializer(query_object2,many =True)

        # query_object3 = Comments.objects.filter(postid=pk)
        # unserialized_query_object3 = CommentsSerializer(query_object3,many =True)

        return Response({"message": "Fetched successfully.", "data": unserialized_query_object1.data}, status=status.HTTP_200_OK)

        # except Exception as e:
        #     return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk, *args, **kwargs):
        try:
            query_object = Posts.objects.filter(id=request.data['id']).update(
                title_english=request.data['title_english'],
                title_telugu=request.data['title_telugu'],
                category=request.data['category'],
                description_english=request.data['description_english'],
                description_telugu=request.data['description_telugu'],
                source_link=request.data['source_link'],
                tags=request.data['tags'],
                location=request.data['location'],
                post_type=request.data['post_type'],
                user_id=request.data['user_id'],
                published=request.data['published'])

            return Response({"message": "Updated successfully.", "data": request.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status": 500, "msg": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk, *args, **kwargs):
        try:
            query_object = Posts.objects.filter(id=pk)
            query_object.delete()
            return Response({"message": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"status": 500, "msg": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentApi(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    # authentication_classes = [CustomAuthentication]

    def create(self, request, *args, **kwargs):
        # try:
        serializer = CommentsSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"message": "Commented successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

        # except Exception as e:
        #     return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk, *args, **kwargs):
        try:
            query_object = Comments.objects.filter(
                id=request.data['id']).update(comment=request.data['comment'])

            return Response({"message": "Updated successfully.", "data": request.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status": 500, "msg": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk, *args, **kwargs):
        try:
            query_object = Comments.objects.filter(id=pk)
            query_object.delete()
            return Response({"message": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"status": 500, "msg": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LikesApi(viewsets.ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    # authentication_classes = [CustomAuthentication]

    def create(self, request, *args, **kwargs):
        try:
            query_object1 = Likes.objects.filter(
                post_id=request.data['post_id'], liked_by=request.data['liked_by'])
            unserialized_query_object1 = LikesSerializer(
                query_object1, many=True)

            print(unserialized_query_object1.data)
            if unserialized_query_object1.data:
                return Response({"message": "You have already liked this post"}, status=status.HTTP_409_CONFLICT)
            else:
                serializer = LikesSerializer(data=request.data)

                if serializer.is_valid(raise_exception=True):
                    serializer.save()

                query_object2 = Posts.objects.filter(
                    id=request.data['post_id'])
                unserialized_query_object2 = PostsSerializer(
                    query_object2, many=True)
                liked_dataset = unserialized_query_object2.data[0]['liked_users']
                liked_dataset[int(request.data['liked_by'])] = True
                query_object = Posts.objects.filter(id=request.data['post_id']).update(
                    liked_users=liked_dataset, likes_count=len(liked_dataset))
                return Response({"message": "Liked successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status": 500, "msg": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            query_object = Likes.objects.filter(
                post_id=request.data['post_id'])
            query_object.delete()

            query_object1 = Posts.objects.filter(id=request.data['post_id'])
            unserialized_query_object1 = PostsSerializer(
                query_object1, many=True)
            liked_dataset = unserialized_query_object1.data[0]['liked_users']
            liked_dataset.pop(str(request.data['liked_by']))
            query_object = Posts.objects.filter(id=request.data['post_id']).update(
                liked_users=liked_dataset, likes_count=len(liked_dataset))

            return Response({"message": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"status": 500, "msg": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookmarksApi(viewsets.ModelViewSet):
    queryset = Bookmarks.objects.all()
    serializer_class = BookmarksSerializer
    # authentication_classes = [CustomAuthentication]

    def create(self, request, *args, **kwargs):
        # try:
        serializer = BookmarksSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"message": "Bookmarked successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

        # except Exception as e:
        #     return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk, *args, **kwargs):
        try:
            query_object = Bookmarks.objects.filter(id=pk)
            query_object.delete()
            return Response({"message": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"status": 500, "msg": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FeedAPI(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    # authentication_classes = [CustomAuthentication]

    def feed(self, request, *args, **kwargs):
        try:
            userid = str(3)
            query_object1 = Posts.objects.filter(published=True)
            unserialized_query_object1 = PostsSerializer(
                query_object1, many=True)
            feed_data = []

            for i in unserialized_query_object1.data:
                i['user_liked'] = True if userid in i['liked_users'] else False
                i['user_bookmarked'] = True if userid in i['bookmarked_users'] else False
                feed_data.append(i)

            final_data_set = sorted(
                feed_data, key=lambda x: x['created_date'], reverse=True)
            return Response({"message": "Fetched successfully.", "data": final_data_set}, status=status.HTTP_200_OK)

            # page = self.paginate_queryset(finaldata)

        except jwt.ExpiredSignatureError as e:
            raise jwt.ExpiredSignatureError
        except jwt.InvalidSignatureError as e:
            raise jwt.InvalidSignatureError
        except Exception as e:
            return Response({"status": 500, "msg": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
