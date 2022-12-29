from django.shortcuts import render,redirect
# Create your views here.
from django.contrib.auth.hashers import make_password,check_password
# password=''
# hashed_pwd=make_password(password)
# check_password(password,hashed_pwd)
from .models import Admins,Districts,Assemblies,PadayatraSchedule
from django.contrib import messages
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

# def admin_login(request):
#     if request.method=="POST":
#         user_name=request.POST['username']
#         password=request.POST['password']
#         print(user_name,password)
#         if Admins.objects.filter(user_name=user_name).exists():
#             ad_password=Admins.objects.get(user_name=user_name).password
#             if check_password(password,ad_password):
#                 return redirect('dashboard')
#             else:
#                 messages.error(request,"Incorrect Password")
#                 return redirect('signin')
#         else:
#             messages.error(request,"User Not Found")
#             return redirect('signin')


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
 

def create_story(request,username):
    user=Admins.objects.get(user_name=username)
    return render(request,'create-stories.html',{"user":user})

import requests
import io
import base64
from PIL import Image

def upload_post(request):
    if request.method=="POST":

        images=request.FILES.getlist('files')
        for image in images:
            print(image.file)
            img=Image.open(image.file)
            print("======img=========",img.format)
      

        # response=requests.post('http://localhost:8000/feed/upload-file',data=file)

    print("====else============")

def create_banner(request,username):
    user=Admins.objects.get(user_name=username)
    return render(request,'create-banner.html',{"user":user})
    

def view_padayatra_list(request,username):
    user=Admins.objects.get(user_name=username)
    return render(request,'list-padayatra.html',{"user":user})
        



def schedule_padayatra(request,username):
    user=Admins.objects.get(user_name=username)
    return render(request,'schedule-padayatra.html',{"user":user})
   

import datetime
from django.views.decorators.csrf import csrf_exempt

def edit_padayatra(request,username):
    user=Admins.objects.get(user_name=username)

    return render(request,'edit-schedule.html',{"user":user})
    

def users(request,username):
    user=Admins.objects.get(user_name=username)
    return render(request,'users.html',{"user":user})
  


def admin_logout(request,username):
   
    return redirect('signin')



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from . import serializers
@api_view(['GET','POST'])
def admin_sign_api(request):
    if request.method=="GET":
        return Response({"message": "Hello, world!"})
    if request.method == 'POST':
        data=request.data['username']
        user_name=request.data['username']
        password=request.data['password']
        if Admins.objects.filter(user_name=user_name).exists():
            ad_password=Admins.objects.get(user_name=user_name).password
            if check_password(password,ad_password):
                return Response({"message":"Login Success","status":"True"})
            else:
                return Response({"message":"Incorrect Password","status":"False"})
        else:
            return Response({"message":"User Not Found","status":'False'})

    return Response({"message": "Hello, Iam Sorry Get Method is Not Allowed"})

