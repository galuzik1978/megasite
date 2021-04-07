from django.db import models
from postoffice.models import Inbox, Contract
from django.contrib.auth.models import User


class Status(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class TaskStatus(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class EventType(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class MainWork(models.Model):
    inbox = models.ForeignKey(Inbox, on_delete=models.PROTECT, verbose_name="Входящее")
    manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name="manager", verbose_name="Менеджер")
    expert = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="expert",
        null=True,
        blank=True,
        help_text="Исполнитель"
    )
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True, verbose_name="Статус заявки")
    cost = models.DecimalField(max_digits=24, decimal_places=2, null=True, blank=True, verbose_name='Цена заявки')
    payed = models.DecimalField(max_digits=24, decimal_places=2, null=True, blank=True, verbose_name="Оплаченная сумма")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Договор")
    accountant = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="accountant",
        null=True,
        blank=True,
        verbose_name="Представитель заказчика"
    )

    def __str__(self):
        return "Заявка по {} от {}".format(
            self.inbox.name,
            self.inbox.date
        )

class Task(models.Model):
    work_flow = models.ForeignKey(MainWork, on_delete=models.PROTECT, verbose_name="Работа")
    initiator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='initiator', verbose_name="Инициатор")
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='executor', verbose_name="Исполнитель")
    subscriber = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="subscriber",
        verbose_name="Потребитель"
    )
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Краткое описание")
    status = models.ForeignKey(TaskStatus, on_delete=models.PROTECT, verbose_name="Статус")
    estimate = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Оценка выполения задачи")

    def __str__(self):
        return "Задача по {} для {}".format(
            self.title,
            self.executor.name
        )


class Message(models.Model):
    task = models.ForeignKey(Task, on_delete=models.PROTECT, verbose_name="Задача")
    sender = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Отправитель",
        related_name="Message_sender"
    )
    recipients = models.ManyToManyField(User, verbose_name="Получатели")
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Краткое описание")
    annex = models.FileField(upload_to="mainWork/static", verbose_name="Приложение", null=True, blank=True)

    def __str__(self):
        return "Сообщение {} от {}".format(
            self.title,
            self.sender.name,
        )
