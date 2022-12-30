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
    # source를 가져올 때 해당 데이터가 null값만 있는 경우는 default를 지정해줘야 에러가 나지 않는다.
    category = serializers.CharField(source='category.name', default=None)

    class Meta:
        model = Post
        fields = ['id', 'title', 'image', 'like', 'category']


class PostRetrieveSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        # fields = ['id', 'title', 'image', 'like', 'category']
        # exclude 기능을 이용해서 빼는 것만 지정하는 방법도 있다.
        exclude = ['created_at',]


class PostSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title']


class CommentSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'updated_at']


class PostDetailSerializer(serializers.Serializer):
    post = PostRetrieveSerializer()
    prevPost = PostSubSerializer()
    nextPost = PostSubSerializer()
    commentList = CommentSubSerializer(many=True, default=None)


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