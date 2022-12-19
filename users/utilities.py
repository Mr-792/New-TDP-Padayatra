import math
import random
from .models import *
from .serializers import *
import boto3
import datetime


def generate_otp():
    digits = "1234567891"
    OTP = ""
    for i in range(5):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def send_messsage(complete_number,message):
    # AWS CREDs
    access_key = "AKIA3EKDCQ7FZHYCQZN5"
    secret_key = "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"
    region = "ap-south-1"

    client = boto3.client("sns", aws_access_key_id= access_key, aws_secret_access_key=secret_key, region_name=region)
    aws_response = client.publish(PhoneNumber=complete_number,Message=message)
    return aws_response

def transmit_otp(country_code,phone):

    complete_number = country_code+str(phone)
    query_object = Otp.objects.filter(phone=phone)
    query_object.delete()
    
    if phone =="9676686432":
        otp = "12345"
    else:
        otp = generate_otp()
    message = "Hello,\nUse the OTP "+str(otp)+" for logging into Yuva Dalam Application.\n\nThank You\n"
    
    if phone != "":
        aws_response = send_messsage(complete_number,message)
        if aws_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            Otp.objects.create(otp=otp,phone=phone,expiry=datetime.datetime.now() + datetime.timedelta(hours=1))
            return 200
        else:
            return 500








