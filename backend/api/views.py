from datetime import datetime

from django.contrib.auth.models import User
from django.http import JsonResponse, FileResponse
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, authentication, filters, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from util import customize
from util.Mixins import FormMenuMixin

from api.serializers import InboxSer, OutboxSer, SenderSer, ProfileSer, RoleSer, CustomerSer, TypeLetterSer, \
    SendStatusSer, TypeWorkSer, ContractSer, StatusSer, TaskStatusSer, EventTypeSer, MainWorkSer, TaskSer, MessageSer, \
    TypeCustomerSer, CityTypeSer, StreetTypeSer, TypeLiftSer, LiftDesignSer, TypeProtocolSer, DeviceSetSer, \
    StatusDeviceSer, TypeDeviceSer, RangeMeasureSer, AccuracyClassSer, ObjectSer, ProtocolSer, DeviceSer, \
    get_organization_by_inn, ManagerSer, OrganisationSer, FormsSer, TablesSer, HeaderSer, SellSer, RowSer, \
    SelectChoicesSer, WorkRequestSer, SellValueSer, RowDefectsSer, ReasonSer, DocumentSer, ObservedDefectSer, \
    ProtocolAnnexSer, RulesSer, hint_address
from organisation.models import Organisation, TypeOrganisation, CityType, StreetType, TypeLift, LiftDesign, \
    TypeProtocol, DeviceSet, \
    StatusDevice, TypeDevice, RangeMeasure, AccuracyClass, Object, Protocol, Device, Form
from mainWork.models import Status, TaskStatus, EventType, MainWork, Task, Message
from postoffice.models import Inbox, Outbox, TypeLetter, SendStatus, TypeWork, Contract, WorkRequest
from user_profile.models import Profile, Role
from util.customize import tables
from util.functions import capacity_text_to_decimal


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
            form.table = []
            for table in form.table_set.all():
                table.header = []
                for header in table.header_set.all():
                    query = header.selectchoices_set.all()
                    if len(query):
                        header.selectchoices = []
                        for selectchoice in query:
                            header.selectchoices.append(SelectChoicesSer(selectchoice).data)
                    table.header.append(HeaderSer(header).data)
                table.row = []
                for row in table.row_set.all():
                    row.sell = []
                    for sell in row.sell_set.all():
                        sell.sell_value = []
                        for sell_value in sell.sellvalue_set.all():
                            sell_value.observed_defect = []
                            for observed_defect in sell_value.observeddefect_set.all():
                                sell_value.observed_defect.append(ObservedDefectSer(observed_defect).data)
                            sell_value.annex = []
                            for annex in sell_value.protocolannex_set.all():
                                sell_value.annex.append(ProtocolAnnexSer(annex).data)
                            sell.sell_value.append((SellValueSer(sell_value).data))
                        sell.rules = []
                        for rules in sell.rules_set.all():
                            sell.rules.append(RulesSer(rules).data)
                        row.sell.append(SellSer(sell).data)
                    row.rowdefect = []
                    for row_defects in row.rowdefects_set.all():
                        row_defects.reason = []
                        for reason in row_defects.reason_set.all():
                            reason.document = []
                            for document in reason.document_set.all():
                                reason.document.append((DocumentSer(document).data))
                            row_defects.reason.append(ReasonSer(reason).data)
                        row.rowdefect.append(RowDefectsSer(row_defects).data)
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

    @staticmethod
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


