from django import forms
from django.forms import ModelForm, Select
from models import *

class PrinterListForm(forms.ModelForm):
    class Meta:
        model = PrinterList
    printer = forms.ModelMultipleChoiceField(queryset=Printer.objects.all(),widget = forms.CheckboxSelectMultiple,required=False)
        
class OptionsForm(forms.ModelForm):
    class Meta:
        model = Option
    
class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
    
    ppd_file = forms.FileField(label='choose a ppd', required=False)
    new_option = forms.CharField(max_length=100,required=False)
    option = forms.ModelMultipleChoiceField(queryset=Option.objects.all(),widget = forms.CheckboxSelectMultiple,required=False)
    