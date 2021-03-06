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
        return u'%s' % self.option 
                        
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
        return u'%s' % self.description


            

class PrinterList(models.Model):
    name = models.CharField(max_length=200)
    printer = models.ManyToManyField(Printer, blank=True)
    public = models.BooleanField(default=True)
    
    def __unicode__(self):
        return u'%s' % self.name

class SubscriptionPrinterList(models.Model):
    subnet = models.CharField(max_length=200, blank=False)
    printer = models.ManyToManyField(Printer, blank=True)
    
    def __unicode__(self):
        return self.subnet

    @classmethod
    def instance_for_ip(cls, client_ip):
        '''return the subscription list for a specific ip address'''
        byte_to_bits = lambda b: bin(int(b))[2:].rjust(8, '0')
        ip_to_bits = lambda ip: ''.join([byte_to_bits(b) for b in ip.split('.')])
        client_ip_bits = ip_to_bits(client_ip)

        for _list in cls.objects.all():
            ip_addr, snet = _list.subnet.split('/')

            print "list subnet: " + _list.subnet
            print 'client ip: ' + client_ip
            print 'subnet: ' + ip_addr
            print 'subnet: ' + snet
            
            ip_bits = ip_to_bits(ip_addr)
            if client_ip_bits[:int(snet)] == ip_bits[:int(snet)]:
                return _list



@receiver(models.signals.post_delete, sender=Printer)
def auto_delete_file_on_delete(sender, instance, **kwargs):
   return delete_file_on_delete(instance,'ppd_file')

@receiver(models.signals.pre_save, sender=Printer)
def auto_delete_file_on_change(sender, instance, **kwargs):    
    return delete_file_on_change(sender,instance,'ppd_file')

