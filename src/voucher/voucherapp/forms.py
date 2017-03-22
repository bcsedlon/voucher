from django import forms
from .models import Person

class RFIDForm(forms.Form):
    
    #CHOICES = (('Option 1', 'Option 1'),('Option 2', 'Option 2'),)
    #RFID = forms.ChoiceField(choices=CHOICES)
    
    
    #choices = [(obj.id, obj.rfid) for obj in Person.objects.all()]
    #person = forms.ModelChoiceField(required=False , queryset=choices, empty_label='', label='RFID')
    
    
    person = forms.ModelChoiceField(required=False , queryset=Person.objects.all(), empty_label='', to_field_name='rfid', label='Osoba')
    
    #def __init__(self, *args, **kwargs):
        #super(RFIDForm, self).__init__(*args, **kwargs)
        #field = forms.ChoiceField(choices=Person.objects.all())
