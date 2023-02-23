# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import datetime
from .models import *
from .serializers import *
from Admins.models import *
from Admins.serializers import *
from Users.utilities import *
import jwt, datetime
import boto3
import csv
from io import StringIO
from YuvaGallam.settings import SECRET_KEY
from Admins.models import PadayatraSchedule
from Admins.serializers import PadayatraScheduleSerializer
from YuvaGallam.customauth import CustomAuthentication
from Users.utilities import write_CSV

class DistrictsAPI(viewsets.ModelViewSet):

    def all_districts(request,varargs):
        try:
            query_object = Districts.objects.all()
            unserialized_query_object = DistrictsSerializer(query_object,many =True) 
            return Response({"message":"all districts","data":unserialized_query_object.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfessionAPI(viewsets.ModelViewSet):

    def all_professions(request,varargs):
        try:
            query_object = Professions.objects.all()
            unserialized_query_object = ProfessionSerializer(query_object,many =True) 
            return Response({"message":"all Professions","data":unserialized_query_object.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AssembliesAPI(viewsets.ModelViewSet):
    queryset = Assemblies.objects.all()
    serializer_class = AssembliesSerializer
    
    def all_assemblies(request,varargs):
        try:
            query_object = Assemblies.objects.all()
            unserialized_query_object = AssembliesSerializer(query_object,many =True) 
            return Response({"message":"all assemblies","data":unserialized_query_object.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def search_assemblies(self, request, district):

        try:
            query_object =  Assemblies.objects.filter(district__icontains=district)
            unserialized_query_object = AssembliesSerializer(query_object,many =True)

            if unserialized_query_object.data:
                return Response({"message":"district wise assemblies","data":unserialized_query_object.data},status=status.HTTP_200_OK) 

        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UsersAPI(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def signup(self, request):
        try:
        # if 1:
            query_object1 =  Users.objects.filter(phone=request.data['phone'],verified=True)
            unserialized_query_object = UsersSerializer(query_object1,many =True)


            if unserialized_query_object.data:
                return Response({"message":"You number is already registered. Please login"},status=status.HTTP_409_CONFLICT)        
            else:
                query_object2 = Users.objects.filter(phone=request.data['phone'],verified=False)
                query_object2.delete()
                otp_response = transmit_otp("91",request.data["phone"])
            
                if otp_response == 200:
                    request.data['role'] ='ENDUSER'
                    request.data['verified'] = False
                    serializer = UsersSerializer(data=request.data)

                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                return Response({"message":"Otp sent to your mobile."},status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def verify_otp(self, request):
        try:
        # if 1:
            now = datetime.datetime.now()

            query_object1 = Otp.objects.filter(phone=request.data['phone']).filter(otp=request.data['otp']).filter(expiry__gte=now)
            unserialized_query_object1 = OtpSerializer(query_object1, many=True)

            if unserialized_query_object1.data:
                data = {}
                query_object2 = Users.objects.filter(phone=request.data['phone'],verified=True)
                unserialized_query_object2 = UsersSerializer(query_object2,many =True)

                print(unserialized_query_object2.data)
                
                if unserialized_query_object2.data:
                    # verifying existing user and sending token as response
                    payload = {
                                'id': unserialized_query_object2.data[0]["id"],
                                'name':unserialized_query_object2.data[0]["name"],
                                'role': unserialized_query_object2.data[0]["role"],
                                'iat': datetime.datetime.utcnow()
                                }
                    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
                    return Response({"message":"Logged in successfully.","id":unserialized_query_object2.data[0]["id"],"user":unserialized_query_object2.data[0]["name"],"phone":unserialized_query_object2.data[0]["phone"],"token":token},status=status.HTTP_200_OK)
                else:
                    # creating a new user and sending token as response
                    query_object3 = Users.objects.filter(phone=request.data['phone']).update(verified=True)

                    query_object4 = Users.objects.filter(phone=request.data['phone'],verified=True)
                    unserialized_query_object4 = UsersSerializer(query_object4,many =True)

                    payload = {
                                'id': unserialized_query_object4.data[0]["id"],
                                'name':unserialized_query_object4.data[0]["name"],
                                'role': unserialized_query_object4.data[0]["role"],
                                'iat': datetime.datetime.utcnow()
                                }
                    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

                    return Response({"message":"Signed up successfully.","id":unserialized_query_object4.data[0]["id"],"user":unserialized_query_object4.data[0]["name"],"phone":unserialized_query_object4.data[0]["phone"],"token":token},status=status.HTTP_200_OK)
            else:
                return Response({"message":"You have entered a wrong OTP."},status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def login(self,request):
        try:
        # if 1:
            query_object = Users.objects.filter(phone=request.data['phone'])
            unserialized_query_object = UsersSerializer(query_object,many =True)

            if unserialized_query_object.data:
                otp_response = transmit_otp("91",request.data["phone"])
                return Response({"message":"Otp sent to your mobile."},status=status.HTTP_200_OK)
            else:
                return Response({"message":"User not registered"},status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def resend_otp(self,request):
        try:
        # if 1:
                otp_response = transmit_otp("91",request.data["phone"])
                print(otp_response)
                if otp_response == 200:
                    return Response({"message":"Otp sent to your mobile."},status=status.HTTP_200_OK)
                else:
                    return Response({"message":"AWS server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def all_users(self, request):
        try:
        # if 1:
            user_data = {}
            query_object1 =  Users.objects.all()
            unserialized_query_object1 = UsersSerializer(query_object1,many =True)
            user_data['user_data'] = unserialized_query_object1.data

            query_object2 = Districts.objects.all()
            unserialized_query_object2 = DistrictsSerializer(query_object2,many =True)
            
            district_wise_users = []
            for i in unserialized_query_object2.data:
                temp = {}
                temp[i['district']]=Users.objects.filter(district=i['district']).count()

                query_object3 = PadayatraSchedule.objects.filter(district = i['district'])
                unserialized_query_object3 = PadayatraScheduleSerializer(query_object3,many = True)
                
                total_district_users = 0
                if unserialized_query_object3.data:
                    
                    for j in unserialized_query_object3.data:
                        total_district_users = total_district_users+j['registered_users_count']
                    temp['padayatra_registered_users'] = total_district_users
                    
                else:
                    temp['padayatra_registered_users'] = 0
                district_wise_users.append(temp)

            user_data['district_wise_users'] = district_wise_users
            return Response({"message":"all users have been fetched successfully.","data":user_data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def download_all_users(self, request):
        try:
            s3 = boto3.client('s3', aws_access_key_id='AKIAWX46IY3CQVLKK2J2', aws_secret_access_key='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')
            bucket_name = 'dev-tdp-feed'
            file_name = 'users.csv'

            user_data = {}
            query_object1 =  Users.objects.all()
            unserialized_query_object1 = UsersSerializer(query_object1,many =True)
            user_data['user_data'] = unserialized_query_object1.data

            stud_data = user_data['user_data']
            json_data=json.loads(json.dumps(stud_data))
            # print(json_data)
            contents = write_CSV(json_data)
            s3.put_object(Body=contents, Bucket='dev-tdp-feed', Key=file_name)

            object_name = "users.csv"

            bucket_location = s3.get_bucket_location(Bucket=bucket_name)
            object_url = "https://{1}.s3.{0}.amazonaws.com/{2}".format(bucket_location['LocationConstraint'],bucket_name,object_name)
            return Response({"message":"uploaded successfully","data":object_url},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PadayatraRegistrationAPI(viewsets.ModelViewSet):
    queryset = PadayatraRegistration.objects.all()
    serializer_class = PadayatraRegistrationSerializer
    authentication_classes = [CustomAuthentication]

    def create(self, request, *args, **kwargs):
        try:
            payload = CustomAuthentication.authenticate(self,request)
            logged_in_user = str(payload[0]['id'])
            serializer = PadayatraRegistrationSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

            query_object1 = PadayatraSchedule.objects.filter(id=request.data['padayatra_id'])
            unserialized_query_object1 = PadayatraScheduleSerializer(query_object1,many =True)
            registered_users = unserialized_query_object1.data[0]['registered_users']
            registered_users[int(logged_in_user)] = True
            query_object2 = PadayatraSchedule.objects.filter(id=request.data['padayatra_id']).update(registered_users=registered_users,registered_users_count=len(registered_users))
            return Response({"message":"Registered successfully.","data":serializer.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request,user_id, *args, **kwargs):
        try:
            query_object1 = PadayatraRegistration.objects.filter(user_id=user_id)
            unserialized_query_object1 = PadayatraRegistrationSerializer(query_object1,many =True)
            
            users_padayatra_list = []
            for i in unserialized_query_object1.data:
                temp = {}
                temp['user_id'] = i['user_id']
                query_object2 = PadayatraSchedule.objects.filter(id=i['padayatra_id'])
                unserialized_query_object2 = PadayatraScheduleSerializer(query_object2,many =True)
                temp['padayatra_details'] = unserialized_query_object2.data[0]
                users_padayatra_list.append(temp)
            return Response({"message":"Fetched successfully.","data":users_padayatra_list},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def update(self, request, *args, **kwargs):
        try:
            query_object1 = PadayatraRegistration.objects.filter(id=request.data['id'],user_id = request.data['user_id']).update(
            padayatra_id = request.data['padayatra_id'])

            return Response({"message":"Updated successfully.","data":request.data},status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, *args, **kwargs):
        try:
            payload = CustomAuthentication.authenticate(self,request)
            logged_in_user = str(payload[0]['id'])
            query_object1 = PadayatraRegistration.objects.filter(id=request.data['id'])
            query_object1.delete()

            query_object2 = PadayatraRegistration.objects.filter(id=request.data['padayatra_id'])
            unserialized_query_object2 = PadayatraScheduleSerializer(query_object2,many =True)
            registered_users = unserialized_query_object2.data[0]['registered_users']
            registered_users.pop(str(logged_in_user))
            query_object = PadayatraRegistration.objects.filter(id=request.data['post_id']).update(registered_users=registered_users,registered_users_count=len(registered_users))

            return Response({"message":"Deleted successfully."},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)