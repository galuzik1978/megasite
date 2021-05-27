from django.db import models


# Create your models here.
class Division(models.Model):
    name = models.CharField(max_length=80, verbose_name="Подразделение")

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=80, verbose_name="Участок")
    division = models.ForeignKey(Division, on_delete=models.PROTECT)

    def __str__(self):
        return "Участок {} цеха {}".format(
            self.name,
            self.division.name
        )

class Machine(models.Model):
    name = models.CharField(max_length=80, verbose_name="Оборудование")
    stock_number = models.CharField(max_length=25, verbose_name="Инвентарный номер")
    division = models.ForeignKey(Division, on_delete=models.PROTECT)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return "Оборудование {} участка {} цеха {}".format(
            self.name,
            self.region.name,
            self.division.name
        )