
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from custom_authentication.models import User


class Custom_SignUp(APIView):

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            if request.POST.get('username') and request.POST.get('password'):
                user = User.objects.create_user(request.POST.get('username'),
                                                request.POST.get('email', None),
                                                request.POST.get('password')
                                                )
                if user is not None:
                    return Response({'message':'Create User success'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message':'missing credential'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'method '.join(request.method,' is not allowed')}, \
                                 status=status.HTTP_400_BAD_REQUEST)
    
class Custom_Login(APIView):


    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            if request.POST.get('username') and request.POST.get('password'):
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(username = username,password= password)
                if user is not None:
                    refresh_token = RefreshToken.for_user(user)
                    return Response(
                        {
                            'refresh_token': str(refresh_token),
                            'access_token': str(refresh_token.access_token),
                            'user': username,
                        }
                        , status=status.HTTP_200_OK
                    )
            else:
                return Response({'message':'missing credential'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'method '.join(request.method,' is not allowed')}, \
                                 status=status.HTTP_400_BAD_REQUEST)




