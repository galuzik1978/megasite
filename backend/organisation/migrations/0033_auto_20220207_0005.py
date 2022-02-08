# Generated by Django 3.1.1 on 2022-02-06 19:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0032_leadform_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='leadform',
            name='form',
            field=models.FileField(upload_to='LeadForm/%Y/%m/'),
        ),
    ]