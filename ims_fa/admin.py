from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CustomerUserAdmin(UserAdmin):
    list_display = ('id','username', 'email', 'first_name', 'last_name', 'is_staff')
    ordering = ('id',)


admin.site.unregister(User)
admin.site.register(User, CustomerUserAdmin)