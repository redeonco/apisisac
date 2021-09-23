from .models import Cadpaciente, Entrada, ApiEntrada
from rest_framework import serializers


class CadpacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cadpaciente
        fields = [
            'codpaciente',
            'paciente',
            'sexo',
            'datanasc',
            'idade',
            'rg',
            'cpf',
        ]


class EntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrada
        fields = [
            'codmovimento',
            'codpaciente',
            'codconvenio',
            'matricula',
            'tipo',
            'datahoraent',
            'hist',
            'codmedico',
            'total',
            'fechado',
            'codamb',
            'codcid',
            'usuario',
        ]


class ApiEntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiEntrada
        fields = [
            'codpaciente',
            'paciente',
            'codmovimento',
            'matricula',
            'tipoatd',
            'situacao',
            'datahoraent',
            'datahorasai',
            'codconvenio',
            'convenio',
            'plano',
            'codmedico',
            'medico',
            'codamb',
            'procedimento',
            'hist',
            'total'
        ]
