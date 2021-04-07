from django.contrib import admin

from postoffice.models import TypeLetter, SendStatus, TypeWork, Inbox, Outbox, ContractStatus, Contract, ObjRequest, \
    WorkRequest

admin.site.register(TypeLetter)
admin.site.register(SendStatus)
admin.site.register(TypeWork)
admin.site.register(Inbox)
admin.site.register(Outbox)
admin.site.register(ContractStatus)
admin.site.register(Contract)
admin.site.register(WorkRequest)
admin.site.register(ObjRequest)
