from rest_framework import serializers
from .models import User
from .models import CNCMachine
from .models import MachineRealtimeStatus


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CNCMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CNCMachine
        fields = '__all__'

class MachineRealtimeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineRealtimeStatus
        fields = '__all__'
