from django.contrib.auth.models import User
from django.http import JsonResponse, FileResponse
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, authentication, filters, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from util import customize
from util.Mixins import FormMenuMixin

from api.serializers import InboxSer, OutboxSer, SenderSer, ProfileSer, RoleSer, CustomerSer, TypeLetterSer, \
    SendStatusSer, TypeWorkSer, ContractSer, StatusSer, TaskStatusSer, EventTypeSer, MainWorkSer, TaskSer, MessageSer, \
    TypeCustomerSer, CityTypeSer, StreetTypeSer, TypeLiftSer, LiftDesignSer, TypeProtocolSer, DeviceSetSer, \
    StatusDeviceSer, TypeDeviceSer, RangeMeasureSer, AccuracyClassSer, ObjectSer, ProtocolSer, DeviceSer, \
    get_organization_by_inn, ManagerSer, OrganisationSer, FormsSer, TablesSer, HeaderSer, SellSer, RowSer, \
    SelectChoicesSer, WorkRequestSer
from organisation.models import Organisation, TypeOrganisation, CityType, StreetType, TypeLift, LiftDesign, \
    TypeProtocol, DeviceSet, \
    StatusDevice, TypeDevice, RangeMeasure, AccuracyClass, Object, Protocol, Device, Form
from mainWork.models import Status, TaskStatus, EventType, MainWork, Task, Message
from postoffice.models import Inbox, Outbox, TypeLetter, SendStatus, TypeWork, Contract, WorkRequest
from user_profile.models import Profile, Role
from util.customize import tables


class MainPageView(FormMenuMixin, TemplateView):
    template_name = "vue/index.html"


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


class SenderApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all().filter(is_staff=False)
    serializer_class = SenderSer


class ManagerApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all().filter(profile__role__name="Менеджер")
    serializer_class = ManagerSer


class ProfileApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSer


class RoleApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = RoleSer


class CustomerApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Organisation.objects.all()
    serializer_class = CustomerSer


class OrganisationApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSer


class TypeLetterApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = TypeLetter.objects.all()
    serializer_class = TypeLetterSer


class SendStatusApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = SendStatus.objects.all()
    serializer_class = SendStatusSer


class TypeWorkApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = TypeWork.objects.all()
    serializer_class = TypeWorkSer


class ContractApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Contract.objects.all()
    serializer_class = ContractSer

    def post(self, *args, **kwargs):
        res = super(ContractApiView, self).post(*args, **kwargs)
        return res


class StatusApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Status.objects.all()
    serializer_class = StatusSer


class TaskStatusApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusSer


class EventTypeApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = EventType.objects.all()
    serializer_class = EventTypeSer


class MainWorkApiView(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = MainWork.objects.all()
    serializer_class = MainWorkSer


class TaskApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSer


class MessageApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageSer


class TypeCustomerApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = TypeOrganisation.objects.all()
    serializer_class = TypeCustomerSer


class CityTypeApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = CityType.objects.all()
    serializer_class = CityTypeSer


class StreetTypeApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = StreetType.objects.all()
    serializer_class = StreetTypeSer


class TypeLiftApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = TypeLift.objects.all()
    serializer_class = TypeLiftSer


class LiftDesignApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = LiftDesign.objects.all()
    serializer_class = LiftDesignSer


class TypeProtocolApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = TypeProtocol.objects.all()
    serializer_class = TypeProtocolSer


class DeviceSetApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = DeviceSet.objects.all()
    serializer_class = DeviceSetSer


class StatusDeviceApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = StatusDevice.objects.all()
    serializer_class = StatusDeviceSer


class TypeDeviceApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = TypeDevice.objects.all()
    serializer_class = TypeDeviceSer


class RangeMeasureApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = RangeMeasure.objects.all()
    serializer_class = RangeMeasureSer


class AccuracyClassApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = AccuracyClass.objects.all()
    serializer_class = AccuracyClassSer


class ObjectApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Object.objects.all()
    serializer_class = ObjectSer


class ProtocolApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Protocol.objects.all()
    serializer_class = ProtocolSer


class DeviceApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Device.objects.all()
    serializer_class = DeviceSer


class TemplateView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request, format=None):
        return Response({'desktop': customize.desk_config, 'tables': customize.tables})

    @staticmethod
    def post(request, format=None):
        return Response({'desktop': customize.desk_config, 'tables': customize.tables})


class CustomApiLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': "{} {} {}".format(user.first_name, user.profile.surname, user.last_name),
            'role': user.profile.role.name,
            'email': user.email,
            'desktop': customize.desk_config['manager']['sections'],
            'tables': customize.tables,
            'title': customize.TITLE,
            'logo': customize.LOGO,
            'company': customize.COMPANY
        })


class InnRequestView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request, format=None):
        inn = request.query_params['inn']
        return get_organization_by_inn(inn, request)

    @staticmethod
    def post(request, format=None):
        inn = request.query_params['inn']
        return get_organization_by_inn(inn, request)


class InboxDeclineView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        inbox = Inbox.objects.get(pk=kwargs['inbox'])
        try:
            send_status = SendStatus.objects.get(name = "Отклонено")
        except SendStatus.DoesNotExist as err:
            send_status = SendStatus.objects.create(name = "Отклонено")
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
            send_status = SendStatus.objects.get(name = "В работе")
        except SendStatus.DoesNotExist as err:
            send_status = SendStatus.objects.create(name = "В работе")
        inbox.send_status = send_status
        inbox.save()
        serializer = InboxSer(inbox)
        response_status = status.HTTP_200_OK
        return Response(serializer.data, status=response_status)


class CreateContractByInboxView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        inbox = Inbox.objects.get(pk=kwargs['inbox'])
        table = tables['contract']
        table['edit']['fields']['inbox']['value'] = InboxSer(inbox).data
        table['edit']['fields']['customer']['value'] = CustomerSer(inbox.customer).data
        table['edit']['fields']['type_work']['value'] = TypeWorkSer(inbox.type_work).data
        return JsonResponse(table)


class GetBlankView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]


    @staticmethod
    def post(request, *args, **kwargs):
        f = FileResponse(open("../Основные функции.ods", 'rb'))
        return f

    @staticmethod
    def get(request, *args, **kwargs):
        return FileResponse("Основные функции.ods")


class FormsView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request, format=None):
        forms = Form.objects.all()
        response = []
        for form in Form.objects.all():
            form.table=[]
            for table in form.table_set.all():
                table.header=[]
                for header in table.header_set.all():
                    query = header.selectchoices_set.all()
                    if len(query):
                        header.selectchoices=[]
                        for selectchoice in query:
                            header.selectchoices.append(SelectChoicesSer(selectchoice).data)
                    table.header.append(HeaderSer(header).data)
                table.row = []
                for row in table.row_set.all():
                    row.sell = []
                    for sell in row.sell_set.all():
                        row.sell.append(SellSer(sell).data)
                    table.row.append(RowSer(row).data)
                form.table.append(TablesSer(table).data)
            response.append({'form': FormsSer(form).data})
        return Response(response)

    @staticmethod
    def post(request, format=None):
        return Response({'desktop': customize.desk_config, 'tables': customize.tables})


class NewWorkRequestView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        contract = Contract.objects.get(pk=kwargs['contract'])
        work_request = WorkRequest(contract=contract)
        work_request.save()
        serializer = WorkRequestSer(work_request)
        response_status = status.HTTP_200_OK
        return Response(serializer.data, status=response_status)

    def get(request, *args, **kwargs):
        contract = Contract.objects.get(pk=kwargs['contract'])
        try:
            work_request = contract.workrequest_set.get()
        except WorkRequest.DoesNotExist as err:
            work_request = WorkRequest(contract=contract)
            work_request.save()
        serializer = WorkRequestSer(work_request)
        response_status = status.HTTP_200_OK
        return Response(serializer.data, status=response_status)