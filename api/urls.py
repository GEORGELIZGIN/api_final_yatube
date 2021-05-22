from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (CommentViewSet, FollowListCreateViewSet,
                    GroupListCreateViewSet, PostViewSet)

router_v1 = DefaultRouter()
router_v1.register(
    r'(?P<post_id>\d+)/comments', CommentViewSet,
    basename='comments')
router_v1.register('', PostViewSet)

urlpatterns = [
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        'v1/group/',
        GroupListCreateViewSet.as_view(
            {'get': 'list', 'post': 'create'})
    ),
    path(
        'v1/follow/',
        FollowListCreateViewSet.as_view(
            {'get': 'list', 'post': 'create'})
    ),
    path('v1/posts/', include(router_v1.urls)),
]
