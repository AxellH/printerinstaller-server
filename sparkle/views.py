from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.contrib.sites.models import Site
from django.template.loader import get_template
from django.template import RequestContext, Template, Context, loader
from django.contrib.auth.decorators import login_required, permission_required
from forms import *
from sparkle.models import *


def appcast(request, name):
    """Generate the appcast for the given application while recording any system profile reports"""
    
    application = get_object_or_404(Application, name=name)
    
    # if there are get parameters from the system profiling abilities
    if len(request.GET):
        # create a report and records of the keys/values
        report = SystemProfileReport.objects.create(ip_address=request.META.get('REMOTE_ADDR'))
        for key, value in request.GET.iteritems():
            record = SystemProfileReportRecord.objects.create(report=report, key=key, value=value)
    
    # get the latest versions
    versions = Version.objects.filter(application__name=name, active=True).order_by('-published')
    
    # get the current site for the domain
    site = Site.objects.get_current()
    
    return render_to_response('sparkle/appcast.xml', {'application': application, 'versions': versions, 'site': site})

@login_required(redirect_field_name='')
def index(request):
    apps = Version.objects.all()
    site = Site.objects.get_current()
    context = {'apps':apps,'site':site}
    
    return render(request, 'sparkle/index.html',context) 
    
@login_required(redirect_field_name='')
def appcast_edit(request, appcast_id):
    appcast=get_object_or_404(Version, pk=appcast_id)
    if request.POST:
        form = AppcastForm(request.POST,request.FILES,instance=appcast)
        if form.is_valid(): 
            form.save()            
        return redirect('sparkle.views.index')            
    else:
        form = AppcastForm(instance=appcast)
    return render_to_response('sparkle/appcast_edit.html', {'form': form,'appcast':appcast}, context_instance=RequestContext(request))
    
@login_required(redirect_field_name='')
def appcast_add(request):
    if request.POST:
        form = AppcastForm(request.POST,request.FILES)
        if form.is_valid():
            appcast = form.save(commit=True)
            appcast.save()            
        return redirect('sparkle.views.index')            
    else:
        form = AppcastForm()
    return render_to_response('sparkle/appcast_add.html', {'form': form,}, context_instance=RequestContext(request))

