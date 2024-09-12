from rest_framework import serializers
from app.models import users, leaveRequest
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

class usersSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = users
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'role']
        extra_kwargs = {
            'role': {'required': True},
        }

    def validate_username(self, value):
        if users.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class leaveSerializers(serializers.ModelSerializer):
    class Meta:
        model = leaveRequest
        fields = ['id','employee', 'AssignedManager', 'reason', 'ManagerApproval']
        extra_kwargs = {
            'reason': {'required': True},
            'AssignedManager': {'required': True},
        }
