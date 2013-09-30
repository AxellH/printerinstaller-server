from django import forms
from models import *

class PrinterListForm(forms.ModelForm):
    class Meta:
        model = PrinterList
        
class OptionsForm(forms.ModelForm):
    class Meta:
        model = Option
        
class PrinterForm(forms.ModelForm):
    options = OptionsForm()
    class Meta:
        model = Printer
        options = OptionsForm()
        
    
        
