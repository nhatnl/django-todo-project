from django.db import models
from custom_authentication.models import User


# Create your models here.
class UserTimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='create_constrain')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='update_constrain')

    # def __str__(self):
    #     return 'Create by:'.join(self.created_by, 'at', self.created_at, '\n',\
    #                                 'Updated by', self.updated_by, 'at', self.updated_at)