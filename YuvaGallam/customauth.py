from rest_framework.authentication import BasicAuthentication
import jwt
from YuvaGallam.settings import SECRET_KEY
from rest_framework.exceptions import AuthenticationFailed
from Users.models import *
from Users.serializers import *

class CustomAuthentication(BasicAuthentication):
     
    def authenticate(self,request):
        try:
            # print(request.headers)
            authorization_data = request.headers.get('Authorization')
            # print(authorization_data)
            if 'Authorization' in request.headers.keys():            
                data = authorization_data.split(" ")
                token = data[1]
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                # try:
                # if 1:
                    # print(payload)
                    # payload = CustomAuthentication.authenticate(self,request)
                #     logged_in_user = payload['id']
                #     # print("--------------",logged_in_user)
                #     query_object = Users.objects.filter(id=logged_in_user)
                #     unserialized_query_object = UsersSerializer(query_object,many =True)
                #     print("nigga",unserialized_query_object.data)
                #     return (payload,None)   
                # except Exception as e:
                #     print("-------------------------------------------------------")
                #     print(e)
                #     raise AuthenticationFailed('user not found')
                return (payload,None)   

            else:
                raise  AuthenticationFailed('No token found!')
        except jwt.exceptions.ExpiredSignatureError as e:
            raise AuthenticationFailed('Token expired')
        except jwt.exceptions.DecodeError as e:
            raise AuthenticationFailed('Decode error')
        except jwt.exceptions.InvalidAlgorithmError as e:
            raise AuthenticationFailed('Invalid algorithm')
        except Exception as e:
            raise e
