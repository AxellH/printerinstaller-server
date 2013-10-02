from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.template import RequestContext, Template, Context, loader
from django.template.loader import get_template
from django.forms.models import inlineformset_factory

from plistlib import writePlistToString

from printers.models import *
from forms import *


@login_required(redirect_field_name='')
def index(request):
    #show list of printers and groups
    printerlists = PrinterList.objects.all()
    printers = Printer.objects.all()
    context = {'printerlists': printerlists,'printers' : printers}
    return render(request, 'printers/index.html', context)


###################################
######  Printer Methods ###########
###################################
@login_required(redirect_field_name='')
def printer_details(request, id):
    printer = get_object_or_404(Printer, pk=id)
    return render(request, 'printers/printer_details.html', {'printer': printer})

@login_required(redirect_field_name='')
def add_printer(request):
    if request.method == 'POST':
        form = PrinterForm(request.POST)
        if form.is_valid():
            printer = form.save(commit=True)
            
            new_option = form.cleaned_data['new_option']
            if new_option:
                 printer.option.create(option=new_option)
            
            printer.save()
            return redirect('printers.views.printer_details', printer.id)            
    else:
        form = PrinterForm()
        
    return render_to_response('printers/add_printer.html', {'form': form,}, context_instance=RequestContext(request))


@login_required(redirect_field_name='')
def edit_printer(request, printer_id):
    printer=get_object_or_404(Printer, pk=printer_id)
    if request.POST:
        form = PrinterForm(request.POST,instance=printer)
        if form.is_valid(): 
            form.save()            
            new_option = form.cleaned_data['new_option']
            if new_option:
                 printer.option.create(option=new_option)            
                 printer.save()
        return redirect('printers.views.printer_details', printer.id)            
    else:
        form = PrinterForm(instance=printer)
        
    return render_to_response('printers/edit_printer.html', {'form': form,'printer':printer}, context_instance=RequestContext(request))
    
@login_required(redirect_field_name='')
def del_printer(request, id):
    printer = get_object_or_404(Printer, pk=id)
    if printer:
        printer.delete()
    return redirect('printers.views.index')
    


########################################
######  Printer List Methods ###########
########################################  
@login_required(redirect_field_name='')
def add_printerlist(request):
    if request.method == 'POST':
        form = PrinterListForm(request.POST)
        if form.is_valid():
            printerlist = form.save(commit=True)
            printerlist.save()
            return redirect('printers.views.printerlist_details', printerlist.id)
    else:
        form = PrinterListForm()
    return render_to_response('printers/add_printerlist.html', {'form': form,}, context_instance=RequestContext(request))
    
@login_required(redirect_field_name='')
def printerlist_details(request, id):
    printerlist = get_object_or_404(PrinterList, pk=id)
    return render(request, 'printers/printerlist_details.html', {'printerlist': printerlist})

@login_required(redirect_field_name='')
def edit_printerlist(request, printerlist_id):
    printerlist = PrinterList.objects.get(id=printerlist_id)  
    if request.POST:
        form = PrinterListForm(request.POST,instance=printerlist)
        if form.is_valid():
            form.save()
            return redirect('printers.views.printerlist_details', printerlist.id)
    else:
        form = PrinterListForm(instance=printerlist)
    return render_to_response('printers/edit_printerlist.html', {'form': form,'printerlist':printerlist}, context_instance=RequestContext(request))
    
@login_required(redirect_field_name='')
def del_printerlist(request, id):
    p = get_object_or_404(PrinterList, pk=id)
    p.delete()
    return redirect('printers.views.index')



## This is the request that returns the plist for the Printer-Installer.app
## it should be the only area that requires no login
def getlist(request, name):       
    pl = PrinterList.objects.all()
    for listname in pl:
        if listname.name == name:
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
        
        opts = p.option.all()
        addopt = []
        for o in opts:
            addopt.append(o.option)
        
        if addopt:
            d['options'] = addopt
            
        output.append(d)
        
    detail=writePlistToString({'printerList':output})
    return HttpResponse(detail)
    