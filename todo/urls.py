from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = 'todo'
urlpatterns = [
    path('',views.TodoView.as_view(),name='todolist'),
    path('<int:pk>',views.Todo_Up_Del_View.as_view(),name='up_del_todo'),
    path('uploaddata',views.simple_upload, name='upload')                             
]