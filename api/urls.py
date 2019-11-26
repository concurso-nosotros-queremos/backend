from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'contest', ContestViewSet, base_name='contest')
router.register(r'state', StateViewSet, base_name='state')
router.register(r'city', CityViewSet, base_name='city')
router.register(r'group', GroupViewSet, base_name='group')
router.register(r'raw_project', RawProjectViewSet, base_name='raw_project')
router.register(r'raw_school', RawSchoolViewSet, base_name='raw_school')
router.register(r'contest_winner', ContestWinnerViewSet, base_name='contest_winner')
router.register(r'contest_finalist', ContestFinalistViewSet, base_name='contest_finalist')
router.register(r'group_role', GroupRoleViewSet, base_name='group_role')
router.register(r'group_token', GroupTokenViewSet, base_name='group_token')
router.register(r'token_uses', TokenUsesViewSet, base_name='token_uses')
router.register(r'raw_participant', RawParticipantViewSet, base_name='raw_participant')
router.register(r'category', CategoryViewSet, base_name='category')
router.register(r'project_category', ProjectCategoryViewSet, base_name='project_category')
router.register(r'raw_contact', RawContactViewSet, base_name='raw_contact')
router.register(r'contest_end', ContestEnd, base_name='contest_end'),
router.register(r'message_email', MessageEmailViewSet, base_name='message_email')

urlpatterns = [
    path('auth/', include('rest_framework_social_oauth2.urls')),
    path('rest/', include(router.urls)),
    path('rest/check/', CheckToken.as_view(), name='check'),
    path('rest/group_info/total/', GroupCount.as_view(), name='group_total'),
    path('rest/participant_info/total/', RawParticipantCount.as_view(), name='participant_total'),
    path('rest/group_info/city/', GroupCity.as_view(), name='group_city'),
    path('rest/group_info/state/', GroupState.as_view(), name='group_state'),
    path('rest/user_info/<str:token>/', UserInfoToken.as_view(), name='user_info'),
    path('rest/export/contest/<str:token>/', PDFGeneral, name='contest_pdf'),
    path('rest/export/group/<int:id>/<str:token>/', PDFEspecifico, name='group_ pdf')
]