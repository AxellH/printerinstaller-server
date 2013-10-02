import datetime
from django.utils import timezone
from django.db import models

class Option(models.Model):
    option = models.CharField(max_length=200,blank=True)
    
    def __unicode__(self):
         return self.option 
                        
class Printer(models.Model):   
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200,blank=True)
    location = models.CharField(max_length=200,blank=True)
    model = models.CharField(max_length=200)
    ppd = models.CharField(max_length=200,blank=True)
    url = models.CharField(max_length=200)
    protocol = models.CharField(max_length=200)
    option = models.ManyToManyField(Option,blank=True)
    
    def __unicode__(self):
            return self.name
            return self.description
            return self.location
            return self.model
            return self.ppd
            return self.url
            return self.protocol


class PrinterList(models.Model):
    name = models.CharField(max_length=200)
    printer = models.ManyToManyField(Printer,blank=True)
    
    def __unicode__(self):
        return self.name
        