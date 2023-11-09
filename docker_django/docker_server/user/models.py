from django.db import models

# Create your models here.


class UserInfo(models.Model):
    name = models.CharField(max_length=40, default="", blank=False, null=False)
    age = models.IntegerField(default="", blank=True, null=True)
