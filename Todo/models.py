
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy 


from usertimestamp.models import UserTimeStamp

# class UserTimeStamp(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     created_by = models.IntegerField(null=False)
#     updated_at = models.DateTimeField(auto_now=True)
#     updated_by = models.IntegerField(null=False)

#     # def __str__(self):
#     #     return 'Create by:'.join(self.created_by, 'at', self.created_at, '\n',\
#     #                                 'Updated by', self.updated_by, 'at', self.updated_at)


class Todo(UserTimeStamp, models.Model):

    class StatusChoices(models.TextChoices):
        status_open = 'OP', gettext_lazy('Open')
        status_inprogress = 'IN', gettext_lazy('Inprogress')
        status_block = 'BL', gettext_lazy('Block')
        status_qa = 'QA', gettext_lazy('QA')
        status_reView = 'RV', gettext_lazy('Review Code')
        status_done = 'DN', gettext_lazy('Done')

    todo_title = models.CharField(max_length=255)
    todo_status = models.CharField(
        max_length=2,
        choices=StatusChoices.choices,
        default=StatusChoices.status_open
        )
    todo_user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)


    def __str__(self):
        return self.todo_title
    


