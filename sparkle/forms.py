from django import forms
from django.forms import ModelForm, Select
from models import *

class AppcastForm(forms.ModelForm):
    class Meta:
        model = Version
        
    