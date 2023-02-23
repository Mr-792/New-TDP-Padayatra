from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password,check_password
from .models import Admins,PadayatraSchedule
from .serializers import *
from django.contrib import messages
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.core.exceptions import *
import json
from django.utils.dateparse import parse_datetime
from Feed.models import *
from Feed.serializers import *
from Users.models import *
from Users.serializers import *
from datetime import datetime
import requests

from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password,check_password


def sign_in_form(request):
    if Admins.objects.filter(is_superadmin=1).count()==0:
        password=make_password('superadmin')
        admin=Admins.objects.create(user_name="superadmin",password=password,is_superadmin=True)
        admin.save()
    if Admins.objects.filter(is_manager=1).count()==0:
        password=make_password('manager')
        admin=Admins.objects.create(user_name="manager",password=password,is_manager=True)
        admin.save()
    if Admins.objects.filter(is_supervisor=1).count()==0:
        password=make_password('supervisor')
        admin=Admins.objects.create(user_name="supervisor",password=password,is_supervisor=True)
        admin.save()
    return render(request,'sign-in.html')


def admin_dashboard(request,username):
    user=Admins.objects.get(user_name=username)
    return render(request,'index.html',{"user":user})
    

def view_posts(request,username):
    user=Admins.objects.get(user_name=username)
    return render(request,'posts-list.html',{"user":user})

def view_stories(request,username):
    user=Admins.objects.get(user_name=username)
    return render(request,'stories.html',{"user":user})

def view_banners(request,username):
    user=Admins.objects.get(user_name=username)
    return render(request,'banners.html',{"user":user})
  
def create_post(request,username):
    user=Admins.objects.get(user_name=username)
    return render(request,'create-post.html',{"user":user})
 
  
def edit_post(request,username,id):
    user=Admins.objects.get(user_name=username)
    return render(request,'edit-post.html',{"user":user,"id":id})
 

def create_story(request,username):
    user=Admins.objects.get(user_name=username)
    return render(request,'create-stories.html',{"user":user})

def edit_story(request,username,id):
    user=Admins.objects.get(user_name=username)
    return render(request,'edit-stories.html',{"user":user,"id":id})

def create_banner(request,username):
    user=Admins.objects.get(user_name=username)
    return render(request,'create-banner.html',{"user":user})

def edit_banner(request,username,id):
    user=Admins.objects.get(user_name=username)
    return render(request,'edit-banner.html',{"user":user,"id":id})
  

def view_padayatra_list(request,username):
    user=Admins.objects.get(user_name=username)
    return render(request,'list-padayatra.html',{"user":user})
        



def schedule_padayatra(request,username):
    user=Admins.objects.get(user_name=username)
    return render(request,'schedule-padayatra.html',{"user":user})
   


def edit_padayatra(request,username,id):
    user=Admins.objects.get(user_name=username)

    return render(request,'edit-schedule.html',{"user":user,"id":id})
    

def users(request,username):
    user=Admins.objects.get(user_name=username)
    return render(request,'users.html',{"user":user})

def connect_with_nl(request,username):
    user=Admins.objects.get(user_name=username)

    return render(request,'connectwithNL.html',{"user":user})

def view_poll(request,username,id):
    user=Admins.objects.get(user_name=username)
    return render(request,'view-poll.html',{"user":user,"id":id})

def createpoll(request,username):
    user=Admins.objects.get(user_name=username)
    return render(request,'createpoll.html',{"user":user})

def edit_poll(request,username,id):
    user=Admins.objects.get(user_name=username)
    return render(request,'edit-poll.html',{"user":user,"id":id})
    
def live(request,username):
    user=Admins.objects.get(user_name=username)
    return render(request,'live.html',{"user":user})

def admin_logout(request,username):
    return redirect('signin')

def verified(request):
    return render(request,'verified.html')

def sendNotification(request,username):    
    user=Admins.objects.get(user_name=username)    
    return render(request,'send-notification.html',{'user':user})

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from . import serializers
from YuvaGallam.customauth import CustomAuthentication
import jwt, datetime 
from YuvaGallam.settings import SECRET_KEY

import jwt
import json
import datetime
class admin_sign_in(viewsets.ModelViewSet):

    def sign_in(self,request,*args):
        json_data=json.loads(json.dumps(request.data))
        username=json_data['username']
        password=json_data['password']

        if Admins.objects.filter(user_name=username).exists():
            ad_password=Admins.objects.get(user_name=username).password
            if check_password(password,ad_password):
                payload = {
                    'id': 1,
                    'name':username,
                    'role':username,
                    'iat': datetime.datetime.utcnow()
                    }
                token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
                print(token)
                return Response({"message":"Login Success","status":"True","token":token})
            else:
                return Response({"message":"Incorrect Password","status":"False"})
        else:
            return Response({"message":"User Not Found","status":'False'})


