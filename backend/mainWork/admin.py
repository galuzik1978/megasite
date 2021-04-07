from django.contrib import admin

from mainWork.models import Status, TaskStatus, EventType, MainWork, Task, Message

admin.site.register(Status)
admin.site.register(TaskStatus)
admin.site.register(EventType)
admin.site.register(MainWork)
admin.site.register(Task)
admin.site.register(Message)
