from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    phone=models.CharField(max_length=15,unique=True)
    

class Post(models.Model):
    title=models.CharField(max_length=100,null=True)
    image=models.ImageField(upload_to="social_media_images")
    description=models.CharField(max_length=150,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="post")

class Comment(models.Model):
    comment=models.TextField(max_length=100)
    added_at=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="comment")
    post_obj=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comment")

class Like(models.Model):
    post_obj=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="likes")
    owner_obj=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="likes")
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=('post_obj','owner_obj')

class Follow(models.Model):
    follower=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="following")
    following=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="followers")
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together=('follower','following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"