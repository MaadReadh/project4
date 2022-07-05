from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Post(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
  content = models.TextField()
  date = models.DateTimeField(default=timezone.now)
  updated_dat = models.DateTimeField(auto_now=True)
  likes = models.IntegerField(default=0)

  def __str__(self):
        return f'{self.user} wrote post at {self.date}'

  class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


 

 
class Follower (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_profile')
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    user_following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', null=True)
    def __str__(self):
        return f'{self.user}:  has {self.user_follower} as follower'

    class Meta:
        verbose_name = 'Follower'
        verbose_name_plural = 'Followers'


 

class Like (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='userLike')
    posts = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='likePost')
    def __str__(self):
        return f'{self.user} like {self.posts}'

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'