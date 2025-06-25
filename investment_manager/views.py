from django.shortcuts import render
from rest_framework import viewsets

from investment_manager.models import Investment, Owner
from investment_manager.serializers import InvestmentSerializer, OwnerSerializer


class InvestmentViewSet(viewsets.ModelViewSet):
    """
    Habilita o CRUD de Investments
    """
    queryset = Investment.objects.all().order_by('-creation_date','-id')
    serializer_class = InvestmentSerializer

class OwnerViewSet(viewsets.ModelViewSet):
    """
    Habilita o CRUD de Owners
    """
    queryset = Owner.objects.all().order_by('-creation_date', '-id')
    serializer_class = OwnerSerializer
