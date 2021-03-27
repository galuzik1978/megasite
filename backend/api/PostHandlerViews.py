from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, authentication, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import InboxSer, OutboxSer
from postoffice.models import Inbox, Outbox, SendStatus


class InboxApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Inbox.objects.all().order_by('date')
    serializer_class = InboxSer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['send_status__name', 'sender__id', 'customer_id']


class OutboxApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Outbox.objects.all().order_by('date')
    serializer_class = OutboxSer


class InboxDeclineView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        inbox = Inbox.objects.get(pk=kwargs['inbox'])
        try:
            send_status = SendStatus.objects.get(name="Отклонено")
        except SendStatus.DoesNotExist as err:
            send_status = SendStatus.objects.create(name="Отклонено")
        inbox.send_status = send_status
        inbox.save()
        serializer = InboxSer(inbox)
        response_status = status.HTTP_200_OK
        return Response(serializer.data, status=response_status)


class InboxAcceptView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        inbox = Inbox.objects.get(pk=kwargs['inbox'])
        try:
            send_status = SendStatus.objects.get(name="В работе")
        except SendStatus.DoesNotExist as err:
            send_status = SendStatus.objects.create(name="В работе")
        inbox.send_status = send_status
        inbox.save()
        serializer = InboxSer(inbox)
        response_status = status.HTTP_200_OK
        return Response(serializer.data, status=response_status)