class PadayatraScheduleAPI(viewsets.ModelViewSet):
    queryset = PadayatraSchedule.objects.all()
    serializer_class = PadayatraScheduleSerializer
    authentication_classes = [CustomAuthentication] 

    def create(self, request, *args, **kwargs):
        try:
            serializer = PadayatraScheduleSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({"message":"Scheduled successfully.","data":serializer.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def retrieve(self, request, pk, *args, **kwargs):
        try:
            query_object1 = PadayatraSchedule.objects.filter(id=pk)
            unserialized_query_object1 = PadayatraScheduleSerializer(query_object1,many =True)

            return Response({"message":"Fetched successfully.","data":unserialized_query_object1.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            query_object = PadayatraSchedule.objects.filter(id=request.data['id']).update(
                title = request.data['title'],
                district = request.data['district'],
                source_link = request.data['source_link'],
                assembly = request.data['assembly'],
                village = request.data['village'],
                start_point = request.data['start_point'],
                start_date = request.data['start_date'],
                end_date = request.data['end_date'],
                status = request.data['status'],
                )
            return Response({"message":"Updated successfully.","data":request.data},status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request,pk, *args, **kwargs):
        try:
            query_object = PadayatraSchedule.objects.filter(id=pk)
            query_object.delete()
            return Response({"message":"Deleted successfully."},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PadayatraSearchAPI(viewsets.ModelViewSet):
    authentication_classes = [CustomAuthentication] 

    def all_districts(self, request, *args, **kwargs):
        try:
    #         query_object1 = PadayatraSchedule.objects.all()
    #         unserialized_query_object1 = PadayatraScheduleSerializer(query_object1,many =True)

    #         return Response({"message":"Fetched successfully.","data":unserialized_query_object1.data},status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def all_districts_mobile(self, request, *args, **kwargs):
    #     try:
            query_object1 = Districts.objects.all().values('district','source_link')
            unserialized_query_object1 = DistrictsSerializer(query_object1,many =True)
            all_districts = []

            for i in unserialized_query_object1.data:
                records = PadayatraSchedule.objects.filter(district=i['district'])
                if records:
                    first_record_start_date = records.order_by('start_date').first().start_date
                    last_record_end_date = records.order_by('-end_date').first().end_date
                    temp = {
                        'district':i['district'],
                        'source_link':i['source_link'],
                        'start_date': first_record_start_date,
                        'end_date': last_record_end_date,
                    }
                    all_districts.append(temp)

            return Response({"message":"Fetched successfully.","data":all_districts},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def search_district(self, request, district, *args, **kwargs):
        try:
            query_object1 = PadayatraSchedule.objects.filter(district=district)
            unserialized_query_object1 = PadayatraScheduleSerializer(query_object1,many =True)

            data = []
            for i in unserialized_query_object1.data:
                temp = {}
                records = PadayatraSchedule.objects.filter(assembly=i['assembly'])
                if records:
                    first_record_start_date = records.order_by('start_date').first().start_date
                    last_record_end_date = records.order_by('-end_date').first().end_date
                    temp = {
                        'assembly':i['assembly'],
                        'source_link':i['source_link'],
                        'start_date': first_record_start_date,
                        'end_date': last_record_end_date,
                    }
                if temp not in data:
                    data.append(temp)
            
            return Response({"message":"Fetched successfully.","data":data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

    
    def search_assembly(self, request, assembly, *args, **kwargs):
        try:
            payload = CustomAuthentication.authenticate(self,request)
            logged_in_user = str(payload[0]['id'])
            query_object1 = PadayatraSchedule.objects.filter(assembly=assembly)
            unserialized_query_object1 = PadayatraScheduleSerializer(query_object1,many =True)
            
            temp_data1 = json.loads(json.dumps(unserialized_query_object1.data))
            date_wise_sorted_data_set = sorted(temp_data1,key = lambda x:x['end_date'],reverse=True)

            import datetime

            now = datetime.datetime.now()
            data = []
            for i in date_wise_sorted_data_set:
                temp = {}
                temp['id'] = i['id']
                temp['assembly'] = i['assembly']
                temp['source_link'] = i['source_link']
                temp['village'] = i['village']
                temp['start_point'] = i['start_point']
                temp['start_date'] = i['start_date']
                temp['end_date'] = i['end_date']

                from datetime import datetime

                date_string = i['end_date']
                date_format = "%Y-%m-%dT%H:%M:%SZ"
                end_date_time = datetime.strptime(date_string, date_format)


                if end_date_time > now:
                    temp['is_completed'] = False
                else:
                    temp['is_completed'] = True

                temp['padayatra_link'] = i['padayatra_link']
                temp['is_registered'] = True if logged_in_user in i['registered_users'] else False
                data.append(temp)

            return Response({"message":"Fetched successfully.","data":data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def all_districts_web(self, request, *args, **kwargs):
        try:
            query_object1 = PadayatraSchedule.objects.all()
            unserialized_query_object1 = PadayatraScheduleSerializer(query_object1,many =True)

            full_data = json.loads(json.dumps(unserialized_query_object1.data))
            sorted_data_set = sorted(full_data,key = lambda x:x['status'],reverse=True)
            
            return Response({"message":"Fetched successfully.","data":sorted_data_set},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def all_padayatra_mobile(self, request, *args, **kwargs):
        # try:
            from datetime import datetime
            from datetime import date

            payload = CustomAuthentication.authenticate(self,request)
            logged_in_user = str(payload[0]['id'])
            now = datetime.now()
            today = date.today()
            
            date_format = "%Y-%m-%d"

            query_object1 = PadayatraSchedule.objects.filter(start_date__gte = today)
            unserialized_query_object1 = PadayatraScheduleSerializer(query_object1,many =True)
            
            temp_data1 = json.loads(json.dumps(unserialized_query_object1.data))
            date_wise_sorted_data_set = sorted(temp_data1,key = lambda x:x['start_date'])

            import datetime

            data = []
            for i in date_wise_sorted_data_set:
                temp = {}
                temp['id'] = i['id']
                temp['district'] = i['district']
                temp['assembly'] = i['assembly']
                temp['source_link'] = i['source_link']
                temp['village'] = i['village']
                temp['start_point'] = i['start_point']
                temp['start_date'] = i['start_date']
                temp['end_date'] = i['end_date']


                date_string = i['end_date']
                date_format = "%Y-%m-%dT%H:%M:%SZ"
                from datetime import datetime

                end_date_time = datetime.strptime(date_string, date_format)


                if end_date_time > now:
                    temp['is_completed'] = False
                else:
                    temp['is_completed'] = True

                temp['padayatra_link'] = i['padayatra_link']
                temp['is_registered'] = True if logged_in_user in i['registered_users'] else False
                data.append(temp)

            return Response({"message":"Fetched successfully.","data":data},status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DashboardAPI(viewsets.ModelViewSet):    
    authentication_classes = [CustomAuthentication] 

    def dashboard(self, request, *args, **kwargs):
        try:
            data = {}
            data['all_users'] = Users.objects.all().count()
            data['all_posts'] = Posts.objects.all().count()
            data['all_stories'] = Stories.objects.all().count()
            data['all_banners'] = Banners.objects.all().count()

            data['all_padayatra_districts'] = Districts.objects.all().count()
            query_object1 = PadayatraSchedule.objects.all() 
            unserialized_query_object1  = PadayatraScheduleSerializer(query_object1,many =True)
            data['all_padayatra_schedules'] = unserialized_query_object1.data
            return Response({"message":"Fetched successfully.","data":data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def push_notification(self, request, *args, **kwargs):
        try:

            headers = {
                "Authorization": "key=AAAAeuQtz7Y:APA91bFDLvVptXFHkA7FG7fXkz9A0fkRp4brlDRI1HoH2iAzHVRPKBOTMSKchNufM21uqT2K6unZZOgjl29VVJO5LsAqq8nnpQBMGGpE1TgO0W3Sx7gf69pbtsfkS2LZ8gSkYT6RRtKh",
                "Content-Type": "application/json"
            }

            title = request.data['title']
            message = request.data['message']
            type = request.data['type']

            if type !='padayatra':
                
                to = type

                body = {"priority": "high","sound": True,
                        "data": {
                            "click_action": "FLUTTER_NOTIFICATION_CLICK",
                            "type": to
                        },
                        "notification": {
                            "body":message,
                            "title": title
                        },
                        "to" : "/topics/"+to
                        }
            else:
                to = ""
                district = request.data['district']
                if 'assembly' in request.data:
                    assembly = request.data['assembly']
                    to = assembly
                else:
                    to = district

                body = {
                        "priority": "high",
                        "sound": True,
                        "data": {
                            "click_action": "FLUTTER_NOTIFICATION_CLICK",
                            "type": "padayatra"
                        },
                        "notification": {
                            "body": message,
                            "title": title
                        },
                        "to" : "/topics/"+to
                    }

            response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))

            if response.status_code == 200:
                return Response({"message":"Notification send successfully."},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class YoutubeURLsAPI(viewsets.ModelViewSet):
    queryset = YoutubeURLs.objects.all()
    serializer_class = YoutubeURLsSerializer
    authentication_classes = [CustomAuthentication] 

    def create(self, request, *args, **kwargs):
        try:
            serializer = YoutubeURLsSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({"message":"Posted successfully.","data":serializer.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            query_object1 = YoutubeURLs.objects.all()
            unserialized_query_object1 = YoutubeURLsSerializer(query_object1,many =True)

            return Response({"message":"Fetched successfully.","data":unserialized_query_object1.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            query_object = YoutubeURLs.objects.filter(id=request.data['id']).update(
                live_url = request.data['live_url'],
                Addational_Video_url1 = request.data['Addational_Video_url1'],
                Addational_Video_url2 = request.data['Addational_Video_url2'],
                Addational_Video_url3 = request.data['Addational_Video_url3'],
                Addational_Video_url4 = request.data['Addational_Video_url4'],
                Addational_Video_url5 = request.data['Addational_Video_url5']
                )
            return Response({"message":"Updated successfully.","data":request.data},status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request,pk, *args, **kwargs):
        try:
            query_object = YoutubeURLs.objects.filter(id=pk)
            query_object.delete()
            return Response({"message":"Deleted successfully."},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status":500,"msg":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
