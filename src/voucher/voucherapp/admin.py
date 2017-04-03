# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.
from .models import Voucher, Person #, Credit

class PersonAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('__str__', 'personal_number', 'rfid', 'center', 'last_name', 'first_name','note', 'quantity', 'released', 'last_released',)
    list_filter = ('center', 'quantity', 'released', )
    search_fields = ('personal_number', 'rfid', 'center', 'last_name', 'first_name','note', 'quantity', 'released', 'last_released',)   
   
admin.site.register(Person, PersonAdmin)
      
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('person', 'datetime', )
    list_filter = ('datetime', )
    search_fields = ('person__personal_number',) # 'datetime', )
       
    def get_form(self, request, obj=None, **kwargs):    # Just added this override
        form = super(VoucherAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['person'].widget.can_add_related = False
        return form
    
admin.site.register(Voucher, VoucherAdmin)

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
admin.site.unregister(Group)


UserAdmin.fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Důležitá data'), {'fields': ('last_login', 'date_joined')}),
    )

def UserAdmin_get_form(self, request, obj=None, **kwargs):    # Just added this override
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['groups'].widget.can_add_related = False
        return form 
        
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

