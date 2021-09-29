from rest_framework import routers
from django.urls import path, include

import api.InnRequestViews
import api.PostHandlerViews
from api import views
from rest_framework.authtoken import views as rest_views

router = routers.DefaultRouter()
router.register(r'inbox', api.PostHandlerViews.InboxApiView)
router.register(r'outbox', api.PostHandlerViews.OutboxApiView)
router.register(r'sender', views.SenderApiView)
router.register(r'manager', views.ManagerApiView)
router.register(r'profile', views.ProfileApiView)
router.register(r'role', views.RoleApiView)
router.register(r'customer', views.CustomerApiView)
router.register(r'organisation', views.OrganisationApiView)
router.register(r'type_letter', views.TypeLetterApiView)
router.register(r'send_status', views.SendStatusApiView)
router.register(r'type_work', views.TypeWorkApiView)
router.register(r'contract', views.ContractApiView)
router.register(r'status', views.StatusApiView)
router.register(r'task_status', views.TaskStatusApiView)
router.register(r'event_type', views.EventTypeApiView)
router.register(r'main_work', views.MainWorkApiView)
router.register(r'task', views.TaskApiView)
router.register(r'message', views.MessageApiView)
router.register(r'type_customer', views.TypeCustomerApiView)
router.register(r'city_type', views.CityTypeApiView)
router.register(r'street_type', views.StreetTypeApiView)
router.register(r'type_lift', views.TypeLiftApiView)
router.register(r'lift_design', views.LiftDesignApiView)
router.register(r'type_protocol', views.TypeProtocolApiView)
router.register(r'device_set', views.DeviceSetApiView)
router.register(r'status_device', views.StatusDeviceApiView)
router.register(r'type_device', views.TypeDeviceApiView)
router.register(r'range_measure', views.RangeMeasureApiView)
router.register(r'accuracy', views.AccuracyClassApiView)
router.register(r'object', views.ObjectApiView)
router.register(r'protocol', views.ProtocolApiView)
router.register(r'device', views.DeviceApiView)
router.register(r'form', views.FormApiView)
router.register(r'table', views.TableApiView)

# app_name = 'restapi'
urlpatterns = [
    path('', views.MainPageView.as_view(), name='main'),
    path('api/', include (router.urls), name='api'),
    path('inbox/decline/<int:inbox>/', api.PostHandlerViews.InboxDeclineView.as_view(), name='inboxDecline'),
    path('inbox/accept/<int:inbox>/', api.PostHandlerViews.InboxAcceptView.as_view(), name='inboxAccept'),
    # path('api-token-auth/', rest_views.obtain_auth_token),
    path('api-token-auth/', views.CustomApiLoginView.as_view()),
    path('api/innrequest/', api.InnRequestViews.InnRequestView.as_view()),
    path('template/', views.TemplateView.as_view(), name='template'),
    path('contract/create_by_inbox/<int:inbox>/', views.CreateContractByInboxView.as_view(), name="ContractByInbox"),
    path('get_blank/', views.GetBlankView.as_view()),
    path('forms/', views.FormsView.as_view(), name='template'),
    path('api/workrequest/<int:contract>/', views.WorkRequestView.as_view(), name='newWorkRequest'),
    path('api/workrequest/', views.WorkRequestListView.as_view(), name='WorkRequestList'),
    path('api/testfilefield/', views.FileFieldTestView.as_view(), name='FileFieldTest'),
]
