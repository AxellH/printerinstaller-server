'''Views'''
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect, render

from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext, Template
from django.template.loader import get_template
from django.forms.models import inlineformset_factory
from django.conf import settings
from urlparse import urlunparse
from plistlib import writePlistToString

import datetime

from sparkle.models import Version, GitHubVersion

from printerinstaller.utils import get_client_ip

from printers.models import *
from printers.forms import *
from printers.utils import generate_printer_dict_from_list, \
                           auto_process_form, \
                           github_latest_release

def index(request):
    '''index page'''
    printerlists = PrinterList.objects.filter(public=True)
    subscriptions = SubscriptionPrinterList.objects.all().count > 0


    version_url = None
    if settings.HOST_SPARKLE_UPDATES:
        version = Version.objects.filter(application__name='Printer-Installer', active=True).order_by('-published')
        if version:
            version_url = version[0].update.url
    
    # If we're not hosting updates, or it has yet to be 
    # Configured with any releases, use the GitHub project page's release.
    if not version_url:
        # We only need one object, so get it or create it
        try:
            version = GitHubVersion.objects.filter(pk=1)[0]
        except IndexError:
            version = GitHubVersion()

        # Check-in with github once a day for new releases
        # use the locally stored value every other time
        today = datetime.datetime.today
        last_checked = version.url
        version_url = version.url

        if not last_checked or not version_url or last_checked < today:
            version_url = github_latest_release(settings.GITHUB_LATEST_RELEASE)
            if version_url: 
                version.url = version_url
                version.last_checked = today()
                version.save()

    host = request.get_host()
    subpath = request.META.get('SCRIPT_NAME')
    scheme = request.is_secure() and 'printerinstallers' or 'printerinstaller'
    org = settings.ORGANIZATION_NAME

    pr_uri = urlunparse([scheme, host, subpath, None, None, None])
    context = {'domain':pr_uri, 
               'printerlists': printerlists,
               'subscriptions':subscriptions, 
               'version':version_url,
               'organization':org}
    
    return render(request, 'printers/index.html', context)

@login_required(redirect_field_name='')
def manage(request):
    '''show list of printers and groups'''
    printerlists = PrinterList.objects.all()
    subscription_lists = SubscriptionPrinterList.objects.all()
    printers = Printer.objects.all()
    options = Option.objects.all()
        
    context = {'printerlists':printerlists, 
               'subscription_lists':subscription_lists,
               'printers':printers,
               'options':options}

    return render(request, 'printers/manage.html', context)


########################################################################
#####  Forms     #######################################################
########################################################################
@login_required(redirect_field_name='')
def printer_form(request, id=None):
    '''edit printer object'''
    instance = None
    if id:
        instance = get_object_or_404(Printer, pk=id)
    if request.POST:
        form = PrinterForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(commit=True)

            # We have to pre-save the form in order 
            # to create the ManyToMany field relationship
            new_option = form.cleaned_data['new_option']
            if new_option:
                instance.options.create(option=new_option)            
                instance.save()
            return redirect('printers.views.manage')            
    else:
        form = PrinterForm(instance=instance)
        
    return render_to_response('printers/forms/printer.html', \
                             {'form': form, 'instance':instance}, \
                             context_instance=RequestContext(request))

@login_required(redirect_field_name='')
def printerlist_form(request, id=None):
    '''edit printer list object'''

    return auto_process_form(request,
                             id, 
                             PrinterList,
                             PrinterListForm,
                             'printers/forms/printerlist.html',
                             'printers.views.manage')

@login_required(redirect_field_name='')
def subscription_list_form(request, id=None):
    '''edit printer list object'''
    return auto_process_form(request,
                             id, 
                             SubscriptionPrinterList,
                             SubscriptionPrinterListForm,
                             'printers/forms/subscription_list.html',
                             'printers.views.manage')

@login_required(redirect_field_name='')
def options_form(request, id=None):
    '''Add/Edit options'''
    return auto_process_form(request,
                             id, 
                             Option,
                             OptionForm,
                             'printers/forms/option.html',
                             'printers.views.manage')


###################################
######  Printer Methods ###########
###################################
@login_required(redirect_field_name='')
def printer_details(request, id):
    '''show printer printer'''
    printer = get_object_or_404(Printer, pk=id)
    return render(request, 
                  'printers/printer_details.html',
                  {'printer': printer})
    
@login_required(redirect_field_name='')
def printer_delete(request, id):
    '''Delete printer object'''
    printer = get_object_or_404(Printer, pk=id)
    if printer:
        printer.delete()
    return redirect('printers.views.manage')
    

########################################
######  Printer List Methods ###########
########################################  
@login_required(redirect_field_name='')
def printerlist_details(request, id):
    '''show details of a printer list'''
    printerlist = get_object_or_404(PrinterList, pk=id)
    return render(request, 
                  'printers/printerlist_details.html',
                  {'printerlist': printerlist})
    
@login_required(redirect_field_name='')
def printerlist_delete(request, id):
    '''delete printer list object'''
    printerlist = get_object_or_404(PrinterList, pk=id)
    printerlist.delete()
    return redirect('printers.views.manage')

@login_required(redirect_field_name='')
def printerlist_public(request, id):
    '''Toggle the printer list public/private'''
    instance = get_object_or_404(PrinterList, pk=id)
    instance.public = not instance.public
    instance.save()
    return redirect('printers.views.manage')

############################################
######  Subscripton List Methods ###########
############################################  
    
@login_required(redirect_field_name='')
def subscription_list_delete(request, id):
    '''delete printer list object'''
    printerlist = get_object_or_404(PrinterList, pk=id)
    printerlist.delete()
    return redirect('printers.views.manage')


########################################
#########  Option Methods ##############
########################################  
@login_required(redirect_field_name='')
def options_delete(request,id):
    option = get_object_or_404(Option, pk=id)
    option.delete()
    return redirect('printers.views.manage')
    


###############################################
## This is the request that returns the plist #
## for the Printer-Installer.app it should    #
## be the only area that requires no login    #
###############################################
def getlist(request, name):
    '''display the xml plist for the client'''
    printer_list_object = get_object_or_404(PrinterList, name=name)    
    p_dict = generate_printer_dict_from_list(request, printer_list_object)
    
    plist = writePlistToString(p_dict)

    return HttpResponse(plist, content_type='application/xml')

def get_subscription_list(request):
    '''get the printers avaliable for a given subnet'''

    # TODO: Get subnet from request
    client_ip = get_client_ip(request)
    printer_list_object = SubscriptionPrinterList.instance_for_ip(client_ip)
    p_dict = generate_printer_dict_from_list(request, printer_list_object)
    
    p_dict['subnet'] = printer_list_object.subnet
    plist = writePlistToString(p_dict)

    return HttpResponse(plist, content_type='application/xml')
    
