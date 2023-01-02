from collections import OrderedDict
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from api.serializers import *
from blog.models import Post, Comment, Category, Tag
from .utils import *


def get_prev_next(instance):
    try:
        prev = instance.get_previous_by_updated_at()
    except instance.DoesNotExist:
        prev = None

    try:
        next_ = instance.get_next_by_updated_at()
    except instance.DoesNotExist:
        next_ = None

    return prev, next_


class PostPageNumberPagination(PageNumberPagination):
    page_size = 5
    # page_size_query_param = 'page_size'
    # max_page_size = 1000
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('postList', data),
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number),
        ]))


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    # serializer_class = PostListSerializer
    serializer_class = PostDetailSerializer
    pagination_class = PostPageNumberPagination

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': None, 
            'format': self.format_kwarg,
            'view': self
        }

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        prevInstance, nextInstance = get_prev_next(instance)
        commentList = instance.comment_set.all()

        data = {
            'post': instance,
            'prevPost': prevInstance,
            'nextPost': nextInstance,
            'comment': commentList,
        }

        serializer = self.get_serializer(instance=data)
        return Response(serializer.data)

    def get_queryset(self):
        return Post.objects.all().select_related('category').prefetch_related('tags', 'comment_set')

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     commentList = instance.comment_set.all()

    #     postDict = obj_to_post(instance)
    #     prevDict, nextDict = prev_next_post(instance)
    #     commentDict = [obj_to_comment(c) for c in commentList]

    #     dataDict = {
    #         'post': postDict,
    #         'prevPost': prevDict,
    #         'nextPost': nextDict,
    #         'comment': commentDict,
    #     }

    #     return Response(dataDict)

    # viewset에서 get method는 사용하지 않는다.
    def like(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like += 1
        instance.save()

        return Response(instance.like)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CateTagAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cateList = Category.objects.all()
        tagList = Tag.objects.all()

        data = {
            'cateList': cateList,
            'tagList': tagList,
        }

        serializer = CateTagSerializer(instance=data)
        return Response(serializer.data)