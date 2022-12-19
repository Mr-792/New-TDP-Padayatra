# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import datetime
from .models import *
from .serializers import *
from users.utilities import *


class DistrictsAPI(viewsets.ModelViewSet):

    def all_districts(request,varargs):
        try:
            query_object = Districts.objects.all()
            unserialized_query_object = DistrictsSerializer(query_object,many =True) 
            return Response({"message":"all districts","data":unserialized_query_object.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AssembliesAPI(viewsets.ModelViewSet):

    def all_assemblies(request,varargs):
        try:
            query_object = Assemblies.objects.all()
            unserialized_query_object = AssembliesSerializer(query_object,many =True) 
            return Response({"message":"all assemblies","data":unserialized_query_object.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UsersAPI(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def login(self,request):
        try:
        # if 1:
            query_object = Users.objects.filter(phone=request.data['phone'])
            unserialized_query_object = UsersSerializer(query_object,many =True)

            if unserialized_query_object.data:
                return Response({"message":"Otp sent to your mobile."},status=status.HTTP_200_OK)
            else:
                return Response({"message":"User not registered"},status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def send_otp(self,request):
        try:
        # if 1:
            query_object = Users.objects.filter(phone=request.data['phone'])
            unserialized_query_object = UsersSerializer(query_object,many =True)

            if unserialized_query_object.data:
                return Response({"message":"You are already a registered user."},status=status.HTTP_307_TEMPORARY_REDIRECT)
            else:
                otp_response = transmit_otp("+91",request.data["phone"])
                if otp_response == 200:
                    return Response({"message":"Your OTP has been sent successfully."},status=status.HTTP_200_OK)
                else:
                    return Response({"message":"AWS server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def verify_otp(self, request):
        try:
            now = datetime.datetime.now()

            query_object1 = Otp.objects.filter(phone=request.data['phone']).filter(otp=request.data['otp']).filter(expiry__gte=now)
            unserialized_query_object1 = OtpSerializer(query_object1, many=True)

            if unserialized_query_object1.data:
                data = {}
                query_object2 = Users.objects.filter(phone=request.data['phone'])
                unserialized_query_object2 = UsersSerializer(query_object2,many =True)
                
                if unserialized_query_object2.data:
                    data["name"] = unserialized_query_object2.data[0]["name"]
                    return Response({"message":"Your OTP is verified.","data":data},status=status.HTTP_200_OK)
                else:
                    return Response({"message":"Your OTP is verified."},status=status.HTTP_200_OK)
            else:
                return Response({"message":"You have entered a wrong OTP."},status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def signup(self, request):
        try:
        # if 1:
            query_object =  Users.objects.filter(phone=request.data['phone'])
            unserialized_query_object = UsersSerializer(query_object,many =True)

            if unserialized_query_object.data:
                return Response({"message":"You mobile number is already registered. Please login"},status=status.HTTP_409_CONFLICT)        
            
            request.data['role'] ='ENDUSER'
            serializer = UsersSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
            otp_response = transmit_otp("+91",request.data["phone"])
            return Response({"message":"Account has been created successfully.","data":serializer.data},status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def all_users(self, request):
        try:
        # if 1:
            query_object =  Users.objects.all()
            unserialized_query_object = UsersSerializer(query_object,many =True)

            return Response({"message":"all users have been fetched successfully.","data":unserialized_query_object.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    # def login(self,request):
    #     try:
    #         query_object = Users.objects.filter(phone=request.data['phone'])
    #         unserialized_query_object = UsersSerializer(query_object,many =True)
            
    #             if unserialized_query_object.data:
    #                 # for internal testing
    #                 if (request.data["phone"] == "8328067271"):
    #                     otp = 12345
    #                 else:
    #                     otp = generate_otp()
    #                 send_otp(otp,request.data["phone"], request.data["countryCode"], request.data["email"])
                    
    #                 data = {}
    #                 data["firstName"] = unserialized_query_object.data[0]["first_name"]
    #                 return Response({"message":"Your OTP has been sent successfully.","data": data,"status": status.HTTP_200_OK})
    #             else:
    #                 return Response({"message":"You are not a registered user, please go signup","status": status.HTTP_409_CONFLICT})

    #     except Exception as e:
    #         return Response({"message":"internal server error","status":status.HTTP_500_INTERNAL_SERVER_ERROR})


