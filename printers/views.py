from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.template import RequestContext, Template, Context, loader
from django.template.loader import get_template
from django.core import serializers

from printers.models import *
import urllib2
import plistlib
import json

@login_required(redirect_field_name='')
def index(request):
    #show table with printer groups
    groups = PrinterList.objects.all()
    context = {'groups': groups,}
    return render(request, 'printers/index.html', context)
   
    
    
def detail(request, printerlist_id):
    pl = get_object_or_404(PrinterList, pk=printerlist_id)
    output = pl.printer.all()
    return render(request, 'printers/details.html', {'pl': output})
   
        
def getlist(request, printerlist_name):       
    pl = PrinterList.objects.all()
    for listname in pl:
        if listname.name == printerlist_name:
            i = listname
    
    pl=i.printer.all()
    output = []
    
    for p in pl:
        d = {
        'printer':p.name,
        'url':p.url, 
        'description':p.description,
        'location':p.location,
        'model':p.model,
        'ppd':p.ppd,
        'protocol':p.protocol,
        }
        
        opts = p.option_set.all()
        addopt = []
        for o in opts:
            addopt.append(o.option)
        
        if addopt:
            d['options'] = addopt
            
        output.append(d)
    
    data = {'printerList':output}
    
    detail=plistlib.writePlistToString(data)
    return HttpResponse(detail)
    