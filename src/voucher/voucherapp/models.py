# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Create your models here.

class NullableCharField(models.CharField):
    description = "CharField that stores NULL but returns ''"
    #__metaclass__ = models.SubfieldBase
    #def from_db_value(self, value, expression, connection, context):
    #    return models.CharField.from_db_value(self, value, expression, connection, context)
    def to_python(self, value):
        if isinstance(value, models.CharField):
            return value
        return value or ''
    def get_prep_value(self, value):
        return value or None
        

class Person(models.Model):
    #rfid = models.CharField(unique=True, max_length=16, verbose_name='RFID', help_text='')
    rfid = NullableCharField(blank=True, null=True, default=None, unique=True, max_length=16, verbose_name='RFID', help_text='')
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
        
    class Meta:
        verbose_name = 'Osoba'
        verbose_name_plural = '  Osoby'

class Voucher(models.Model):
    person = models.ForeignKey(Person, related_name='voucher_user', verbose_name='Osoba')
    datetime = models.DateTimeField(verbose_name='datum a čas vydání', help_text='')
    
    def __str__(self):
        return str(self.person) + ': ' + str(self.datetime)
        
    class Meta:
        verbose_name = 'Poukaz'
        verbose_name_plural = 'Poukazy'
        ordering = ('person',)
