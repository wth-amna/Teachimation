from django.contrib import admin
from .models import User, Topic

# Register your models here.
admin.site.register(Topic)
admin.site.register(User)