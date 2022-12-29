from collections import OrderedDict
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from api.serializers import *
from blog.models import Post, Comment, Category, Tag

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer


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


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            # image url을 경로만 나오게 하기 위해 오버라이딩 하고 request를 None값을 줌.
            # 해당 requestsms generics > fields.py > ImageField > FileField > def to_representation에서 처리됨.
            'request': None, 
            'format': self.format_kwarg,
            'view': self
        }


# class PostRetrieveAPIView(RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostRetrieveSerializer


# class PostLikeAPIView(UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostLikeSerializer

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         data = {'like' : instance.like + 1}
#         # data = instance.like + 1 # dictionary가 아닌 데이터는 에러 발생.
        
#         serializer = self.get_serializer(instance, data=data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}

#         # return Response(serializer.data)
#         # return test
#         return Response(data['like'])


class PostLikeAPIView(GenericAPIView): # APIView를 이용해서 하는 방법도 있음
    queryset = Post.objects.all()
    # serializer_class = PostLikeSerializer # 굳이 사용할 이유가 없어짐.

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like += 1
        instance.save()

        return Response(instance.like)


class CommentCreateAPIView(CreateAPIView):
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



class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

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