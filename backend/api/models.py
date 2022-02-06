from django.db import models

from user_profile.models import Role


class Table(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()
    title = models.CharField(max_length=50)
    role = models.ManyToManyField(Role)

    def __str__(self):
        return self.title


class Desk(models.Model):
    role = models.ManyToManyField(Role)
    table = models.ManyToManyField(Table)
    text = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    router = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=False)
