import pdb

from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.contrib.auth import authenticate


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from CustomAuthenticated.models import User


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

class Custom_Logout(APIView):

    def post(self, request, *args, **kwargs):
        # authentication_classes = [SessionAuthentication, BasicAuthentication]
        # permission_classes = [IsAuthenticated]
        token = { 
            'token' : request.POST.get('access_token')
        }
        try:
            valid_token = TokenBackend(algorithm='HS256').decode(token,False)
            user = valid_token['user']
        except ValidationError as e:
            return Response(
            {
                'message': 'invalid token' + e
            },
            status= status.HTTP_400_BAD_REQUEST
            )
        user = valid_token['user']
        if user:
            print(user)
            user.auth_token.delete()
            return Response(
                {
                    'message': 'logout success'
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'message': 'login ?'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        


