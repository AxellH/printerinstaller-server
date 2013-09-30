import datetime
from django.utils import timezone
from django.db import models
   
                        
class Printer(models.Model):   
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200,blank=True)
    location = models.CharField(max_length=200,blank=True)
    model = models.CharField(max_length=200)
    ppd = models.CharField(max_length=200,blank=True)
    url = models.CharField(max_length=200)
    protocol = models.CharField(max_length=200)
    
    def __unicode__(self):
            return self.name
            return self.description
            return self.location
            return self.model
            return self.ppd
            return self.url
            return self.protocol
    
    # def get_fields(self):
    #     return [(field.name, field.value_to_string(self)) for field in Printer._meta.fields]


class Option(models.Model):
    printer = models.ForeignKey(Printer)
    option = models.CharField(max_length=200,blank=False)
    
    def __unicode__(self):
         return self.option

class PrinterList(models.Model):
    name = models.CharField(max_length=200)
    printer = models.ManyToManyField(Printer,blank=True)
    
    def __unicode__(self):
        return self.name
        
    def make_plist(self):
        for i in self.printer.all():
            out = i.name
            