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
        
    name=forms.CharField(max_length=100,label='Priner Name*',help_text='CUPS compliant name, No spaces or CAPS, must start with letter')
    protocol=forms.CharField(max_length=100,label='Protocol*',help_text='(socket,lpd,ipp or http)')
    host=forms.CharField(max_length=100,label='Host*',help_text='(FQDN or IP Address of printer or server)')

    model=forms.CharField(max_length=100,label='Printer Model',help_text='(As Listed with lpinfo -m)',required=False)
    ppd_file = forms.FileField(label='PPD File', required=False)
    new_option = forms.CharField(max_length=100,required=False)
    option = forms.ModelMultipleChoiceField(queryset=Option.objects.all(),widget = forms.CheckboxSelectMultiple,required=False)
    