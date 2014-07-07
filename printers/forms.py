from django import forms
from django.forms import ModelForm, Select

from models import *
from validators import *
from extras import supported_protocols
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
    
    name=forms.CharField(max_length=50,label='Priner Name*',help_text='CUPS compliant name, No spaces or CAPS, must start with letter',validators=[validate_printer_name])
    protocol = forms.ChoiceField(choices=supported_protocols, label=u'Protocol*',validators=[validate_protocol])
    host=forms.CharField(max_length=50,label='Host*',help_text='(FQDN or IP Address of printer or server)')

    model=forms.CharField(max_length=50,label='Printer Model',help_text='(As Listed with lpinfo -m)',required=False)
    ppd_file = forms.FileField(label='PPD File', required=False)
    new_option = forms.CharField(max_length=50,required=False)
    option = forms.ModelMultipleChoiceField(queryset=Option.objects.all(),widget = forms.CheckboxSelectMultiple,required=False)
    


        