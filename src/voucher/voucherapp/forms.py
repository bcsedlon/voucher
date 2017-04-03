from django import forms
from .models import Person

class RFIDForm(forms.Form):
    
    person = forms.ModelChoiceField(required=False , queryset=Person.objects.all(), empty_label='', to_field_name='rfid', label='Osoba')
    printout = forms.BooleanField(required=False ,initial=False, label='Tisk')

