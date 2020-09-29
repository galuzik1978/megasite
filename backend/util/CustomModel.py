from django.db import models


class ChoiceModel(models.Model):
    name = models.CharField("Имя поля", max_length=25)

    def __str__(self):
        return self.name