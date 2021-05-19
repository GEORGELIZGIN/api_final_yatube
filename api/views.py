from django.core import exceptions
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, permissions, filters, exceptions

from .models import Post, User, Group, Follow
from .permissions import PostAndCommentPermissions
from .serializers import CommentSerializer, PostSerializer, FollowSerializer, GroupSerializer
from django_filters.rest_framework import DjangoFilterBackend


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (PostAndCommentPermissions,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('group',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = (PostAndCommentPermissions,)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class FollowListCreateViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username']

    def get_queryset(self):
        return self.request.user.followers.all()

    def perform_create(self, serializer):
            
            if serializer.is_valid(raise_exception=True):
                if (not User.objects.filter(username=self.request.data.get('following')).exists()):
                    raise exceptions.ParseError()
                following = User.objects.get(username=self.request.data.get('following'))
                user = self.request.user
                if (following == user):
                    raise exceptions.ParseError()

                if Follow.objects.filter(following=following, user=user).exists():
                    raise exceptions.ParseError() 

                serializer.save(user=user, following=following)


class GroupCreateViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Group.objects.all()

    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
