from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import Post, Comment


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'image', 'like', 'category']


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'image', 'like', 'category']


class PostRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = ['id', 'title', 'image', 'like', 'category']
        # exclude 기능을 이용해서 빼는 것만 지정하는 방법도 있다.
        exclude = ['created_at',]


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['like']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'