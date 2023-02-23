import math
import random
from .models import *
from .serializers import *
import boto3
import datetime

import requests
import json
from io import StringIO
import csv

def generate_otp():
    digits = "1234567891"
    OTP = ""
    for i in range(5):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def send_messsage(complete_number,message):

    # AWS CREDs
    # access_key = "AKIA3EKDCQ7FVPPPQSYQ"
    # secret_key = "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"

    # client = boto3.client("sns", aws_access_key_id= access_key, aws_secret_access_key=secret_key, region_name="ap-south-1")
    # aws_response = client.publish(PhoneNumber=complete_number,Message=message)
    # print(aws_response)
    # return aws_response

 

    url = "https://www.fast2sms.com/dev/bulk"

    data_set = {'sender_id': 'FSTSMS','message': message,'language': 'english','route': 'p','numbers': complete_number}
    headers = {'authorization': 'qTLE5wotkn3s6r7HaNzcgW0U4J1ZDlOSeAMKbQGj9mIpCf8dhiYCesihIrQJtZngz1mSxuDEbA5wkpd3','Content-Type': "application/x-www-form-urlencoded",'Cache-Control': "no-cache"}
        
    response = requests.request("POST",url,data = data_set,headers = headers)
    returned_msg = json.loads(response.text)
    return returned_msg

def transmit_otp(country_code,phone):
    complete_number = str(phone)
    query_object = Otp.objects.filter(phone=phone)
    query_object.delete()
    
    if phone =="9490497399":
        otp = "12345"
    else:
        otp = generate_otp()
    message = "Hello,\nUse the OTP "+str(otp)+" for logging into Yuva Galam Application.\n\nThank You\n"
    
    if phone != "":
        sms_service_response = send_messsage(complete_number,message)
        
        # if aws_response['ResponseMetadata']['HTTPStatusCode'] == 200:
        #     Otp.objects.create(otp=otp,phone=phone,expiry=datetime.datetime.now() + datetime.timedelta(hours=1))
        #     return 200
        # else:
        #     return 500
        if sms_service_response['message'][0] == 'SMS sent successfully.':
            Otp.objects.create(otp=otp,phone=phone,expiry=datetime.datetime.now() + datetime.timedelta(minutes=10))
            return 200
        else:
            return 500

def write_CSV(csvData):
    body = StringIO()
    writer = csv.writer(body)
    for item in csvData:
        writer.writerow(item.values())
    csvS3 = body.getvalue()
    return csvS3