class WorkRequestView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        """
        Сохранение/обновление заявок на проведение работ, а также контракта,
        связанного с этими заявками.
        """
        contract = Contract.objects.get(pk=kwargs['contract'])
        # Обновляем данные заказчика в соответствии с заявкой
        contract.customer.inn = int(request.data['inn']) if request.data['inn'] != 'null' else None
        contract.customer.full_name = request.data['full_name']
        contract.customer.head = request.data['head']
        contract.customer.head_last_name = request.data['head_last_name']
        contract.customer.head_name = request.data['head_name']
        contract.customer.head_surname = request.data['head_surname']
        contract.customer.ogrn = int(request.data['ogrn']) if request.data['ogrn'] != 'null' else None
        contract.customer.kpp = int(request.data['kpp']) if request.data['kpp'] != 'null' else None
        contract.customer.legal_address = request.data['address']
        contract.customer.post_address = request.data['post_address']
        contract.customer.bic = int(request.data['bik']) if request.data['bik'] != 'null' else None
        contract.customer.bank = request.data['bank']
        contract.customer.account = int(request.data['account']) if request.data['account'] != 'null' else None
        contract.customer.cor_account = int(request.data['korr_account']) if request.data[
                                                                                 'korr_account'] != 'null' else None
        try:
            contract.customer.type_customer = TypeOrganisation.objects.get(name=request.data['type_customer'])
        except TypeOrganisation.DoesNotExist:
            type_customer = TypeOrganisation(name=request.data['type_customer'])
            type_customer.save()
            contract.customer.type_customer = type_customer
        contract.customer.save()
        new_form = json.loads(request.data['form'])
        try:
            form = Form.objects.get(pk=new_form['id'])
        except TypeError:
            form = None
        table_rows = json.loads(request.data['table_rows'])
        try:
            work_request = contract.workrequest_set.get()
        except WorkRequest.DoesNotExist:
            work_request = WorkRequest(contract=contract, form=form)
            work_request.save()
        # Удаляем заявки текущего договора, отсутствующие в полученном запросе, но присутствующие в базе
        objects_id = [row.get('id') for row in table_rows]
        for work_object in work_request.object.all():
            if work_object.id not in objects_id:
                work_object.delete()
        for obj in table_rows:
            obj['address'] = obj['address']
            # расифровываем адрес через Dadata.ru
            address = hint_address(obj['address'], request).data
            try:
                city_type = CityType.objects.get(name=address['city_type'])
            except CityType.DoesNotExist:
                city_type = CityType(name=address['city_type'])
                city_type.save()
            try:
                street_type = StreetType.objects.get(name=address['street_type'])
            except StreetType.DoesNotExist:
                street_type = StreetType(name=address['street_type'])
                street_type.save()
            try:
                type_lift = TypeLift.objects.get(name=obj['type_lift']['name'])
            except TypeLift.DoesNotExist:
                type_lift = TypeLift(name=obj['type']['name'])
                type_lift.save()
            if obj.get('id', False):
                # Если заявка уже зарегистрирована
                work_object = work_request.object.get(pk=obj['id'])
                work_object.postcode = int(address['postcode'])if address['postcode'] != 'null' else None
                work_object.region = address['region']
                work_object.city = address['city']
                work_object.street_type = street_type
                work_object.city_type = city_type
                work_object.street = address['street']
                work_object.building = address['building']
                work_object.reg_num = obj['reg_num']
                work_object.mf_year = datetime.strptime(obj['mf_year'], '%Y')
                work_object.type_lift = type_lift
                work_object.capacity = capacity_text_to_decimal(obj['capacity'])
                work_object.floors = int(obj['floors']) if obj['floors'] != 'null' else None
                work_object.date_exam = datetime.strptime(obj['date_exam'], '%Y-%m').date()
                work_object.save()
            else:
                work_object = Object(
                    postcode=int(address['postcode']) if address['postcode'] != 'null' else None,
                    region=address['region'],
                    city_type=city_type,
                    city=address['city'],
                    street_type=street_type,
                    street=address['street'],
                    building=address['building'],
                    reg_num=obj['reg_num'],
                    mf_year=datetime.strptime(obj['mf_year'], '%Y'),
                    type_lift=type_lift,
                    capacity=capacity_text_to_decimal(obj['capacity']),
                    floors=int(obj['floors']) if obj['floors'] != 'null' else None,
                    date_exam=datetime.strptime(obj['date_exam'], '%Y-%m').date(),
                )
                work_object.save()
                work_request.object.add(work_object)

        response_status = status.HTTP_200_OK
        return Response("", status=response_status)

    @staticmethod
    def get(request, *args, **kwargs):
        """
        Выдача данных по заявкам на провдение работ и связанным сущностям
        """
        contract = Contract.objects.get(pk=kwargs['contract'])
        try:
            work_request = contract.workrequest_set.get()
        except WorkRequest.DoesNotExist as err:
            work_request = WorkRequest(contract=contract)
            work_request.save()
        work_request.all_forms = Form.objects.all()
        data = {
            'id': kwargs['contract'],
            'form': work_request.form,
            'contract': contract,
            'all_forms': Form.objects.all(),
            'objects': work_request.object.all()
        }
        serializer = WorkRequestSer(data)
        response_status = status.HTTP_200_OK
        return Response(serializer.data, status=response_status)
