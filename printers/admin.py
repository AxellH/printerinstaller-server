from django.contrib import admin
from printers.models import *

class OptionInline(admin.StackedInline):
    model = Option
    extra = 1
    
class PrinterAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    

admin.site.register(Printer,PrinterAdmin)
admin.site.register(PrinterList)
