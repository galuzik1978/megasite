# Generated by Django 3.1.1 on 2021-02-23 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0010_auto_20210223_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sell',
            name='value',
            field=models.CharField(max_length=255, null=True),
        ),
    ]