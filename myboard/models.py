from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'MyUser'


class Task(models.Model):
    class Status(models.IntegerChoices):
        NEW = 1,
        IN_PROG = 2,
        IN_QA = 3,
        READY = 4,
        DONE = 5

    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    status = models.IntegerField(choices=Status.choices, default=Status.NEW)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Profile, related_name='tasks', blank=True, null=True, on_delete=models.SET_DEFAULT,
                                   default=None)
    assigned_to = models.ForeignKey(Profile, related_name='assigned_tasks', blank=True, null=True,
                                    on_delete=models.SET_DEFAULT, default=None)

    class Meta:
        verbose_name = 'Task'
        ordering = ['-created']

    def __str__(self):
        return f"{self.title}, status: {self.status}, created by {self.created_by}, assigned to {self.assigned_to}"
