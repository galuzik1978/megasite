# Generated by Django 3.1.1 on 2022-01-28 09:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0027_auto_20220116_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='sent',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lead',
            name='customer_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organisation.typeorganisation'),
        ),
    ]
