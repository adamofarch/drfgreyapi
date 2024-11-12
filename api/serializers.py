from rest_framework import serializers
from .models import Department, Patient_Record, User
from oauth2_provider.models import AccessToken

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name', 'diagnostics', 'location', 'specialization']

class Patient_RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient_Record
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'role']

