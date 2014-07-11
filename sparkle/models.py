import os
import subprocess
import zipfile
import tempfile
import shutil
import plistlib
from django.db import models
from django.conf import settings
from django.dispatch import receiver

from conf import SPARKLE_PRIVATE_KEY_PATH
from validators import *

def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError("Can only create 1 %s instance" % model.__name__)

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

    def generate_signature(self,path,private_key):
        p1 = subprocess.Popen(['openssl','dgst','-sha1','-binary',path], stdout=subprocess.PIPE)
        if p1.wait() != 0:
            return None

        p2 = subprocess.Popen(['openssl','dgst','-dss1' ,'-sign', private_key], stdin=p1.stdout, stdout=subprocess.PIPE)
        if p1.wait() != 0:
            return None

        p3 = subprocess.Popen(['openssl','enc','-base64'], stdin=p2.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        p2.stdout.close()

        output = p3.communicate()[0].strip()

        if p3.returncode != 0:
            return None
        
        return output

    def __unicode__(self):
        return self.title
        
    def save(self, *args, **kwargs):        
        update = False
        path = os.path.join(settings.MEDIA_ROOT, self.update.path)
        pks = PrivateKey.objects.all()[:1].get()
        if pks:
            SPARKLE_PRIVATE_KEY_PATH=os.path.join(settings.MEDIA_ROOT, '%s' % pks.private_key)

        if SPARKLE_PRIVATE_KEY_PATH or not self.dsa_signature:
            if os.path.exists(SPARKLE_PRIVATE_KEY_PATH):                
                self.dsa_signature = self.generate_signature(path,SPARKLE_PRIVATE_KEY_PATH)
        
        # if there is no length and it is a zip file
        # extract it to a tempdir and calculate the length
        # also parse the plist file for versions
        if not self.length and path.endswith('.zip'):
                zip_file = zipfile.ZipFile(path)
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
                    
                    if not self.short_version and 'CFBundleShortVersionString' in plist:
                        self.short_version = plist.get('CFBundleShortVersionString')     
                    
                    if not self.minimum_system_version and 'LSMinimumSystemVersion' in plist:
                        self.minimum_system_version = plist.get('LSMinimumSystemVersion')
                
                shutil.rmtree(tempdir)      
                self.length = total_size
        
        super(Version, self).save(*args, **kwargs)
            

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


@receiver(models.signals.post_delete)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if sender == Version:
        if instance.update:
            if os.path.isfile(instance.update.path):
                os.remove(instance.update.path)
    elif sender == PrivateKey:
        if instance.private_key:
            if os.path.isfile(instance.private_key.path):
                os.remove(instance.private_key.path)


@receiver(models.signals.pre_save)
def auto_delete_file_on_change(sender, instance, **kwargs):
    
    #make sure to include any modles that recieve signals in here
    if not sender in [Version,PrivateKey]:
        return 

    if sender == Version:
        if not instance.pk:
            return False
        try:
            old_file = Version.objects.get(pk=instance.pk).update
            if not old_file:
                return False
        except Version.DoesNotExist:
            return False

        new_file = instance.update

    elif sender == PrivateKey:
        if not instance.pk:
            return False
        try:
            old_file = PrivateKey.objects.get(pk=instance.pk).private_key
            if not old_file:
                return False
        except Printer.DoesNotExist:
            return False

        new_file = instance.private_key

    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

