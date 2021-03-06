from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.contrib.sites.models import Site, RequestSite
from django.template.loader import get_template
from django.template import RequestContext, Template, Context, loader
from django.contrib.auth.decorators import login_required, permission_required
from printerinstaller.utils import site_info
from forms import *
from sparkle.models import *
from validators import *

@login_required(redirect_field_name='')
def index(request):
    versions = Version.objects.all()
    privateKey = PrivateKey.objects.all()
    if not Application.objects.all():
        Application(name='Printer-Installer').save()

    site = Site.objects.get_current()
    context = {'versions':versions, 'site':site, 'privateKey':privateKey}
    
    return render_to_response('sparkle/index.html', context, context_instance=RequestContext(request)) 
    
@login_required(redirect_field_name='')
def private_key_add(request):
    error = False
    if request.POST:
        if "cancel" in request.POST:
            return redirect('sparkle.views.index')

        form = PrivateKeyForm(request.POST, request.FILES)
        if form.is_valid():
            privateKey = form.save(commit=True)
            privateKey.save()            
            return redirect('sparkle.views.index')
        else:
            error = True          
    else:
        form = PrivateKeyForm()
    context = {'form':form, 'error':error}
    return render_to_response('sparkle/forms/private_key.html', context, context_instance=RequestContext(request)) 

@login_required(redirect_field_name='')
def private_key_edit(request, id):
    error = False
    privateKey=get_object_or_404(PrivateKey, pk=id)
    if request.POST:
        if "cancel" in request.POST:
            return redirect('sparkle.views.index')

        form = PrivateKeyForm(request.POST,request.FILES,instance=privateKey)
        if form.is_valid():
            form.save()            
            return redirect('sparkle.views.index')
    else:
        form = PrivateKeyForm(instance=privateKey)

    context = {'form': form,'privateKey':privateKey,'error':error}
    return render_to_response('sparkle/forms/private_key.html', context, context_instance=RequestContext(request)) 


@login_required(redirect_field_name='')
def version_edit(request, id):
    version=get_object_or_404(Version, pk=id)
    if request.POST:
        form = AppcastForm(request.POST,request.FILES,instance=version)
        if form.is_valid(): 
            form.save()            
        return redirect('sparkle.views.index')            
    else:
        form = AppcastForm(instance=version)
    return render_to_response('sparkle/forms/version.html', {'form': form,'version':version}, context_instance=RequestContext(request))
    
@login_required(redirect_field_name='')
def version_add(request):
    if request.POST:
        form = AppcastForm(request.POST,request.FILES)
        if form.is_valid():
            version = form.save(commit=True)
            version.save()            
        return redirect('sparkle.views.index')            
    else:
        form = AppcastForm(initial={'application':Application.objects.get(id=1)})
    return render_to_response('sparkle/forms/version.html', {'form': form,}, context_instance=RequestContext(request))

@login_required(redirect_field_name='')
def version_delete(request, id):
    version = get_object_or_404(Version, pk=id)
    if version:
        version.delete()
    return redirect('sparkle.views.index')
    
@login_required(redirect_field_name='')
def version_activate(request, id):
    version = get_object_or_404(Version, pk=id)
    if version.active:
        version.active=False
    else:
        version.active=True
    version.save()
    return redirect('sparkle.views.index')

###############################################################################################
### No Login Requierd Below This Point ########################################################
###############################################################################################

def appcast(request, name):
    """Generate the appcast for the given application while recording any system profile reports"""
    application = get_object_or_404(Application, name=name)
    site = site_info(request)

    # if there are get parameters from the system profiling abilities
    if len(request.GET):
        # create a report and records of the keys/values
        report = SystemProfileReport.objects.create(ip_address=request.META.get('REMOTE_ADDR'))
        for key, value in request.GET.iteritems():
            record = SystemProfileReportRecord.objects.create(report=report, key=key, value=value)
            record.save()
            
    # get the latest versions
    versions = Version.objects.filter(application__name=name, active=True).order_by('-published')

    # get the current site for the domain
    # site = Site.objects.get_current()
    
    return render_to_response('sparkle/appcast.xml', {'application': application, 'versions': versions, 'site': site})


