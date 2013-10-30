import datetime
from django.utils import timezone
from django.db import models

class Option(models.Model):
    option = models.CharField(max_length=200,blank=True,unique=True)
    
    def __unicode__(self):
         return self.option 
                        
class Printer(models.Model):   
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200,blank=True)
    
    url = models.CharField(max_length=200)
    protocol = models.CharField(max_length=200)
    
    location = models.CharField(max_length=200,blank=True)
    
    model = models.CharField(max_length=200,blank=True)
    ppd_file = models.FileField(upload_to='ppds/',blank=True)
    option = models.ManyToManyField(Option,blank=True)
    
    def __unicode__(self):
            return self.name
            return self.description
            return self.url
            return self.protocol
            return self.location
            return self.model
            


class PrinterList(models.Model):
    name = models.CharField(max_length=200)
    printer = models.ManyToManyField(Printer,blank=True)
    
    def __unicode__(self):
        return self.name
        