dict={'Chittoor': ['Kuppam', 'Palamaneru', 'Puthalapattu', 'Chittoor', 'GD Nellore', 'Nagari', 'Chandragiri'], 'Tirupati': ['Satyavedu', 'Srikalahasti', 'Tirupati', 'Venkatagiri', 'Gudur', 'Sarvepalli'], 'Rajampet': ['Punganuru', 'Pileru', 'Madanapalle', 'Thamballapalle', 'Rajampet', 'Kodur'], 'Hindupur': ['Kadiri', 'Dharmavaram', 'Puttaparthi', 'Penukonda', 'Hindupur', 'Raptadu'], 'Anantapur': ['Kalyandurg', 'Uravakonda', 'Anantapur', 'Singanamala', 'Tadipatri', 'Guntakal'], 'Nandyal': ['Dhone', 'Panyam', 'Nandyal', 'Banaganapalle', 'Allagadda'], 'Kurnool': ['Pattikonda', 'Alur', 'Adoni', 'Mantralayam', 'Yemmiganur', 'Kodumur', 'Kurnool'], 'Kadapa': ['Proddatur', 'Mydukur', 'Kamalapuram', 'Kadapa', 'Badvel'], 'Nellore': ['Nellore city', 'Kovur', 'Kavali', 'Atmakur', 'Udayagiri'], 'Ongole': ['Kanigiri', 'Markapuram', 'Kondepi', 'Ongole'], 'Bapatla': ['Santhanuthalapadu', 'Addanki', 'Parchur', 'Chirala', 'Bapatla', 'Repalle', 'Vemuru'], 'Machilipatnam': ['Avanigadda', 'Gannavaram', 'Penamaluru', 'Pamarru', 'Gudiwada'], 'Guntur': ['Tenali', 'Ponnur', 'Guntur East', 'Guntur West', 'Tadikonda', 'Mangalagiri'], 'Narsaraopeta': ['Chilakaluripeta', 'Narsaraopeta', 'Sattenapalli', 'Pedakurapadu'], 'Vijayawada': ['Nandigama', 'Mylavaram', 'Vijayawada West'], 'Eluru': ['Kaikalur', 'Eluru', 'Denduluru', 'Unguturu'], 'Rajahmundry': ['Gopalpuram', 'Nidudavole', 'Kovvur', 'Rajahmundry city', 'Rajahmundry Rural'], 'Narsapuram': ['Tadepalligudem', 'Tanuku'], 'Amalapuram': ['Mandapeta', 'Ramachandrapuram'], 'Kakinada': ['Kakinada Rural', 'Kakinada City', 'Pithapuram', 'Tuni'], 'Anakapalli': ['Payakraopet', 'Narsipatnam', 'Yelamanchili', 'Anakapalli', 'Chodavaram', 'Madugula', 'Pendurthi'], 'Vizag': ['Gajuwaka', 'Vizag South', 'Vizag North', 'Bhimili', 'Srungavarapukota'], 'Vizianagaram': ['Gajapathinagaram', 'Vizianagaram', 'Nellimarla', 'Etcherla', 'Rajam'], 'Srikakulam': ['Srikakulam', 'Amadalavalasa', 'Pathapatnam', 'Narsannapeta', 'Tekkali', 'Palasa', 'Icchapuram'], 'Araku': ['Palakonda']}




class DistrictData(generics.ListAPIView):
    queryset=Districts.objects.all()
    serializer_class=serializers.DistrictsSerializer


class AssembliesData(generics.ListAPIView):
    queryset=Assemblies.objects.all()
    serializer_class=serializers.AssemblySerializer


# =======================
    # def get_queryset(self):
    #     if Assemblies.objects.count()==0:
    #         createlocations()
    #     return Assemblies.objects.all()
# =======================

# def createlocations():
#     for k,v in dict.items():
#         if Districts.objects.filter(name=k).exists():
#             pass
#         else:
#             district=Districts.objects.create(name=k)
#             district.save()
#             print("districxt saved")
#         if Assemblies.objects.filter(name=v,district=k).exists():
#             pass
#         else:
#             for i in v:
#                 ass=Assemblies.objects.create(name=i,district=k)
#                 ass.save()
#             print('Assembly saved')
#     return Response({"message": "Hello, world!"})

@api_view(['GET'])
def get_padayatra_registrate(request):
    if request.method=="GET":
        my_dict={}
        districts=Districts.objects.all()
        for i in districts:
            users=0
            req=PadayatraSchedule.objects.filter(district=i.name)
            for each in req:
                users+=each.registered_users_count
            my_dict[i.name]=users

        return Response(my_dict)
from Feed.models import Posts
from Users.models import Users
@api_view(['GET'])
def get_dashboard_stats(request):
    if request.method=="GET":
        total_posts=Posts.objects.count()
        total_users=Users.objects.count()
        total_sharing=0
        posts=Posts.objects.all()
        for post in posts:
            total_sharing+=post.shares_count
        return Response({"total_users":total_users,"total_posts":total_posts,"total_sharing":total_sharing})
    return Response({"message":"Method not allowed"})







from rest_framework import viewsets
from .serializers import AssemblySerializer


class AcViewSet(viewsets.ModelViewSet):
    # queryset=AssemblyConstituencies.objects.all()
    serializer_class=AssemblySerializer

    def get_queryset(self):
        district_name=self.kwargs['district']
        return Assemblies.objects.filter(district=district_name)

class PadayatraScheduleViewSet(viewsets.ModelViewSet):
    queryset=PadayatraSchedule.objects.all()
    serializer_class=serializers.PadayatraSerializer

    

