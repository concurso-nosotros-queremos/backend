from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'contest', ContestViewSet, base_name='contest')
router.register(r'state', StateViewSet, base_name='state')
router.register(r'city', CityViewSet, base_name='city')
router.register(r'group', GroupViewSet, base_name='group')
router.register(r'group_location', GroupLocationViewSet, base_name='group_location')
router.register(r'raw_project', RawProjectViewSet, base_name='raw_project')
router.register(r'raw_school', RawSchoolViewSet, base_name='raw_school')
router.register(r'contest_winner', ContestWinnerViewSet, base_name='contest_winner')
router.register(r'contest_finalist', ContestFinalistViewSet, base_name='contest_finalist')
router.register(r'group_role', GroupRoleViewSet, base_name='group_role')
router.register(r'group_post', GroupPostViewSet, base_name='group_post')
router.register(r'post_commnet', PostCommentViewSet, base_name='post_commnet')
router.register(r'post_attachment', PostAttachmentViewSet, base_name='post_attachment')
router.register(r'group_token', GroupTokenViewSet, base_name='group_token')
router.register(r'token_uses', TokenUsesViewSet, base_name='token_uses')
router.register(r'raw_participant', RawParticipantViewSet, base_name='raw_participant')
router.register(r'category', CategoryViewSet, base_name='category')
router.register(r'project_category', ProjectCategoryViewSet, base_name='project_category')

urlpatterns = [
    path('auth/', include('rest_framework_social_oauth2.urls')),
    path('rest/', include(router.urls)),
]