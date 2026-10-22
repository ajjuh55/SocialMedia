from rest_framework import serializers
from coco.models import *

class UserSerializer(serializers.ModelSerializer):
    post_count=serializers.SerializerMethodField()
    followers_count=serializers.SerializerMethodField()
    following_count=serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "password", "phone","post_count","followers_count","following_count"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    def get_post_count(self,obj):
        return Post.objects.filter(owner=obj).count()
    def get_followers_count(self,obj):
            return Follow.objects.filter(following=obj).count()
    def get_following_count(self,obj):
            return Follow.objects.filter(follower=obj).count()
    

class PostSerializer(serializers.ModelSerializer):
    comment_count=serializers.SerializerMethodField()
    like_count=serializers.SerializerMethodField()
    comment=serializers.SerializerMethodField()
    class Meta:
        model=Post
        fields="__all__"
        read_only_fields=["id","created_at","owner"]

    def get_comment_count(self,obj):
        return Comment.objects.filter(post_obj=obj).count()

    def get_like_count(self,obj):
        return Like.objects.filter(post_obj=obj).count()

    def get_comment(self,obj):
        comments=Comment.objects.filter(post_obj=obj)
        return CommentSerializer(comments,many=True).data

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["id", "added_at", "owner"]

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields="__all__"
        read_only_fields=['owner_obj']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id","follower","following","created_at"]
        read_only_fields = ["id", "follower", "created_at"]