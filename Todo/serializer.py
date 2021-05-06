from rest_framework import serializers

from .models import Todo

class Todo_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = [
            'id',
            'todo_title',
            'todo_status',
            'todo_user',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by'
        ]
        extra_kwargs = {
            'todo_user': {'required' : True},
            'created_by': {'required': False},
            'updated_by': {'required': False},

        }