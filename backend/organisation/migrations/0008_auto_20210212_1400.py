# Generated by Django 3.1.1 on 2021-02-12 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0007_auto_20210210_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='capacity',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Грузоподъемность'),
        ),
    ]
