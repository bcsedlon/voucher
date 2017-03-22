# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.
from .models import Voucher, Person #, Credit

class PersonAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('__str__', 'personal_number', 'rfid', 'center', 'last_name', 'first_name','note', 'quantity', 'released', 'last_released',)
    #list_filter = ('personal_number', 'rfid', 'center', 'last_name', 'first_name','note', 'quantity', 'released', 'last_released',)
    list_filter = ('center', 'quantity', 'released', )
    search_fields = ('personal_number', 'rfid', 'center', 'last_name', 'first_name','note', 'quantity', 'released', 'last_released',)   
   
admin.site.register(Person, PersonAdmin)

'''
class CreditAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('person', 'quantity', 'released', )
    list_filter = ('person', 'quantity', 'released', )
    search_fields = ('person', 'quantity', 'released', )
    
    def get_form(self, request, obj=None, **kwargs):    # Just added this override
        form = super(CreditAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['person'].widget.can_add_related = False
        #form.base_fields['person'].widget.can_edit_related = False
        return form
    
admin.site.register(Credit, CreditAdmin)
'''

'''
from django.forms import ModelForm, PasswordInput
from django import forms

class VoucherAdminForm(ModelForm):
    class Meta:
        model = Voucher
        fields = ['person', 'datetime']
        #password = forms.CharField(widget=forms.PasswordInput())
        #widgets = {'password': PasswordInput(),}
        #password = forms.CharField(widget=forms.PasswordInput(render_value = True))
        #password = forms.CharField(widget=PasswordInput())
        #password = forms.CharField(widget=forms.PasswordInput())
        #widgets = { 'password': forms.PasswordInput(render_value=True),}
'''        
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('person', 'datetime', )
    list_filter = ('datetime', )
    search_fields = ('person__personal_number',) # 'datetime', )
       
    def get_form(self, request, obj=None, **kwargs):    # Just added this override
        form = super(VoucherAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['person'].widget.can_add_related = False
        #form.base_fields['person'].widget.can_edit_related = False
        return form
    
    #list_display_links = None
    #form = VoucherAdminForm
    
admin.site.register(Voucher, VoucherAdmin)

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
#admin.site.unregister(User)

from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
admin.site.unregister(Group)


UserAdmin.fieldsets = (
        (None, {'fields': ('username', 'password')}),
        #(('Osobní údaje'), {'fields': ('first_name', 'last_name', 'email')}),        
        #(('Oprávnění'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}), #'groups')}),#, 'user_permissions')}),
        (('Důležitá data'), {'fields': ('last_login', 'date_joined')}),
    )

def UserAdmin_get_form(self, request, obj=None, **kwargs):    # Just added this override
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['groups'].widget.can_add_related = False
        return form 
        
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

