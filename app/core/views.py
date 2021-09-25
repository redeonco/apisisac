from django.shortcuts import render

from .models import (
    ApiConsulta, 
    ApiEnfevoluc,
    ApiPrescreveqt,
    ApiRadioterapia, 
    Cadpaciente, 
    Entrada, 
    ApiEntrada,
    ApiEntradaradio,
    ApiPlanejfisicoc,
    ApiPrescreve,
)
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from .serializers import (
    ApiEnfEvoluCSerializer,
    ApiPrescreveqtSerializer,
    ApiRadioterapiaSerializer, 
    EntradaSerializer, 
    CadpacienteSerializer, 
    ApiEntradaSerializer,
    ApiConsultaSerializer,
    ApiEntradaradioSerializer,
    ApiPlanejfisicocSerializer,
    ApiPrescreveSerializer,
)


class EntradaSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = EntradaSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']

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
    http_method_names = ['get', 'head']


class ApiEntradaSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = ApiEntradaSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']

    def get_queryset(self):
        queryset = ApiEntrada.objects.all().order_by('datahoraent')
        codmovimento = self.request.query_params.get('codmovimento')
        if codmovimento is not None:
            queryset = queryset.filter(codmovimento__exact=codmovimento)
        return queryset


class ApiConsultaSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = ApiConsultaSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']

    def get_queryset(self):
        queryset = ApiConsulta.objects.all().order_by('data')
        codmovimento = self.request.query_params.get('codmovimento')
        if codmovimento is not None:
            queryset = queryset.filter(codmovimento__exact=codmovimento)
        return queryset


class ApiEnfEvoluCSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = ApiEnfEvoluCSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']

    def get_queryset(self):
        queryset = ApiEnfevoluc.objects.all().order_by('datahoraf')
        codmovimento = self.request.query_params.get('codmovimento')
        if codmovimento is not None:
            queryset = queryset.filter(codpaciente__exact=codmovimento)
        return queryset


class ApiEntradaRadioSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = ApiEntradaradioSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']

    def get_queryset(self):
        queryset = ApiEntradaradio.objects.all().order_by('datahora')
        codmovimento = self.request.query_params.get('codpaciente')
        if codmovimento is not None:
            queryset = queryset.filter(codmovimento__exact=codmovimento)
        return queryset


class ApiPlanejfisicocSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = ApiPlanejfisicocSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']

    def get_queryset(self):
        queryset = ApiPlanejfisicoc.objects.all().order_by('numpresc')
        codmovimento = self.request.query_params.get('codpaciente')
        if codmovimento is not None:
            queryset = queryset.filter(codmovimento__exact=codmovimento)
        return queryset


class ApiPrescreveSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = ApiPrescreveSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']

    def get_queryset(self):
        queryset = ApiPrescreve.objects.all().order_by('data')
        codmovimento = self.request.query_params.get('codpaciente')
        if codmovimento is not None:
            queryset = queryset.filter(codmovimento__exact=codmovimento)
        return queryset


class ApiPrescreveqtSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = ApiPrescreveqtSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']

    def get_queryset(self):
        queryset = ApiPrescreveqt.objects.all().order_by('data')
        codmovimento = self.request.query_params.get('codpaciente')
        if codmovimento is not None:
            queryset = queryset.filter(codmovimento__exact=codmovimento)
        return queryset


class ApiRadioterapiaSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = ApiRadioterapiaSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']

    def get_queryset(self):
        queryset = ApiRadioterapia.objects.all().order_by('numpresc')
        codmovimento = self.request.query_params.get('codpaciente')
        if codmovimento is not None:
            queryset = queryset.filter(codmovimento__exact=codmovimento)
        return queryset
