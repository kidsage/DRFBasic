from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import Post, Comment, Category, Tag


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


# class PostLikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['like']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


# class CateTagSerializer(serializers.Serializer): # 직접 필드를 정의하기 위해 modelserializer를 사용하지 않음.
#     cateList = CategorySerializer(many=True)
#     tagList = TagSerializer(many=True)


class CateTagSerializer(serializers.Serializer):
    cateList = serializers.ListField(child=serializers.CharField()) # many=True 대신에 Listfield를 사용할 수 있는데, 이는 drf에만 있는 기능.
    tagList = serializers.ListField(child=serializers.CharField())