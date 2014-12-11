'''Models'''

import os
import datetime
from django.utils import timezone
from django.db import models
from django.dispatch import receiver
from django.conf import settings
from printerinstaller.utils import get_dsa_signature, \
                                   delete_file_on_change, \
                                   delete_file_on_delete

class Option(models.Model):
    option = models.CharField(max_length=200, blank=True, unique=True)
    
    def __unicode__(self):
        return self.option 
                        
class Printer(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True)
    host = models.CharField(max_length=200)
    protocol = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    model = models.CharField(max_length=200, blank=True)
    ppd_file = models.FileField(upload_to='ppds/', blank=True)
    option = models.ManyToManyField(Option, blank=True)
    
    def __unicode__(self):
        return self.name
        return self.description
        return self.host
        return self.protocol
        return self.location
        return self.model

            

class PrinterList(models.Model):
    name = models.CharField(max_length=200)
    printer = models.ManyToManyField(Printer, blank=True)
    public = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name


@receiver(models.signals.post_delete, sender=Printer)
def auto_delete_file_on_delete(sender, instance, **kwargs):
   return delete_file_on_delete(instance,'ppd_file')

@receiver(models.signals.pre_save, sender=Printer)
def auto_delete_file_on_change(sender, instance, **kwargs):    
    return delete_file_on_change(sender,instance,'ppd_file')

