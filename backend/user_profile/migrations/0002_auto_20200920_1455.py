# Generated by Django 3.1.1 on 2020-09-20 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=20, unique=True, verbose_name='Должность'),
        ),
    ]
