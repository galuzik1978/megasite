from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from organisation.models import Organisation
from django.conf import settings
from rest_framework.authtoken.models import Token


MALE = 1
FEMALE = 2
SEX_CHOICES = (
    (MALE, 'Мужской'),
    (FEMALE, 'Женский')
)


class Role(models.Model):
    name = models.CharField('Должность', max_length=20, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="юзер")
    surname = models.CharField(max_length=20, blank=True, null=True, verbose_name="Отчество")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Телефон")
    photo = models.ImageField(blank=True, null=True, verbose_name="Фото")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Должность")
    sex = models.PositiveSmallIntegerField(choices=SEX_CHOICES, default=1, verbose_name="Пол")
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Организация")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

