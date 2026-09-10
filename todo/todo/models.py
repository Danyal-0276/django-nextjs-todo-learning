from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):

    srno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    completed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos")

    def __str__(self):
        return self.title
