from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.core.exceptions import *
import datetime, jwt,json,base64,io
from datetime import datetime
import boto3
from django.utils.dateparse import parse_datetime
from YuvaGallam.customauth import CustomAuthentication
from Users.models import *
from Users.serializers import *
from Users.utilities import write_CSV


class PostsApi(viewsets.ModelViewSet):       
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    authentication_classes = [CustomAuthentication]
    
    def upload(self, request, *args, **kwargs):
        ACCESS_KEY_ID = 'AKIAWX46IY3CQVLKK2J2'
        SECRET_ACCESS_KEY = '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'
        Bucket = 'dev-tdp-feed'
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
    
        url_data_set = []
        files = request.data['files']


        for i in files:
            file_extension = i['file_extension']
            file_type = i['file_type']
            data = i['data']
            
            try:
            # if 1:
                now = datetime.now()
                current_time_date = now.strftime("%y%m%d%M%H%S%f")
                file_name = current_time_date+"."+file_extension
                decoded_data = base64.b64decode(data)
                
                if file_type == 'IMAGE':

                    bytes_data = io.BytesIO(decoded_data)

                    s3.upload_fileobj(bytes_data, Bucket, "images/"+file_name,ExtraArgs={'ContentType': "image/"+file_extension})
                    bucket_location = s3.get_bucket_location(Bucket=Bucket)
                    object_url = "https://{1}.s3.{0}.amazonaws.com/images/{2}".format(bucket_location['LocationConstraint'],Bucket,file_name)
                
                elif file_type == 'VIDEO':
                    bytes_data = io.BytesIO(decoded_data)
                    s3.upload_fileobj(bytes_data, Bucket,"videos/"+file_name,ExtraArgs={'ContentType': "video/"+file_extension})
                    bucket_location = s3.get_bucket_location(Bucket=Bucket)
                    object_url = "https://{1}.s3.{0}.amazonaws.com/videos/{2}".format(bucket_location['LocationConstraint'],Bucket,file_name)
                
                url_data_set.append(object_url)

            except Exception as e:
                print(e)

        return Response({"message":"Uploaded successfully.","data":url_data_set},status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            serializer = PostsSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({"message":"Posted successfully.","data":serializer.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, pk, *args, **kwargs):
        # try:
            payload = CustomAuthentication.authenticate(self,request)
            logged_in_user = str(payload[0]['id'])
            query_object1 = Posts.objects.filter(id=pk,published=True)
            unserialized_query_object1 = PostsSerializer(query_object1,many =True)
            
            query_object2 = Likes.objects.filter(post_id=pk)
            unserialized_query_object2 = LikesSerializer(query_object2,many =True)
            
            query_object3 = Comments.objects.filter(post_id=pk)
            unserialized_query_object3 = CommentsSerializer(query_object3,many =True)

            full_data = json.loads(json.dumps(unserialized_query_object1.data))
            
            full_data[0]['user_liked'] = True if logged_in_user in full_data[0]['liked_users'] else False
            full_data[0]['user_bookmarked'] = True if logged_in_user in full_data[0]['bookmarked_users'] else False
            
            full_data[0].pop('liked_users')
            full_data[0].pop('bookmarked_users')

            if full_data[0]['source_link'] != "":
                temp = full_data[0]['source_link'].split(",")
                full_data[0]['source_link'] = temp
            else:
                full_data[0]['source_link'] = []

            return Response({"message":"Fetched successfully.","data":full_data},status=status.HTTP_200_OK)
            
        # except Exception as e:
        #     return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        # try:
            # print("hey")
            # temp = json.dumps(json.loads(request.data))
            # print(temp)
            query_object = Posts.objects.filter(id=request.data['id']).update(
            title_english = request.data['title_english'],
            title_telugu = request.data['title_telugu'],
            category = request.data['category'],
            description_english = request.data['description_english'],
            description_telugu = request.data['description_telugu'],
            source_link = request.data['source_link'],
            tags = request.data['tags'],
            post_type = request.data['post_type'],
            user_id = request.data['user_id'],
            published = request.data['published'])

            return Response({"message":"Updated successfully.","data":request.data},status=status.HTTP_200_OK)
 
        # except Exception as e:
        #     return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def publish(self, request, *args, **kwargs):
        try:
            query_object1 = Posts.objects.filter(id=request.data['id']).update(
                published = request.data['published'])

            return Response({"message":"Updated successfully.","data":request.data},status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request,pk, *args, **kwargs):
        try:
            query_object = Posts.objects.filter(id=pk)
            query_object.delete()
            return Response({"message":"Deleted successfully."},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def all_posts(self, request, *args, **kwargs):
        try:
            query_object1 = Posts.objects.all()
            unserialized_query_object1 = PostsSerializer(query_object1,many =True)
            data_set = sorted(unserialized_query_object1.data,key = lambda x:x['created_date'],reverse=True)

            return Response({"message":"Fetched successfully.","data":data_set},status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def block(self, request, *args, **kwargs):
        try:
            payload = CustomAuthentication.authenticate(self,request)
            logged_in_user = payload[0]['id']

            query_object1 = Users.objects.filter(id=logged_in_user)
            unserialized_query_object1 = UsersSerializer(query_object1,many =True)
            post_blocked = unserialized_query_object1.data[0]['blocked_posts']

            if str(request.data['id']) in post_blocked:
                return Response({"message":"you have already blocked this post.","data":request.data},status=status.HTTP_200_OK)
            else:
                blocked_posts = post_blocked+str(request.data['id'])+","
                query_object2 = Users.objects.filter(id=logged_in_user).update(blocked_posts=blocked_posts)
                return Response({"message":"blocked successfully.","data":request.data},status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def all_posts_with_comments(self, request, *args, **kwargs):
        try:
            query_object1 = Posts.objects.all()
            unserialized_query_object1 = PostsSerializer(query_object1,many =True)
            all_post = []
            for i in unserialized_query_object1.data:
                query_object2 = Comments.objects.filter(post_id=i['id'])
                unserialized_query_object2 = CommentsSerializer(query_object2,many =True)
                temp = unserialized_query_object2.data
                comments_data = sorted(temp,key = lambda x:x['created_date'],reverse=True)
                # full_data = json.loads(json.dumps(unserialized_query_object1.data))
                i['comments_data'] = comments_data
                all_post.append(i)
            return Response({"message":"Fetched successfully.","data":all_post},status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def share(self, request, *args, **kwargs):
        try:

            count = list(Posts.objects.filter(id=request.data['id']).values('shares_count'))
            if count:
                temp = count[0]
                query_object2 = Posts.objects.filter(id=request.data['id']).update(
                    shares_count = temp['shares_count']+1)
                return Response({"message":"Updated successfully.","data":request.data},status=status.HTTP_200_OK)
            else:
                return Response({"message":"no data found"},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LikesApi(viewsets.ModelViewSet):    
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    authentication_classes = [CustomAuthentication]

    def create(self, request, *args, **kwargs):
        try:
        # if 1:
            query_object1 = Likes.objects.filter(post_id=request.data['post_id'],liked_by=request.data['liked_by'])
            unserialized_query_object1 = LikesSerializer(query_object1,many =True)

            print(unserialized_query_object1.data)
            if unserialized_query_object1.data:
                return Response({"message":"You have already liked this post"},status=status.HTTP_409_CONFLICT)   
            else:
                serializer = LikesSerializer(data=request.data)

                if serializer.is_valid(raise_exception=True):
                    serializer.save()

                query_object2 = Posts.objects.filter(id=request.data['post_id'])
                unserialized_query_object2 = PostsSerializer(query_object2,many =True)
                liked_dataset = unserialized_query_object2.data[0]['liked_users']
                liked_dataset[int(request.data['liked_by'])] = True
                query_object = Posts.objects.filter(id=request.data['post_id']).update(liked_users=liked_dataset,likes_count=len(liked_dataset))
                return Response({"message":"Liked successfully.","data":serializer.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, *args, **kwargs):
        try:
            query_object = Likes.objects.filter(liked_by=request.data['liked_by'],post_id=request.data['post_id'])
            query_object.delete()

            query_object1 = Posts.objects.filter(id=request.data['post_id'])
            unserialized_query_object1 = PostsSerializer(query_object1,many =True)
            liked_dataset = unserialized_query_object1.data[0]['liked_users']
            liked_dataset.pop(str(request.data['liked_by']))
            query_object = Posts.objects.filter(id=request.data['post_id']).update(liked_users=liked_dataset,likes_count=len(liked_dataset))

            return Response({"message":"Deleted successfully."},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentsApi(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    authentication_classes = [CustomAuthentication] 

    def create(self, request, *args, **kwargs):
        try:
            serializer = CommentsSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

                query_object2 = Posts.objects.filter(id=request.data['post_id'])
                unserialized_query_object2 = PostsSerializer(query_object2,many =True)
                comments_count = unserialized_query_object2.data[0]['comments_count']
                query_object = Posts.objects.filter(id=request.data['post_id']).update(comments_count=comments_count+1)
            return Response({"message":"Commented successfully.","data":serializer.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk, *args, **kwargs):
        try:
            query_object1 = Comments.objects.filter(post_id=pk,blocked=False)
            unserialized_query_object1 = CommentsSerializer(query_object1,many =True)

            full_data = json.loads(json.dumps(unserialized_query_object1.data))
            return Response({"message":"Fetched successfully.","data":full_data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request,pk, *args, **kwargs):
        try:
            query_object = Comments.objects.filter(id=request.data['id']).update(comment = request.data['comment'])

            return Response({"message":"Updated successfully.","data":request.data},status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, *args, **kwargs):
        try:
            query_object1 = Comments.objects.filter(id=request.data['comment_id'])
            query_object1.delete()
            query_object2 = Posts.objects.filter(id=request.data['post_id'])
            unserialized_query_object2 = PostsSerializer(query_object2,many =True)
            comments_count = unserialized_query_object2.data[0]['comments_count']
            query_object = Posts.objects.filter(id=request.data['post_id']).update(comments_count=comments_count-1)
            return Response({"message":"Deleted successfully."},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def block(self, request, *args, **kwargs):
        try:
            query_object1 = Comments.objects.filter(id=request.data['id']).update(
                blocked = request.data['blocked'])

            return Response({"message":"Blocked successfully.","data":request.data},status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BookmarksApi(viewsets.ModelViewSet):    
    queryset = Bookmarks.objects.all()
    serializer_class = BookmarksSerializer
    authentication_classes = [CustomAuthentication]

    def create(self, request, *args, **kwargs):
        try:
            serializer = BookmarksSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

            query_object1 = Posts.objects.filter(id=request.data['post_id'])
            unserialized_query_object1 = PostsSerializer(query_object1,many =True)
            bookmarked_dataset = unserialized_query_object1.data[0]['bookmarked_users']
            bookmarked_dataset[int(request.data['bookmarked_by'])] = True
            query_object2 = Posts.objects.filter(id=request.data['post_id']).update(bookmarked_users=bookmarked_dataset)
            return Response({"message":"Bookmarked successfully.","data":serializer.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            payload = CustomAuthentication.authenticate(self,request)

            logged_in_user = str(payload[0]['id'])
            # print(logged_in_user)
            ids = list(Bookmarks.objects.filter(bookmarked_by=logged_in_user).values_list('post_id_id', flat=True))
            query_object1 = Posts.objects.filter(id__in=ids)
            unserialized_query_object1 = PostsSerializer(query_object1,many =True)
            
            bookmarked_data = []
            for i in unserialized_query_object1.data:
                if i['published'] == True:
                    print(i['bookmarked_users'])
                    i['user_liked'] = True if logged_in_user in i['liked_users'] else False
                    i['user_bookmarked'] = True if logged_in_user in i['bookmarked_users'] else False
                    temp = i['source_link'].split(",")
                    i['source_link'] = temp
                    
                    i.pop('liked_users')
                    i.pop('bookmarked_users')
                    bookmarked_data.append(i)
                else:
                    # skipping unpublished posts
                    pass
                
            
            final_data_set = sorted(bookmarked_data,key = lambda x:x['created_date'],reverse=True)
            page = self.paginate_queryset(final_data_set)

            if page:
                return Response({"message":"Fetched successfully.","count":len(final_data_set),"data":page},status=status.HTTP_200_OK)
            else:
               return Response({"message":"No more posts.","count":len(final_data_set),"data":[]},status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            query_object1 = Bookmarks.objects.filter(bookmarked_by=request.data['bookmarked_by'],post_id=request.data['post_id'])
            query_object1.delete()

            query_object2 = Posts.objects.filter(id=request.data['post_id'])
            unserialized_query_object2 = PostsSerializer(query_object2,many =True)
            bookmarks_dataset = unserialized_query_object2.data[0]['bookmarked_users']
            bookmarks_dataset.pop(str(request.data['bookmarked_by']))
            query_object = Posts.objects.filter(id=request.data['post_id']).update(bookmarked_users=bookmarks_dataset)
            return Response({"message":"Deleted successfully."},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


###############################################################################################################
###############################################################################################################
###############################-------------------------------------------------###############################


class FeedAPI(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    authentication_classes = [CustomAuthentication]

    def feed(self, request, *args, **kwargs):
        # try:
            payload = CustomAuthentication.authenticate(self,request)
            logged_in_user = str(payload[0]['id'])
            print(logged_in_user)
            query_object1 = Posts.objects.filter(published=True)
            unserialized_query_object1 = PostsSerializer(query_object1,many =True)
            feed_data = []

            query_object2 = Users.objects.filter(id=int(logged_in_user))
            unserialized_query_object2 = UsersSerializer(query_object2,many =True)
            post_blocked = unserialized_query_object2.data[0]['blocked_posts']

            for i in unserialized_query_object1.data:
                if str(i['id']) in post_blocked:
                    # skipping user blocked posted
                    pass
                else:
                    i['user_liked'] = True if logged_in_user in i['liked_users'] else False
                    i['user_bookmarked'] = True if logged_in_user in i['bookmarked_users'] else False

                    if i['source_link'] != "":
                        temp = i['source_link'].split(",")
                        i['source_link'] = temp
                    else:
                        i['source_link'] = []    

                    i.pop('liked_users')
                    i.pop('bookmarked_users')
                    feed_data.append(i)
                
            final_data_set = sorted(feed_data,key = lambda x:x['created_date'],reverse=True)
            page1 = self.paginate_queryset(final_data_set)
            page2 = self.get_paginated_response(page1)

            if page2:
                return page2
            else:
               return Response({"message":"No more posts.","count":len(final_data_set),"data":[]},status=status.HTTP_204_NO_CONTENT)
      
        # except Exception as e:
        #     return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


###############################################################################################################
###############################################################################################################
###############################-------------------------------------------------###############################

class StoriesAPI(viewsets.ModelViewSet):     
    queryset = Stories.objects.all()
    serializer_class = StoriesSerializer
    authentication_classes = [CustomAuthentication]
    
    def upload_stories(self, request, *args, **kwargs):
        ACCESS_KEY_ID = 'AKIAWX46IY3CQVLKK2J2'
        SECRET_ACCESS_KEY = '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'
        Bucket = 'dev-tdp-feed'
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
    
        url_data_set = []
        files = request.data['files']
        
        for i in files:
            file_extension = i['file_extension']
            file_type = i['file_type']
            data = i['data']
            
            try:
            # if 1:
                now = datetime.now()
                current_time_date = now.strftime("%y%m%d%M%H%S%f")
                file_name = current_time_date+"."+file_extension
                decoded_data = base64.b64decode(data)
                
                if file_type == 'IMAGE':

                    bytes_data = io.BytesIO(decoded_data)

                    s3.upload_fileobj(bytes_data, Bucket, "stories/images/"+file_name,ExtraArgs={'ContentType': "image/"+file_extension})
                    bucket_location = s3.get_bucket_location(Bucket=Bucket)
                    object_url = "https://{1}.s3.{0}.amazonaws.com/stories/images/{2}".format(bucket_location['LocationConstraint'],Bucket,file_name)
                
                elif file_type == 'VIDEO':
                    bytes_data = io.BytesIO(decoded_data)
                    s3.upload_fileobj(bytes_data, Bucket,"stories/videos/"+file_name,ExtraArgs={'ContentType': "video/"+file_extension})
                    bucket_location = s3.get_bucket_location(Bucket=Bucket)
                    object_url = "https://{1}.s3.{0}.amazonaws.com/stories/videos/{2}".format(bucket_location['LocationConstraint'],Bucket,file_name)
                
                url_data_set.append(object_url)

            except Exception as e:
                print(e)

        return Response({"message":"Uploaded successfully.","data":url_data_set},status=status.HTTP_200_OK)

    def upload_stories_thumbnail(self, request, *args, **kwargs):
        ACCESS_KEY_ID = 'AKIAWX46IY3CQVLKK2J2'
        SECRET_ACCESS_KEY = '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'
        Bucket = 'dev-tdp-feed'
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
    
        url_data_set = []
        files = request.data['files']
        
        for i in files:
            file_extension = i['file_extension']
            file_type = i['file_type']
            data = i['data']
            
            try:
            # if 1:
                now = datetime.now()
                current_time_date = now.strftime("%y%m%d%M%H%S%f")
                file_name = current_time_date+"."+file_extension
                decoded_data = base64.b64decode(data)
                
                if file_type == 'IMAGE':

                    bytes_data = io.BytesIO(decoded_data)

                    s3.upload_fileobj(bytes_data, Bucket, "stories/thumbnails/"+file_name,ExtraArgs={'ContentType': "image/"+file_extension})
                    bucket_location = s3.get_bucket_location(Bucket=Bucket)
                    object_url = "https://{1}.s3.{0}.amazonaws.com/stories/thumbnails/{2}".format(bucket_location['LocationConstraint'],Bucket,file_name)
                
                elif file_type == 'VIDEO':
                    bytes_data = io.BytesIO(decoded_data)
                    s3.upload_fileobj(bytes_data, Bucket,"stories/videos/"+file_name,ExtraArgs={'ContentType': "video/"+file_extension})
                    bucket_location = s3.get_bucket_location(Bucket=Bucket)
                    object_url = "https://{1}.s3.{0}.amazonaws.com/stories/videos/{2}".format(bucket_location['LocationConstraint'],Bucket,file_name)
                
                url_data_set.append(object_url)

            except Exception as e:
                print(e)

        return Response({"message":"Uploaded successfully.","data":url_data_set},status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            serializer = StoriesSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({"message":"Posted successfully.","data":serializer.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, *args, **kwargs):
        try:
            query_object1 = Stories.objects.filter(published=True).order_by('-id')[:10]
            unserialized_query_object1 = StoriesSerializer(query_object1,many =True)
            full_data = json.loads(json.dumps(unserialized_query_object1.data))
            sorted_data_set = sorted(full_data,key = lambda x:x['created_date'],reverse=True)
            
            story_title_url = []

            all_story_data = []
            for i in sorted_data_set:
                story_urls = []
                thumbnail_temp = {}
                thumbnail_temp['url'] = i['thumbnail']
                story_title_url.append(thumbnail_temp)

                all_links = i['source_link'].split(",")

                stories_dict = {}

                for link in all_links:
                    temp2 = {}
                    if link.lower().endswith(('.png', '.jpg', '.jpeg')):
                        temp2['type'] = 'IMAGE'
                        temp2['url'] = link
                        story_urls.append(temp2)
                    elif link.lower().endswith(('.mp4','.mov','.avi','.wmv','.mkv')):
                        temp2['type'] = 'VIDEO'
                        temp2['url'] = link
                        story_urls.append(temp2)

                stories_dict['story_urls'] = story_urls
                all_story_data.append(stories_dict)

            return Response({"message":"Fetched successfully.","data":all_story_data,"story_title_url":story_title_url},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            query_object1 = Stories.objects.filter(id=request.data['id']).update(
                title_english = request.data['title_english'],
                title_telugu = request.data['title_telugu'],
                source_link = request.data['source_link'],
                thumbnail = request.data['thumbnail'],
                tags = request.data['tags'],
                user_id = request.data['user_id'],
                published = request.data['published'])

            return Response({"message":"Updated successfully.","data":request.data},status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def publish(self, request, *args, **kwargs):
        try:
            query_object1 = Stories.objects.filter(id=request.data['id']).update(
                published = request.data['published'])

            return Response({"message":"Updated successfully.","data":request.data},status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request,pk, *args, **kwargs):
        try:
            query_object = Stories.objects.filter(id=pk)
            query_object.delete()
            return Response({"message":"Deleted successfully."},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def all_stories(self, request, *args, **kwargs):
        try:
            query_object1 = Stories.objects.all()
            unserialized_query_object1 = StoriesSerializer(query_object1,many =True)
            data_set = sorted(unserialized_query_object1.data,key = lambda x:x['created_date'],reverse=True)

            return Response({"message":"Fetched successfully.","data":data_set},status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def story_by_id(self, request,pk, *args, **kwargs):
        try:
            query_object1 = Stories.objects.filter(id=pk)
            unserialized_query_object1 = StoriesSerializer(query_object1,many =True)

            return Response({"message":"Fetched successfully.","data":unserialized_query_object1.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BannersAPI(viewsets.ModelViewSet):     
    queryset = Banners.objects.all()
    serializer_class = BannersSerializer
    authentication_classes = [CustomAuthentication]
    
    def upload_banners(self, request, *args, **kwargs):
        ACCESS_KEY_ID = 'AKIAWX46IY3CQVLKK2J2'
        SECRET_ACCESS_KEY = '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'
        Bucket = 'dev-tdp-feed'
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
    
        url_data_set = []
        files = request.data['files']
        
        for i in files:
            file_extension = i['file_extension']
            file_type = i['file_type']
            data = i['data']
            
            try:
            # if 1:
                now = datetime.now()
                current_time_date = now.strftime("%y%m%d%M%H%S%f")
                file_name = current_time_date+"."+file_extension
                decoded_data = base64.b64decode(data)
                
                if file_type == 'IMAGE':

                    bytes_data = io.BytesIO(decoded_data)

                    s3.upload_fileobj(bytes_data, Bucket, "banners/"+file_name,ExtraArgs={'ContentType': "image/"+file_extension})
                    bucket_location = s3.get_bucket_location(Bucket=Bucket)
                    object_url = "https://{1}.s3.{0}.amazonaws.com/banners/{2}".format(bucket_location['LocationConstraint'],Bucket,file_name)
                
                elif file_type == 'VIDEO':
                    bytes_data = io.BytesIO(decoded_data)
                    s3.upload_fileobj(bytes_data, Bucket,"banners/"+file_name,ExtraArgs={'ContentType': "video/"+file_extension})
                    bucket_location = s3.get_bucket_location(Bucket=Bucket)
                    object_url = "https://{1}.s3.{0}.amazonaws.com/banners/{2}".format(bucket_location['LocationConstraint'],Bucket,file_name)
                
                url_data_set.append(object_url)

            except Exception as e:
                print(e)

        return Response({"message":"Uploaded successfully.","data":url_data_set},status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            serializer = BannersSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({"message":"Posted successfully.","data":serializer.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, *args, **kwargs):
        try:
            query_object1 = Banners.objects.filter(published=True)
            unserialized_query_object1 = BannersSerializer(query_object1,many =True)
            full_data = json.loads(json.dumps(unserialized_query_object1.data))
            print(full_data)
            all_banners_data = []
            for i in full_data: # for posts
                all_links = i['source_link'].split(",")
                for link in all_links: # for links inside
                    temp2 = {}
                    if link.lower().endswith(('.png', '.jpg', '.jpeg')):
                        temp2['url'] = link
                        all_banners_data.append(temp2)

            return Response({"message":"Fetched successfully.","data":all_banners_data},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            query_object1 = Banners.objects.filter(id=request.data['id']).update(
                title_english = request.data['title_english'],
                source_link = request.data['source_link'],
                user_id = request.data['user_id'],
                published = request.data['published'])

            return Response({"message":"Updated successfully.","data":request.data},status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def publish(self, request, *args, **kwargs):
        try:
            query_object1 = Banners.objects.filter(id=request.data['id']).update(
                published = request.data['published'])

            return Response({"message":"Updated successfully.","data":request.data},status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request,pk, *args, **kwargs):
        try:
            query_object = Banners.objects.filter(id=pk)
            query_object.delete()
            return Response({"message":"Deleted successfully."},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def all_banners(self, request, *args, **kwargs):
        try:
            query_object1 = Banners.objects.all()
            unserialized_query_object1 = BannersSerializer(query_object1,many =True)
            data_set = sorted(unserialized_query_object1.data,key = lambda x:x['created_date'],reverse=True)
            
            return Response({"message":"Fetched successfully.","data":data_set},status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def banner_by_id(self, request,pk, *args, **kwargs):
        try:
            query_object1 = Banners.objects.filter(id=pk)
            unserialized_query_object1 = BannersSerializer(query_object1,many =True)

            return Response({"message":"Fetched successfully.","data":unserialized_query_object1.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PollsAPI(viewsets.ModelViewSet):     
    queryset = Polls.objects.all()
    serializer_class = PollsSerializer
    authentication_classes = [CustomAuthentication]
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = PollsSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({"message":"Poll created successfully.","data":serializer.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def user_poll(self, request, *args, **kwargs):
        try:
            payload = CustomAuthentication.authenticate(self,request)
            logged_in_user = str(payload[0]['id'])
            # print(logged_in_user)

            poll_id = request.data['id']
            user_option = request.data['option']

            query_object1 = Polls.objects.filter(id = poll_id)
            unserialized_query_object1 = PollsSerializer(query_object1,many =True)

            polled_users = unserialized_query_object1.data[0]['polled_users']

            if logged_in_user in polled_users.keys():
                return Response({"message":"You have already polled","data":request.data},status=status.HTTP_200_OK)


            options_english_dict =unserialized_query_object1.data[0]['options_english']
            options_telugu_dict =unserialized_query_object1.data[0]['options_telugu']
            
            temp1 = options_english_dict
            temp2 = options_telugu_dict

            temp1[user_option+'_count'] = options_english_dict[user_option+'_count']+1
            temp2[user_option+'_count'] = options_telugu_dict[user_option+'_count']+1

            polled_users[logged_in_user] = True
            
            query_object2 = Polls.objects.filter(id=request.data['id']).update(
                options_english = temp1,
                options_telugu = temp2,
                polled_users = polled_users)
                
            return Response({"message":"Polled successfully.","data":request.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request,*args, **kwargs):
        try:
            payload = CustomAuthentication.authenticate(self,request)
            logged_in_user = str(payload[0]['id'])
            now = datetime.now()
            query_object1 = Polls.objects.filter(start_date__lte = now, end_date__gte =now)
            unserialized_query_object1 = PollsSerializer(query_object1,many =True)
            full_data = json.loads(json.dumps(unserialized_query_object1.data))

            poll_data = []
            for i in full_data:
                temp = {}
                temp = i
                temp['total_count'] = len(i['polled_users'])
                temp['user_polled'] = True if logged_in_user in i['polled_users'] else False
                temp['shared_thoughts'] = True if logged_in_user in i['thoughts'] else False
                
                temp.pop('polled_users')
                temp.pop('thoughts')
                poll_data.append(temp)

            final_poll_data = sorted(poll_data,key = lambda x:x['created_date'],reverse=True)

            return Response({"message":"Fetched successfully.","data":final_poll_data},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            query_object1 = Polls.objects.filter(id=request.data['id']).update(
                question_english = request.data['question_english'],
                options_english = request.data['options_english'],
                question_telugu = request.data['question_telugu'],
                published = request.data['published'],
                start_date = request.data['start_date'],
                end_date = request.data['end_date']
                )

            return Response({"message":"Updated successfully.","data":request.data},status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def publish(self, request, *args, **kwargs):
        try:
            query_object1 = Polls.objects.filter(id=request.data['id']).update(
                published = request.data['published'])

            return Response({"message":"Updated successfully.","data":request.data},status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request,pk, *args, **kwargs):
        try:
            query_object = Polls.objects.filter(id=pk)
            query_object.delete()
            return Response({"message":"Deleted successfully."},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def all_polls(self, request, *args, **kwargs):
        try:
            query_object1 = Polls.objects.all()
            unserialized_query_object1 = PollsSerializer(query_object1,many =True)
            return Response({"message":"Fetched successfully.","data":unserialized_query_object1.data},status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def poll_by_id(self, request,pk, *args, **kwargs):
        try:
            query_object1 = Polls.objects.filter(id=pk)
            unserialized_query_object1 = PollsSerializer(query_object1,many =True)

            return Response({"message":"Fetched successfully.","data":unserialized_query_object1.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def poll_thoughts(self, request, *args, **kwargs):
        try:
            query_object1 = Polls.objects.filter(id=request.data['id'])
            unserialized_query_object1 = PollsSerializer(query_object1,many =True)

            payload = CustomAuthentication.authenticate(self,request)
            logged_in_user = str(payload[0]['id'])

            if logged_in_user in unserialized_query_object1.data[0]['thoughts']:
                return Response({"message":"You have already posted your thoughts"},status=status.HTTP_200_OK)

            thoughts_data = unserialized_query_object1.data[0]['thoughts']
            thoughts_data[logged_in_user] = request.data['body']
            query_object2 = Polls.objects.filter(id=request.data['id']).update(thoughts = thoughts_data)
            
            return Response({"message":"Thought posted successfully.","data":request.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def download_poll_users(self, request,pk):
        try:
            s3 = boto3.client('s3', aws_access_key_id='AKIAWX46IY3CQVLKK2J2', aws_secret_access_key='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')
            bucket_name = 'dev-tdp-feed'
            file_name = 'polldata.csv'

            poll_data = {}
            query_object1 =  list(Polls.objects.filter(id=pk).values_list('polled_users', flat=True))
            
            if query_object1:
                userdata = []
                for i in query_object1:
                    for j in i:
                        userdata.append(int(j))

                query_object2 = list(Users.objects.filter(id__in=userdata).values_list('id','name'))

                final_users = []
                for i in query_object2:
                    temp = {}
                    temp['id'] = i[0]
                    temp['name'] = i[1]
                    final_users.append(temp)

                json_data=json.loads(json.dumps(final_users))

                contents = write_CSV(json_data)
                s3.put_object(Body=contents, Bucket='dev-tdp-feed', Key=file_name)

                object_name = "polldata.csv"

                bucket_location = s3.get_bucket_location(Bucket=bucket_name)
                object_url = "https://{1}.s3.{0}.amazonaws.com/{2}".format(bucket_location['LocationConstraint'],bucket_name,object_name)
                return Response({"message":"uploaded successfully","data":object_url},status=status.HTTP_200_OK)
            else:
                return Response({"message":"no data found"},status=status.HTTP_200_OK)


        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def download_all_thoughts(self, request,pk):
        try:
            s3 = boto3.client('s3', aws_access_key_id='AKIAWX46IY3CQVLKK2J2', aws_secret_access_key='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')
            bucket_name = 'dev-tdp-feed'
            file_name = 'thoughtsdata.csv'

            query_object1 =  list(Polls.objects.filter(id=pk).values_list('thoughts', flat=True))
            # print(query_object1)
            if query_object1:
                final_users = []
                for i in query_object1:
                    di = i.items()
                    for j in di:
                        # print(j)

                        temp = {}
                        temp['id'] = j[0]
                        temp['thought'] = j[1]
                        
                        final_users.append(temp)

                json_data=json.loads(json.dumps(final_users))

                contents = write_CSV(json_data)
                s3.put_object(Body=contents, Bucket='dev-tdp-feed', Key=file_name)

                object_name = "thoughtsdata.csv"

                bucket_location = s3.get_bucket_location(Bucket=bucket_name)
                object_url = "https://{1}.s3.{0}.amazonaws.com/{2}".format(bucket_location['LocationConstraint'],bucket_name,object_name)
                return Response({"message":"uploaded successfully","data":object_url},status=status.HTTP_200_OK)
            else:
                return Response({"message":"no data found"},status=status.HTTP_200_OK)


        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            
    def recent_thoughts(self, request,pk):
        try:
            query_object1 =  Polls.objects.filter(id=pk)
            unserialized_query_object1 = PollsSerializer(query_object1,many =True)

            if query_object1:
                data = unserialized_query_object1.data[0]['thoughts']
                return Response({"message":"uploaded successfully","data":data},status=status.HTTP_200_OK)
            else:
                return Response({"message":"no data found"},status=status.HTTP_200_OK)


        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)