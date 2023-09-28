from django.contrib import admin

# Register your models here.

from intro.models import MyUser,boardobject
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(MyUser,UserAdmin)
admin.site.register(boardobject)
UserAdmin.fieldsets +=("Custom",{'fields':('mobile_number','birth_date')}),