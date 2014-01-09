import os
import datetime
from django.utils import timezone
from django.db import models
from django.dispatch import receiver

class Option(models.Model):
    option = models.CharField(max_length=200,blank=True,unique=True)
    
    def __unicode__(self):
         return self.option 
                        
class Printer(models.Model):   
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200,blank=True)
    
    host = models.CharField(max_length=200)
    protocol = models.CharField(max_length=200)
    
    location = models.CharField(max_length=200,blank=True)
    
    model = models.CharField(max_length=200,blank=True)
    ppd_file = models.FileField(upload_to='ppds/',blank=True)
    option = models.ManyToManyField(Option,blank=True)
    
    def __unicode__(self):
            return self.name
            return self.description
            return self.host
            return self.protocol
            return self.location
            return self.model
            

class PrinterList(models.Model):
    name = models.CharField(max_length=200)
    printer = models.ManyToManyField(Printer,blank=True)
    public = models.BooleanField(default=True);
    def __unicode__(self):
        return self.name


@receiver(models.signals.post_delete, sender=Printer)
def auto_delete_file_on_delete(sender, instance, **kwargs):
   if instance.ppd_file:
        if os.path.isfile(instance.ppd_file.path):
            os.remove(instance.ppd_file.path)

@receiver(models.signals.pre_save, sender=Printer)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = Printer.objects.get(pk=instance.pk).ppd_file
        if not old_file:
            return False
    except Printer.DoesNotExist:
        return False

    new_file = instance.ppd_file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
