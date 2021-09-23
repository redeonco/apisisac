from django.shortcuts import render

from .models import Cadpaciente, Entrada, ApiEntrada
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from .serializers import EntradaSerializer, CadpacienteSerializer, ApiEntradaSerializer


class EntradaSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = EntradaSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Entrada.objects.all().order_by('datahoraent')
        codmovimento = self.request.query_params.get('codmovimento')
        if codmovimento is not None:
            queryset = queryset.filter(codmovimento__exact=codmovimento)
        return queryset


class CadPacienteSerializerViewSet(viewsets.ModelViewSet):
    queryset = Cadpaciente.objects.all().order_by('codpaciente')
    serializer_class = CadpacienteSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]


class ApiEntradaSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = ApiEntradaSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = ApiEntrada.objects.all().order_by('datahoraent')
        codmovimento = self.request.query_params.get('codmovimento')
        if codmovimento is not None:
            queryset = queryset.filter(codmovimento__exact=codmovimento)
        return queryset
