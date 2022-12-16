from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from api.models import Post, Group, Follow, User
from api.permissions import IsOwnerOrReadOnly#, FollowPermission
from api.serializers import PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly, )
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['group', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs.get('id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs.get('id'))
        serializer.save(author=self.request.user, post=post)


class GroupView(mixins.CreateModelMixin,
                mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class FollowView(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 GenericViewSet):
    queryset = Follow.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['=user__username', '=following__username', ]

    def perform_create(self, serializer):
        following = get_object_or_404(User, username=self.request.data.get('following'))
        serializer.save(user=self.request.user, following=following)
