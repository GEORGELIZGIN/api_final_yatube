from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CommentViewSet, PostViewSet, GroupCreateViewSet, FollowListCreateViewSet

comments_router = DefaultRouter()
posts_router = DefaultRouter()
comments_router.register(
    r'(?P<post_id>\d+)/comments', CommentViewSet,
    basename='comments')
posts_router.register('posts', PostViewSet)

urlpatterns = [
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/group/', GroupCreateViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('v1/follow/', FollowListCreateViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('v1/', include(posts_router.urls)),
    path(r'v1/posts/', include(comments_router.urls)),
]
