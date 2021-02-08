# Generated by Django 3.1.1 on 2021-02-02 17:16

from django.db import migrations


def init_forms(apps, schema_editor):
    FIELD_TYPES = [
        (0, 'none'),
        (1, 'bool'),
        (2, 'rows_num'),
        (3, 'select'),
        (4, 'actions')
    ]
    # Создаем новую форму
    Form = apps.get_model('organisation', 'Form')
    form = Form(name="Пассажирский лифт")
    form.save()
    # Создаем новую таблицу, привязанную к форме
    Table = apps.get_model('organisation', 'Table')
    table = Table(
        name='Результаты проверки соответствия электрооборудования лифта'
    )
    table.save()
    table.form.add(form)
    # Определяем столбцы созданной таблицы
    Header = apps.get_model('organisation', 'Header')
    header = Header(
        table=table,
        text='№ п/п',
        type=2,
        value=None,
        editable=False
    )
    header.save()
    header = Header(
        table=table,
        text='Наименование составных элементов электрооборудования лифта',
        value='name',
        editable=False
    )
    header.save()
    header = Header(
        table=table,
        text='Нормативная документация и перечень пунктов, устанавливающих требования ГОСТ Р 53780, ГОСТ Р53783',
        value='documents',
        editable=False
    )
    header.save()
    header = Header(
        table=table,
        text='Результат визуального контроля',
        type=3,
        value='result',
        editable=True
    )
    header.save()
    # Добавим перечень возможных результатов контроля
    SelectChoices = apps.get_model('organisation', 'SelectChoices')
    select_choices = SelectChoices(
        header=header,
        text='соответствует',
        value=0
    )
    select_choices.save()
    select_choices = SelectChoices(
        header=header,
        text='не соответствует',
        value=1
    )
    select_choices.save()
    select_choices = SelectChoices(
        header=header,
        text='не подлежит',
        value=2
    )
    select_choices.save()
    # Добавим несколько строк в таблицу
    Row = apps.get_model('organisation', 'Row')
    row = Row(
        table=table,
        name='Аппараты защиты'
    )
    row.save()
    Sell = apps.get_model('organisation', 'Sell')
    sell = Sell(
        row=row,
        text='Аппараты защиты',
        name='name'
    )
    sell.save()
    sell = Sell(
        row=row,
        text='ГОСТ Р 53780, ГОСТ Р53783',
        name='documents'
    )
    sell.save()
    sell = Sell(
        row=row,
        name='result'
    )
    sell.save()
    row = Row(
        table=table,
        name='Электропроводка'
    )
    row.save()
    sell = Sell(
        row=row,
        text='Электропроводка',
        name='name'
    )
    sell.save()
    sell = Sell(
        row=row,
        text='ГОСТ Р 53780, ГОСТ Р53783',
        name='documents'
    )
    sell.save()
    sell = Sell(
        row=row,
        name='result'
    )
    sell.save()
    row = Row(
        table=table,
        name='Электрооборудование'
    )
    row.save()
    sell = Sell(
        row=row,
        text='Электрооборудование',
        name='name'
    )
    sell.save()
    sell = Sell(
        row=row,
        text='ГОСТ Р 53780, ГОСТ Р53783',
        name='documents'
    )
    sell.save()
    sell = Sell(
        row=row,
        name='result'
    )
    sell.save()
    row = Row(
        table=table,
        name='Освещение и электроустановочные устройства'
    )
    row.save()
    sell = Sell(
        row=row,
        text='Освещение и электроустановочные устройства',
        name='name'
    )
    sell.save()
    sell = Sell(
        row=row,
        text='ГОСТ Р 53780, ГОСТ Р53783',
        name='documents'
    )
    sell.save()
    sell = Sell(
        row=row,
        name='result'
    )
    sell.save()
    row = Row(
        table=table,
        name='Заземление (зануление)'
    )
    row.save()
    sell = Sell(
        row=row,
        text='Заземление (зануление)',
        name='name'
    )
    sell.save()
    sell = Sell(
        row=row,
        text='ГОСТ Р 53780, ГОСТ Р53783',
        name='documents'
    )
    sell.save()
    sell = Sell(
        row=row,
        name='result'
    )
    sell.save()
    row = Row(
        table=table,
        name='Маркировка элементов электрооборудования'
    )
    row.save()
    sell = Sell(
        row=row,
        text='Маркировка элементов электрооборудования',
        name='name'
    )
    sell.save()
    sell = Sell(
        row=row,
        text='ГОСТ Р 53780, ГОСТ Р53783',
        name='documents'
    )
    sell.save()
    sell = Sell(
        row=row,
        name='result'
    )
    sell.save()


class Migration(migrations.Migration):

    operations = [
        migrations.RunPython(init_forms),
    ]

    dependencies = [
        ('organisation', '0004_auto_20210202_2215'),
    ]
