from django import forms
from models import *

class PrinterListForm(forms.ModelForm):
    class Meta:
        model = PrinterList
        

class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        
