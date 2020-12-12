

from django.contrib import admin
from .models import Contact_form,User_Detail
from django.contrib.auth.admin import User

#sigunp form

class ContactToAdmin(admin.ModelAdmin):
    list_display = ('id','Name','Email','Contact','Message')

admin.site.register(Contact_form, ContactToAdmin)


# admin.site.register(extendeduser)


class RegisterAdmin(admin.ModelAdmin):
    list_display = ['Name','gmail_id','Age','City','State','Country','Phone_Number']

admin.site.register(User_Detail,RegisterAdmin)