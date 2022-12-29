from rest_framework import serializers
from .models import Assemblies,PadayatraSchedule,Districts


class DistrictsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Districts
        fields='__all__'


class AssemblySerializer(serializers.ModelSerializer):
    class Meta:
        model=Assemblies
        fields='__all__'
        

class PadayatraSerializer(serializers.ModelSerializer):
    class Meta:
        model=PadayatraSchedule
        exclude=['registered_users','registered_users_count']
        
    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('worldwide_gross cannot be bigger than us_gross')
        return data