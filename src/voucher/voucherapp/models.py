# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Create your models here.

class Person(models.Model):
    #rfid = models.IntegerField(unique=True, default=0, verbose_name='RFID', help_text='') #EA00022F7ABD 257285757565629
    #rfid = HexField(unique=True, default=0, verbose_name='RFID', help_text='') #EA00022F7ABD 257285757565629
    rfid = models.CharField(unique=True, max_length=16, verbose_name='RFID', help_text='')
    personal_number = models.CharField(unique=True, null=False, blank=False, max_length=16, verbose_name='Osobní číslo', help_text='') 
    center = models.IntegerField(default=0, verbose_name='Středisko', help_text='')
    
    first_name = models.CharField(null=False, blank=True, max_length=64, verbose_name='Křestní jméno')
    last_name = models.CharField(null=False, blank=True, max_length=64, verbose_name='Příjmení')
    note = models.CharField(null=False, blank=True, max_length=256, verbose_name='Poznámka')
    
    quantity = models.IntegerField(default=0, verbose_name='počet kupónů na měsíc', help_text='')
    released = models.IntegerField(default=0, verbose_name='počet vydaných kupónů za měsíc', help_text='')
    last_released = models.DateTimeField(null=True, blank=True, verbose_name='datum a čas vydání', help_text='')
    
    
    def __str__(self):
        return str(self.personal_number) #+ ' ' + self.last_name + ' ' + self.first_name
        
        # This method will be used in the admin display
    
    class Meta:
        verbose_name = 'Osoba'
        verbose_name_plural = '  Osoby'
        #ordering = ('user',)

'''       
class Credit(models.Model):
    #groups = models.ManyToManyField(Group, blank=True, verbose_name='skupiny uživatelů') 
    person = models.OneToOneField(Person, related_name='credit_person', verbose_name='Osoba')
    quantity = models.IntegerField(default=0, verbose_name='počet kupónů na měsíc', help_text='')
    released = models.IntegerField(default=0, verbose_name='počet vydaných kupónů za měsíc', help_text='')
    
    def __str__(self):
        return str(self.person) + ': ' + str(self.quantity)
        
    class Meta:
        verbose_name = 'Nárok'
        verbose_name_plural = ' Nároky'
        ordering = ('person',)
'''

class Voucher(models.Model):
    person = models.ForeignKey(Person, related_name='voucher_user', verbose_name='Osoba')
    datetime = models.DateTimeField(verbose_name='datum a čas vydání', help_text='')
    
    def __str__(self):
        return str(self.person) + ': ' + str(self.datetime)
        
    class Meta:
        verbose_name = 'Poukaz'
        verbose_name_plural = 'Poukazy'
        ordering = ('person',)
