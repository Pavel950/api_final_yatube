from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, serializers, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, FollowSerializer
from .serializers import GroupSerializer, PostSerializer
from posts.models import Follow, Group, Post

User = get_user_model()


class CreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(CreateListViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.all().filter(user=self.request.user)

    def perform_create(self, serializer):
        if (
            serializer.initial_data.get('following')
            == self.request.user.get_username()
        ):
            raise serializers.ValidationError(
                'Пользователь не может подписаться на себя самого!'
            )
        serializer.save(user=self.request.user)
