'''A collection of helper functions'''
import os

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.conf import settings

from printers.models import SubscriptionPrinterList
from sparkle.models import Version

from printerinstaller.utils import site_info

def github_latest_release(repo_dict):
    """Download the latest release based on a 
    a user's repo"""
    user = repo_dict['user']
    repo = repo_dict['repo']
    print repo_dict

    print user
    print repo

    if not user or not repo:
        return None

    supported_file_types = ['dmg', 'zip', 'gz']
    
    try:
        dest = str(u'https://api.github.com/repos/%s/%s/releases' % (user, repo))    
        data = json.load(urllib2.urlopen(dest))
        latest_release = data[0]['assets'][0]['browser_download_url']
        for file_type in supported_file_types:
            if latest_release.lower().endswith(file_type):
                return latest_release
    except IndexError:
        pass
    
    return None
    
def generate_printer_dict_from_list(request, list_object):
    '''constructs an xml/plist from djanog objects.all()'''
    
    plist = []
    _site_info = site_info(request)
    printers = list_object.printer.all()

    if settings.SERVE_FILES and Version.objects.all():
        _site_info = site_info(request)
        update_server = os.path.join(_site_info['root'], \
                                     _site_info['subpath'], \
                                     'sparkle/Printer-Installer/appcast.xml',)
    else:
        update_server = settings.GITHUB_APPCAST_URL

    for printer in printers:
        if printer.ppd_file and 'root' in _site_info:
            ppd_url = os.path.join(_site_info['root']) + printer.ppd_file.url
        else:
            ppd_url = ''
            
        printer_dict = {'name':printer.name, \
                        'host':printer.host, \
                        'protocol':printer.protocol, \
                        'description':printer.description, \
                        'location':printer.location, \
                        'model':printer.model, \
                        'ppd_url':ppd_url,}
        
        opts = printer.options.all()
        addopt = []
        for opt in opts:
            addopt.append(opt.option)
        
        if addopt:
            printer_dict['options'] = addopt
        
        # If the class is a subscripton list override
        #  the location property with the subnet variable
        if isinstance(list_object, SubscriptionPrinterList):
            printer_dict['location'] = '%s_pi-printer' % (list_object.subnet) 

        plist.append(printer_dict)

    xml = {'printerList':plist, 'updateServer':update_server}
    return xml


def auto_process_form(request, id, cls, form_cls, template, redir):
    '''Convience function when form needs not special post processing'''
    instance = None
    if id:
        instance = cls.objects.get(id=id)  
    if request.POST:
        form = form_cls(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(redir)            
    else:
        form = form_cls(instance=instance)
    return render_to_response(template, \
        {'form': form, 'instance':instance}, context_instance=RequestContext(request))

