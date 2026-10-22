from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.generics import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from coco.permissions import IsOwner
from coco.models import *
from coco.serializers import *

# Create your views here.
class SignupView(CreateAPIView):
    serializer_class=UserSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username,password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'msg': 'Login successful','token': token.key})

        return Response({'msg': 'Invalid username or password'},status=status.HTTP_400_BAD_REQUEST)
    
class PostView(CreateAPIView,ListAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsOwner]
     
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)
    
class CommonPostView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
      
class PostRetrieveView(RetrieveAPIView,UpdateAPIView,DestroyAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsOwner,IsAuthenticated]
        
class CommentView(CreateAPIView,ListAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
class LikeView(CreateAPIView,ListAPIView):
    queryset=Like.objects.all()
    serializer_class=LikeSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def perform_create(self, serializer):
        post_obj = serializer.validated_data['post_obj']
        if Like.objects.filter(post_obj=post_obj,owner_obj=self.request.user).exists():
            raise ValidationError("You already liked this post")
        serializer.save(owner_obj=self.request.user)

class UnLikeView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def post(srlf,request,pid):
        try:
            like_obj=Like.objects.get(post_obj_id=pid,owner_obj=request.user)
            like_obj.delete()
            return Response({"msg":"Unliked Successfully"},status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({"msg":"You have not liked this post"},status=status.HTTP_400_BAD_REQUEST)
        
class FollowingView(CreateAPIView,ListAPIView):
    queryset=Follow.objects.all()
    serializer_class=FollowSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

class FollowersView(ListAPIView):
    serializer_class=FollowSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(following=self.request.user)

    
class UnFollowView(DestroyAPIView):
    queryset=Follow.objects.all()
    serializer_class=FollowSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

class ProfileView(RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
