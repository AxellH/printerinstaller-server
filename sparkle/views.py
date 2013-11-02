from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.contrib.sites.models import Site
from django.template.loader import get_template
from django.template import RequestContext, Template, Context, loader
from django.contrib.auth.decorators import login_required, permission_required
from forms import *
from sparkle.models import *

@login_required(redirect_field_name='')
def index(request):
    versions = Version.objects.all()
    a = Application.objects.all();
    print a.count()
    if a.count() > 0:
        initialized = True;
    else:
        initialized = False;
        
    print initialized
    
    site = Site.objects.get_current()
    context = {'versions':versions,'site':site,'initialized':a}
    
    return render(request, 'sparkle/index.html',context) 
    
@login_required(redirect_field_name='')
def initialize(request):
    app = Application(name='Printer-Installer')
    app.save()
    return redirect('sparkle.views.index')            
    
def appcast(request, name):
    """Generate the appcast for the given application while recording any system profile reports"""
    
    application = get_object_or_404(Application, name=name)
    
    # if there are get parameters from the system profiling abilities
    if len(request.GET):
        # create a report and records of the keys/values
        report = SystemProfileReport.objects.create(ip_address=request.META.get('REMOTE_ADDR'))
        for key, value in request.GET.iteritems():
            record = SystemProfileReportRecord.objects.create(report=report, key=key, value=value)
            record.save()
            
    print request.GET
    
    # get the latest versions
    versions = Version.objects.filter(application__name=name, active=True).order_by('-published')
    
    # get the current site for the domain
    site = Site.objects.get_current()
    
    return render_to_response('sparkle/appcast.xml', {'application': application, 'versions': versions, 'site': site})


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
    return render_to_response('sparkle/version_edit.html', {'form': form,'version':version}, context_instance=RequestContext(request))
    
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
    return render_to_response('sparkle/version_add.html', {'form': form,}, context_instance=RequestContext(request))

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
    
