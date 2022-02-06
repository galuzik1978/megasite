from django.core.management.base import BaseCommand

import api.interface
from api.models import Table, Desk
from user_profile.models import Role


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            role = Role.objects.get(name='Default')
        except Role.DoesNotExist:
            role = Role.objects.create(name='Default')
        # Доступные таблицы для менеджера
        table_list = [
            api.interface.sender,
            api.interface.send_status,
            api.interface.type_letter,
            api.interface.inbox,
            api.interface.new_inbox,
            api.interface.lead,
            api.interface.type_work,
            api.interface.type_organisation,
            api.interface.organisation,
        ]
        for table in table_list:
            try:
                Table.objects.get(name=table.name, url=table.url, title=table.title, role=role)
            except Table.DoesNotExist:
                table = Table.objects.create(name=table.name, url=table.url, title=table.title)
                table.role.add(role)
                table.save()

        desk_menu = [api.interface.inbox, api.interface.lead, api.interface.organisation]
        for menu in desk_menu:
            table = Table.objects.get(name=menu.name, url=menu.url, title=menu.title, role=role)
            try:
                Desk.objects.get(
                    text=menu.title,
                    icon=menu.icon,
                    table=table,
                    color='red',
                    role=role
                )
            except Desk.DoesNotExist:
                desk = Desk.objects.create(
                    text=menu.title,
                    icon=menu.icon,
                    color='red',
                    is_active=False,
                )
                desk.table.add(table)
                desk.role.add(role)
                desk.save()
        main_menu = Desk.objects.get(text='Необработанные заявки', role=role)
        main_menu.is_active = True
        main_menu.save()