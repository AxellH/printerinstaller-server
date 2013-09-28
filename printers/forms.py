from django import forms
from models import *

class PrinterGroupForm(forms.ModelForm):
    class Meta:
        model = PrinterGroup

class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        
