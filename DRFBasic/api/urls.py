from django.urls import path, include
from rest_framework import routers
# from api.views import UserViewSet, PostViewSet, CommentViewSet
# from api.views import PostListAPIView, PostRetrieveAPIView, CommentCreateAPIView, PostLikeAPIView, CateTagAPIView
from api.views import PostViewSet, CommentViewSet, CateTagAPIView


# router = routers.DefaultRouter()
# router.register(r'user', UserViewSet)
# router.register(r'post', PostViewSet)
# router.register(r'comment', CommentViewSet)

# urlpatterns = [
#     path('', include(router.urls)),

# ]

# urlpatterns = [
#     path('post/', PostListAPIView.as_view(), name='post-list'),
#     path('post/<int:pk>/', PostRetrieveAPIView.as_view(), name='post-detail'),
#     path('post/<int:pk>/like/', PostLikeAPIView.as_view(), name='post-like'),
#     path('comment/', CommentCreateAPIView.as_view(), name='comment-create'),
#     path('catetag/', CateTagAPIView.as_view(), name='catetag')
# ]

# router 안쓰고 viewset url 셋업하는 방법.
urlpatterns = [
    path('post/', PostViewSet.as_view(actions={'get': 'list',}), name='post-list'),
    path('post/<int:pk>/', PostViewSet.as_view(actions={'get': 'retrieve',}), name='post-detail'),
    path('post/<int:pk>/like/', PostViewSet.as_view(actions={'get': 'like',}), name='post-like'),
    path('comment/', CommentViewSet.as_view(actions={'post': 'create',}), name='comment-create'),
    path('catetag/', CateTagAPIView.as_view(), name='catetag')
]