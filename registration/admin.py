from django.contrib import admin
from registration.models import User

class UserAdmin(admin.ModelAdmin): pass
admin.site.register(User, UserAdmin)

