from django.contrib import admin

# Register your models here.
from network.models import *

# admin.site.register(Like)
admin.site.register(Post)
admin.site.register(Follower)