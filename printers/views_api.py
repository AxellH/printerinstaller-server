from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions

from printers.models import Option, Printer, PrinterList, SubscriptionPrinterList
from printers.serializers import *
from printers.permissions import *


class OptionViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Option.objects.all()
    serializer_class = OptionSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self, **kwargs):
        '''this is docstring'''
        return Option.objects.all()


class PrinterViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer

    filter_fields = ('name', 'location', 'description')
    filter_backends = (filters.DjangoFilterBackend,)

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self, **kwargs):
        '''this is docstring'''
        return Printer.objects.all()


# class PrinterListViewSet(viewsets.ModelViewSet):
#     """
#     This viewset automatically provides `list`, `create`, `retrieve`,
#     `update` and `destroy` actions.
#     """

#     queryset = PrinterList.objects.all()
#     serializer_class = PrinterListSerializer
    
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


#     def perform_create(self, serializer):
#         serializer.save()

#     def get_queryset(self, **kwargs):
#         '''this is docstring'''
#         return PrinterList.objects.all()

# class SubscriptionPrinterListViewSet(viewsets.ModelViewSet):
#     """
#     This viewset automatically provides `list`, `create`, `retrieve`,
#     `update` and `destroy` actions.
#     """

#     queryset = SubscriptionPrinterList.objects.all()
#     serializer_class = PrinterListSerializer
    
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

#     def perform_create(self, serializer):
#         serializer.save()

#     def get_queryset(self, **kwargs):
#         '''this is docstring'''
#         return SubscriptionPrinterList.objects.all()

