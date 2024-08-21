from rest_framework import serializers
from django.contrib.auth import get_user_model
from random import randint
# from core.models import User


# User=get_user_model()


# class UserSerializer(serializers.Serializer):
#     email=serializers.EmailField()
#     password=serializers.CharField()
#     confirm_password=serializers.CharField()
    


#     def validate_email(self,value):
#         user=CustomUser.objects.filter(email=value).exists()
#         if user:
#             raise serializers.ValidationError("This email is already in use")
#         return value





#     def validate(self, attrs):
#         if attrs.get('password')!=attrs.get('confirm_password'):
#             raise serializers.ValidationError({
#             'details':"The password and confirm password does not match"
#             })


#         return super().validate(attrs)