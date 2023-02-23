from dataclasses import fields
from rest_framework import serializers
from .models import *


class PadayatraScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PadayatraSchedule
        fields = '__all__'

class YoutubeURLsSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeURLs
        fields = '__all__'