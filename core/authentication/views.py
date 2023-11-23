from django.shortcuts import render
from .models import User
from rest_framework import generics,status,views
from rest_framework.response import Response
from .serializers import RegisterSerializer,EmailVerificationSerializer,LoginSerializer,ResetPasswordEmailRequestSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from ..core.utils.email import Util
from ..core.utils.renders import CustomRenders
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email = user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        asbsurl = 'http://'+current_site+relativeLink+'?token='+str(token)
        email_body = 'Hi '+ user.username + ' Use link below to verify your email \n' + 'domain'+asbsurl
        data={'email_body':email_body,'to_email':user.email,'email_subject':'Verify your email address'}
        # Util.send_email(data)
        print(print('asbsurl',token))
        return Response(user_data,status=status.HTTP_201_CREATED)
    
class VerifyEmail(views.APIView):
        serializer_class = EmailVerificationSerializer
        token_params_config = openapi.Parameter('token',in_=openapi.IN_QUERY,description='Description',type=openapi.TYPE_STRING)
        @swagger_auto_schema(manual_parameters=[token_params_config])
        def get(self,request):
            token = request.GET.get('token')
            signing_key = settings.SIMPLE_JWT['SIGNING_KEY']
            
            try:
                payload = jwt.decode(token,signing_key, algorithms=['HS256'])
                user = User.objects.get(email = payload['user_id'])
                if not user.is_verified:
                    user.is_verified = True
                    user.save()
                    return Response({'status':'Email Verified'},status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError as itentifier:
                    return Response({'error':'Provided token is expired'},status=status.HTTP_400_BAD_REQUEST)
            except jwt.exceptions.DecodeError as itentifier:
                    return Response({'error':'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
      serializer_class = LoginSerializer
      renderer_classes = (CustomRenders,)
      def post(self,request):
            serializer = self.serializer_class(data =request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
    
class RequestPasswordResetEmail(generics.GenericAPIView):
      serializer_class = ResetPasswordEmailRequestSerializer
      def post(self,request):
            serializer = self.serializer_class(data = request.data)
            serializer.is_valid(raise_exception=True)