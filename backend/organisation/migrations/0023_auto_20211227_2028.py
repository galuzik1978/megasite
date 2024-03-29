# Generated by Django 3.1.1 on 2021-12-27 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0022_row_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_full_name', models.CharField(max_length=255, null=True)),
                ('customer_type', models.CharField(max_length=55, null=True)),
                ('customer_head', models.CharField(max_length=55, null=True)),
                ('customer_name', models.CharField(max_length=55, null=True)),
                ('customer_surname', models.CharField(max_length=55, null=True)),
                ('customer_lastname', models.CharField(max_length=55, null=True)),
                ('customer_inn', models.CharField(max_length=25, null=True)),
                ('customer_kpp', models.CharField(max_length=25, null=True)),
                ('customer_ogrn', models.CharField(max_length=25, null=True)),
                ('customer_contact_name', models.CharField(max_length=255, null=True)),
                ('customer_email', models.CharField(max_length=255, null=True)),
                ('customer_phone', models.CharField(max_length=15, null=True)),
                ('customer_legal_address', models.CharField(max_length=255, null=True)),
                ('customer_post_address', models.CharField(max_length=255, null=True)),
                ('bank_name', models.CharField(max_length=150, null=True, verbose_name='Наименование банка')),
                ('bank_bic', models.CharField(max_length=15, null=True)),
                ('bank_inn', models.CharField(max_length=15, null=True)),
                ('bank_kpp', models.CharField(max_length=15, null=True)),
                ('bank_correspondent_account', models.CharField(max_length=55, null=True)),
                ('bank_payment_account', models.CharField(max_length=55, null=True)),
                ('work', models.CharField(max_length=255, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organisation.organisation')),
            ],
        ),
        migrations.CreateModel(
            name='LeadStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisation.lead')),
            ],
        ),
        migrations.CreateModel(
            name='WorkObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisation.lead')),
            ],
        ),
        migrations.CreateModel(
            name='WorkObjAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, null=True)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisation.lead')),
            ],
        ),
        migrations.CreateModel(
            name='WorkMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisation.lead')),
            ],
        ),
        migrations.CreateModel(
            name='WorkLift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, null=True)),
                ('reg_number', models.CharField(max_length=255, null=True)),
                ('year_of_commission', models.IntegerField(null=True)),
                ('type', models.CharField(max_length=25, null=True)),
                ('capacity', models.IntegerField(null=True)),
                ('floors', models.IntegerField(null=True)),
                ('manufactured', models.IntegerField(null=True)),
                ('last_verife', models.DateField(null=True)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisation.lead')),
            ],
        ),
        migrations.CreateModel(
            name='WorkControlObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisation.lead')),
            ],
        ),
        migrations.CreateModel(
            name='WorkControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisation.lead')),
            ],
        ),
        migrations.AddField(
            model_name='lead',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organisation.leadstatus'),
        ),
    ]
