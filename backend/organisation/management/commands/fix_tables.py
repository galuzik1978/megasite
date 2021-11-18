from django.core.management.base import BaseCommand

from organisation.models import Table


class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        tables = Table.objects.all()
        for table in tables:
            rows = table.row_set.all().order_by('id')
            for i, row in enumerate(rows):
                row.order = i * 5
                row.save()
            headers = table.header_set.all().order_by('id')
            for i, header in enumerate(headers):
                header.order = i*3
                header.save()