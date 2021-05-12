import os
import re

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
#from django.utils.decorators import method_decorator

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Todo
from .serializer import Todo_Serializer
from todo_project import settings
from import_data_todo.csv2model import csv2model, csv2dic

class TodoView(ListCreateAPIView):
    model = Todo
    serializer_class = Todo_Serializer
    Authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            
            todo_list = Todo.objects.all()
        else:
            todo_list = Todo.objects.all().filter(todo_user=request.user.id)
        page = self.paginate_queryset(todo_list)
        if page is not None:
            serializer = Todo_Serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = Todo_Serializer(todo_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if (request.POST.get('todo_user') == str(request.user.id)) \
                or request.user.is_superuser:
            data = {
                'todo_title' : request.data.get('todo_title'),
                'todo_status' : request.data.get('todo_status'),
                'todo_user' : request.data.get('todo_user',request.user.id),
                'created_by' : request.user.id,
                'updated_by' : request.user.id,
                }

            serializer = Todo_Serializer(data=data, context={
                'request': request
            })
            if serializer.is_valid():
                serializer.save()
                return Response(
                        {'message':'Create new todo success'}, 
                        status=status.HTTP_201_CREATED
                    )
            else:
                return Response(
                        {'message':'Create new todo failed'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            return Response(
                        {'message':'You cant do that'},
                         status=status.HTTP_400_BAD_REQUEST
                    )

    def get_queryset(self):
        return Todo.objects.all()

class Todo_Up_Del_View(RetrieveUpdateDestroyAPIView):
    model = Todo
    serializer_class = Todo_Serializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        todo_task = Todo.objects.all().filter(id=kwargs.get('pk'))
        serializer = Todo_Serializer(todo_task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        todo_task = get_object_or_404(Todo,id=kwargs.get('pk'))
        if request.method=='PUT':
            if request.user.id == str(todo_task.todo_user) \
                    or request.user.id == (todo_task.created_by) \
                    or request.user.is_superuser:

                serializer = Todo_Serializer(todo_task, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                                {'message': 'Update success'},
                                status=status.HTTP_200_OK
                            )
                else:
                    return Response(
                                {'message': 'Update failed'},
                                status=status.HTTP_400_BAD_REQUEST
                            )
            else:
                return Response(
                            {'message': 'You cant do that'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

    def delete(self, request, *args, **kwargs):
        todo_task = get_object_or_404(Todo,id=kwargs.get('pk'))
        if request.method=='DELETE':
            if request.user.id == str(todo_task.todo_user) \
                    or request.user.id == todo_task.todo_user_create \
                    or request.user.is_superuser:
                todo_task.delete()
                return Response(
                            {'message': 'Delete success'},
                            status=status.HTTP_200_OK
                        )
            else:
                return Response(
                            {'message': 'You cant do that'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
    
    def get_queryset(self):
        return Todo.objects.all()




def simple_upload(request):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    if request.method == 'POST' and request.FILES['document']:
        uploaded_file = request.FILES['document']
        if uploaded_file:
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            with open(os.path.join(settings.MEDIA_ROOT, filename)) as f:
                data = f.readlines()
                for i in range(len(data)):
                    if i == 0:
                        continue
                    else:
                        
                        temp = csv2dic(data[0],data[i])
                        csv2model.delay(temp)
    return render(request,'simple_upload.html')