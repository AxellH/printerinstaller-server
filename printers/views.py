from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.template import RequestContext, Template, Context, loader
from django.template.loader import get_template
from django.forms.models import inlineformset_factory
from django.conf import settings

from plistlib import writePlistToString

from printers.models import *
from sparkle.models import *
from forms import *

def index(request):
    printerlists = PrinterList.objects.all()
    version = Version.objects.filter(application__name='Printer-Installer', active=True).order_by('-published')[0]
    context = {'printerlists': printerlists, 'version':version}
    return render(request, 'printers/index.html', context)

@login_required(redirect_field_name='')
def manage(request):
    #show list of printers and groups
    printerlists = PrinterList.objects.all()
    printers = Printer.objects.all()
    printer_form = PrinterForm(request.POST,request.FILES)
    
    context = {'printerlists': printerlists,'printers' : printers,'printer_form':printer_form}
    return render(request, 'printers/manage.html', context)


###################################
######  Printer Methods ###########
###################################
@login_required(redirect_field_name='')
def printer_details(request, id):
    printer = get_object_or_404(Printer, pk=id)
    return render(request, 'printers/printer_details.html', {'printer': printer})

@login_required(redirect_field_name='')
def printer_add(request):
    if request.method == 'POST':
        form = PrinterForm(request.POST,request.FILES)
        if form.is_valid():
            printer = form.save(commit=True)
            new_option = form.cleaned_data['new_option']
            if new_option:
                 printer.option.create(option=new_option)
            printer.save()
            return redirect('printers.views.index')            
    else:
        form = PrinterForm()
        
    return render_to_response('printers/add_printer.html', {'form': form,}, context_instance=RequestContext(request))


@login_required(redirect_field_name='')
def printer_edit(request, printer_id):
    printer=get_object_or_404(Printer, pk=printer_id)
    if request.POST:
        form = PrinterForm(request.POST,request.FILES,instance=printer)
        if form.is_valid(): 
            form.save()            
            new_option = form.cleaned_data['new_option']
            if new_option:
                 printer.option.create(option=new_option)            
            printer.save()
            return redirect('printers.views.manage')            
    else:
        form = PrinterForm(instance=printer)
        
    return render_to_response('printers/edit_printer.html', {'form': form,'printer':printer}, context_instance=RequestContext(request))
    
@login_required(redirect_field_name='')
def printer_delete(request, id):
    printer = get_object_or_404(Printer, pk=id)
    if printer:
        printer.delete()
    return redirect('printers.views.manage')
    


########################################
######  Printer List Methods ###########
########################################  
@login_required(redirect_field_name='')
def printerlist_add(request):
    if request.method == 'POST':
        form = PrinterListForm(request.POST)
        if form.is_valid():
            printerlist = form.save(commit=True)
            printerlist.save()
            return redirect('printers.views.manage')            
    else:
        form = PrinterListForm()
    return render_to_response('printers/add_printerlist.html', {'form': form,}, context_instance=RequestContext(request))
    
@login_required(redirect_field_name='')
def printerlist_details(request, id):
    printerlist = get_object_or_404(PrinterList, pk=id)
    return render(request, 'printers/printerlist_details.html', {'printerlist': printerlist})

@login_required(redirect_field_name='')
def printerlist_edit(request, printerlist_id):
    printerlist = PrinterList.objects.get(id=printerlist_id)  
    if request.POST:
        form = PrinterListForm(request.POST,instance=printerlist)
        if form.is_valid():
            form.save()
            return redirect('printers.views.manage')            
    else:
        form = PrinterListForm(instance=printerlist)
    return render_to_response('printers/edit_printerlist.html', {'form': form,'printerlist':printerlist}, context_instance=RequestContext(request))
    
@login_required(redirect_field_name='')
def printerlist_delete(request, id):
    p = get_object_or_404(PrinterList, pk=id)
    p.delete()
    return redirect('printers.views.manage')

########################################
#########  Option Methods ##############
########################################  
@login_required(redirect_field_name='')
def options_list(request):
    options = Option.objects.all()
    return render(request, 'printers/options_list.html', {'options': options})

@login_required(redirect_field_name='')
def options_add(request):
    if request.method == 'POST':
        form = OptionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('printers.views.options_list')
    else:
        form = OptionsForm()
    return render_to_response('printers/add_option.html', {'form': form,}, context_instance=RequestContext(request))
    
    
   
@login_required(redirect_field_name='')
def options_delete(request,id):
    o = get_object_or_404(Option, pk=id)
    o.delete()
    return redirect('printers.views.options_list')
    

## This is the request that returns the plist for the Printer-Installer.app
## it should be the only area that requires no login
def getlist(request, name):       
    pl = get_object_or_404(PrinterList, name=name)    
    printers=pl.printer.all()
    plist = []
    
    for p in printers:
        if(p.ppd_file):
            ppd_url=p.ppd_file.url
        else:
            ppd_url=''
            
        d = {
        'name':p.name,
        'host':p.host,
        'protocol':p.protocol,
        'description':p.description,
        'location':p.location,
        'model':p.model,
        'ppd_url':ppd_url,
        }
        
        opts = p.option.all()
        addopt = []
        for o in opts:
            addopt.append(o.option)
        
        if addopt:
            d['options'] = addopt
            
        plist.append(d)
        
    detail=writePlistToString({'printerList':plist,'updateServer':settings.HOST_SPARKLE_UPDATES[1]})
    return HttpResponse(detail)
    