import os
import subprocess
import zipfile
import tempfile
import shutil
import plistlib
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from validators import *
from printerinstaller.utils import get_dsa_signature, delete_file_on_change


class PrivateKey(models.Model):
    def clean(self):
        validate_only_one_instance(self)
    
    """The DSA Key to sign the update"""
    private_key = models.FileField(upload_to='private/')

class Application(models.Model):
    """A sparkle application"""
    
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Version(models.Model):
    """A version for a given application"""
    
    application = models.ForeignKey(Application)
    
    title = models.CharField(max_length=100)
    version = models.CharField(blank=True, null=True, max_length=10)
    short_version = models.CharField(blank=True, null=True, max_length=50)
    dsa_signature = models.CharField(blank=True, null=True, max_length=80)
    length = models.CharField(blank=True, null=True, max_length=20)
    release_notes = models.TextField(blank=True, null=True)
    minimum_system_version = models.CharField(blank=True, null=True, max_length=10)
    published = models.DateTimeField(auto_now_add=True)
    update = models.FileField(upload_to='sparkle/')
    active = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        pre_update_path = self.update.path
        super(Version, self).save(*args, **kwargs)

        update_fields = []
        if not pre_update_path == self.update.path:
            
            pks = PrivateKey.objects.all()[:1].get()
            if pks:
                spk=pks.private_key.path

            if spk or not self.dsa_signature:
                if os.path.exists(spk):
                    self.dsa_signature = get_dsa_signature(self.update.path,spk)
                    update_fields.append('dsa_signature')

            # if there is no length and it is a zip file
            # extract it to a tempdir and calculate the length
            # also parse the plist file for versions
            if not self.length and self.update.path.endswith('.zip'):
                    zip_file = zipfile.ZipFile(self.update.path)
                    tempdir = tempfile.mkdtemp()
                    files = zip_file.namelist()
                    start_path = None
                    
                    for f in files:
                        if f.endswith('/'):
                            d = os.path.join(tempdir, f)
                            if not start_path:
                                start_path = d        
                                os.makedirs(d)
                        else:
                            zip_file.extract(f, tempdir)
                
                    total_size = 0
                    for dirpath, dirnames, filenames in os.walk(start_path):
                        for f in filenames:
                            fp = os.path.join(dirpath, f)
                            total_size += os.path.getsize(fp)
                    
                    info_plist = os.path.join(start_path, 'Contents/Info.plist')

                    if os.path.exists(info_plist):
                        plist = plistlib.readPlist(info_plist)
                        
                        if not self.version and 'CFBundleVersion' in plist:
                            self.version = plist.get('CFBundleVersion')
                            update_fields.append('version')

                        
                        if not self.short_version and 'CFBundleShortVersionString' in plist:
                            self.short_version = plist.get('CFBundleShortVersionString')     
                            update_fields.append('short_version')

                        if not self.minimum_system_version and 'LSMinimumSystemVersion' in plist:
                            self.minimum_system_version = plist.get('LSMinimumSystemVersion')
                            update_fields.append('minimum_system_version')

                    shutil.rmtree(tempdir)      
                    self.length = total_size
                    update_fields.append('length')

            
            print("updating version signing")
            super(Version, self).save(update_fields=update_fields)
            

class SystemProfileReport(models.Model):
    """A system profile report"""
    
    ip_address = models.IPAddressField()
    added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'SystemProfileReport'
    
class SystemProfileReportRecord(models.Model):
    """A key/value pair for a system profile report"""
    
    report = models.ForeignKey(SystemProfileReport)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=80)
    
    def __unicode__(self):
        return u'%s: %s' % (self.key, self.value)


def get_file_attr(sender):
    if sender == Version:
        attr = 'update' 
    elif sender == PrivateKey:
        attr = 'private_key'
    else:
        return None
    
    return attr

@receiver(models.signals.post_delete)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    attr = get_file_attr(sender)
    if attr:
        return delete_file_on_delete(sender,instance,attr)


@receiver(models.signals.pre_save)
def auto_delete_file_on_change(sender, instance, **kwargs):
    attr = get_file_attr(sender)
    if attr:
        return delete_file_on_change(sender,instance,attr)
    



