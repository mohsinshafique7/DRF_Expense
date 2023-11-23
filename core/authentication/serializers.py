from rest_framework import serializers
from .models import User
from django.db import connection
from django.contrib.auth import authenticate,get_user_model
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,DjangoUnicodeDecodeError,smart_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length= 68,min_length= 6,write_only= True)

    class Meta:
        model = User
        fields = ['email','username','password']

    def validate(self,attrs):
        email = attrs.get('email','')
        username = attrs.get('username','')
        if not username.isalnum():
            raise serializers.ValidationError('User name should only contain alphanumeric chars')
        return attrs
    
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length = 555)
    class Meta:
        model = User
        fields = 'token'

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,min_length= 3)
    password = serializers.CharField(max_length = 68,min_length = 6,write_only=True)
    username = serializers.CharField(max_length = 255,min_length = 3,read_only=True)
    tokens = serializers.SerializerMethodField()
    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return user.token()
    class Meta:
        model = User
        fields = ['email','username','tokens','password']
    
    def validate(self,attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        user = authenticate(username=email,password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified, contact admin')

        return {
            'email': user.email,
            'username':user.username,
            'token':user.token()
        }

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    class Meta:
        fields = ['email']
    # def validate(self,attrs):

    #     try:
    #         email = attrs.get('email','')
    #         if User.objects.filter(email = email).exists():
    #             user = User.objects.get(email = email)
    #             uidb64 = urlsafe_base64_encode(user.id)
    #             token = PasswordResetTokenGenerator().make_token(user)
    #             current_site = get_current_site(request).domain
    #             relativeLink = reverse('email-verify')
    #             asbsurl = 'http://'+current_site+relativeLink+'?token='+str(token)
    #             email_body = 'Hi '+ user.username + ' Use link below to verify your email \n' + 'domain'+asbsurl
    #             data={'email_body':email_body,'to_email':user.email,'email_subject':'Verify your email address'}