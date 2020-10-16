from django.db import models
from django.contrib.auth.models import User

from organisation.models import Organisation, Object


class TypeLetter(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name="Тип письма")

    def __str__(self):
        return self.name


class SendStatus(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name="Статус отправки")

    def __str__(self): 
        return self.name


class TypeWork(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name="Тип работы")
    
    def __str__(self):
        return self.name


class Inbox(models.Model):
    num = models.IntegerField(unique=True, verbose_name='Входящй №')
    date = models.DateField(auto_now=True, verbose_name='Дата регистрации')
    sender = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Отправитель',
        related_name='sender'
    )
    customer = models.ForeignKey(
        Organisation,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Организация-отправитель"
    )
    title = models.CharField(max_length=100, verbose_name='Тема письма')
    content = models.TextField(verbose_name='Краткое содержание')
    type_letter = models.ForeignKey(TypeLetter, on_delete=models.PROTECT, verbose_name='Тип документа')
    annex = models.FileField(upload_to="Inbox/", null=True, blank=True, verbose_name='Вложение')
    send_status = models.ForeignKey(SendStatus, on_delete=models.PROTECT, verbose_name='Статус получения')
    type_work = models.ForeignKey(TypeWork, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Тип работы')
    notice = models.TextField(verbose_name='Примечание', null=True, blank=True)
    receiver = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Зарегистрировал",
        related_name='receiver'
    )
    
    def __str__(self):
        return self.title


class Outbox(models.Model):
    num = models.IntegerField(unique=True, verbose_name='Исходящй №')
    date = models.DateField(auto_now=True, verbose_name='Дата регистрации')
    customer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='customer')
    title = models.CharField(max_length=100, verbose_name='Тема письма')
    content = models.TextField(verbose_name='Краткое содержание')
    type_letter = models.ForeignKey(TypeLetter, on_delete=models.PROTECT, verbose_name='Тип документа')
    annex = models.FileField(upload_to="Outbox/", null=True, blank=True)
    notice = models.TextField(verbose_name='Примечание', null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='Sender')

    def __str__(self):
        return self.title


class Contract(models.Model):
    num = models.SmallIntegerField(verbose_name="Номер договора", unique=True)
    date = models.DateField(verbose_name="Дата заключения")
    end_date = models.DateField(verbose_name="Дата окончания")
    type_work = models.ForeignKey(TypeWork, on_delete=models.PROTECT, verbose_name="Тип работы")
    cost = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Стоимость договора")
    external_num = models.CharField(max_length=25, verbose_name="Внешний номер договора")
    inbox = models.ForeignKey(Inbox, on_delete=models.PROTECT, verbose_name="Основание заключения договора")
    customer = models.ForeignKey(Organisation, on_delete=models.PROTECT, verbose_name="Заказчик")
    object = models.ForeignKey(Object, on_delete=models.PROTECT, verbose_name="Объект контроля", null=True,
        blank=True,)