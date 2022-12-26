from django.urls import path, include
from rest_framework import routers
# from api.views import UserViewSet, PostViewSet, CommentViewSet
from api.views import PostListAPIView, PostRetrieveAPIView, CommentCreateAPIView, PostLikeAPIView, CateTagAPIView


# router = routers.DefaultRouter()
# router.register(r'user', UserViewSet)
# router.register(r'post', PostViewSet)
# router.register(r'comment', CommentViewSet)

# urlpatterns = [
#     path('', include(router.urls)),

# ]

urlpatterns = [
    path('post/', PostListAPIView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostRetrieveAPIView.as_view(), name='post-detail'),
    path('post/<int:pk>/like/', PostLikeAPIView.as_view(), name='post-like'),
    path('comment/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('catetag/', CateTagAPIView.as_view(), name='catetag')
]