from django.contrib import admin
from .models import Hashtag, Message, Profile

# Register your models here.
admin.site.register(Hashtag)
admin.site.register(Profile)
admin.site.register(Message)
