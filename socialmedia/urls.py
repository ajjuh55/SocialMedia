"""
URL configuration for socialmedia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from coco.views import *

urlpatterns = [
# Signup
path('signup/',SignupView.as_view()),
path('login/',LoginView.as_view()),
# Posts
path('post/',PostView.as_view()),
path('commonpost/',CommonPostView.as_view()),
path('post/<int:pk>/',PostRetrieveView.as_view()),
# Comments
path('comment/',CommentView.as_view()),
# Likes
path('like/',LikeView.as_view()),
path('unlike/<int:pid>/',UnLikeView.as_view()),
# Following
path('follow/',FollowingView.as_view()),
path('followers/',FollowersView.as_view()),
path('unfollow/<int:pk>/',UnFollowView.as_view()),
# Profile
path('profile/',ProfileView.as_view()),

]