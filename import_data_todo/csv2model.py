import os
import re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_project.settings')

from todo.models import Todo
from todo.serializer import Todo_Serializer

from custom_authentication.models import User
from celery import shared_task
from celery.contrib import rdb
from import_data_todo.celery_app import app

from django.core.exceptions import ValidationError

@app.task()
def csv2model(csv_line):
    todo = Todo(
               todo_title = csv_line['todo_title'],
               todo_status = csv_line['todo_status'],
               todo_user = User.objects.get(pk=csv_line['todo_user']),
               created_at = csv_line['created_at'],
               created_by = User.objects.get(pk=csv_line['created_by']),
               updated_by = User.objects.get(pk=csv_line['updated_by']),
            )
    try:
        todo.full_clean()
    except ValidationError as e:
        print('error in Validation model', e)
        return False
    else:
        todo.save()
        return True

def csv2dic(head, text):
    head=head.replace('\n','')
    text=text.replace('\n','')
    head = re.split(',', head)
    text = re.split(',', text)
    dic = {}
    for i in range(len(head)):
        dic[head[i]] = text[i]
    return dic

