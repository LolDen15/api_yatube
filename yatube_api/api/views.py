from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission

from posts.models import Group, Post
from api.serializers import CommentSerializer, PostSerializer, GroupSerializer


class PermissionBaseClass(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method == 'GET' or obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, PermissionBaseClass)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, PermissionBaseClass)

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        return self.get_post().comments.all()
