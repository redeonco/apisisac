from rest_framework.relations import PrimaryKeyRelatedField
from .models import (
    ApiConsulta,
    ApiRadioterapia, 
    Cadpaciente,
    ApiEntrada,
    ApiEnfevoluc,
    ApiEntradaradio,
    ApiPlanejfisicoc,
    ApiPrescreve,
    ApiPrescreveqt,
    ApiAplicMM_PrescEletiva,
    ApiAplicMM_PrescQT
)
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


class ApiConsultaSerializer(serializers.ModelSerializer):
    # codmovimento = ApiEntradaSerializer(read_only=True)

    class Meta:
        model = ApiConsulta
        fields = [
            'codpaciente',
            'paciente',
            'codmovimento',
            'tipo',
            'codconvenio',
            'convenio',
            'historico',
            'data',
            'nome',
            'obs',
            'numpresc',
            'codmedico',
            'medico'
        ]


class ApiEnfEvoluCSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiEnfevoluc
        fields = [
            'ndoc',
            'codpaciente',
            'paciente',
            'acomod',
            'datahoraf',
            'codmedico',
            'enfermeiro',
            'texto3'
        ]


class ApiPlanejfisicocSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiPlanejfisicoc
        fields = [
            'idplanejfisicoc',
            'codpaciente',
            'paciente',
            'numpresc',
            'energia',
            'dosetotal',
            'dosediaria',
            'naplicacoes',
            'locanatomica',
            'incidencia',
            'ncampo',
            'portal',
            'tpfeixe',
            'fase'
        ]


class ApiPrescreveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiPrescreve
        fields = [
            'codpaciente',
            'codpacref',
            'paciente',
            'codmedico',
            'medico',
            'data',
            'numero',
            'texto',
            'obs',
            'aplicado'
        ]


class ApiEntradaradioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiEntradaradio
        fields = [
            'identradaradio',
            'codmovimento',
            'codpaciente',
            'paciente',
            'numpresc',
            'idplanejfisico',
            'encerrado',
            'observacao',
            'usuario',
            'datahora',
            'nplanejamento',
            'nomecampo',
            'incidencia',
            'ncampo'
        ]


class ApiRadioterapiaSerializer(serializers.ModelSerializer):
    sessoes = ApiEntradaradioSerializer(source='numpresc_set', many=True, read_only=True)
    planejamento = ApiPlanejfisicocSerializer(source='planej_set', many=True, read_only=True)

    class Meta:
        model = ApiRadioterapia
        fields = [
            'numpresc',
            'codpaciente',
            'paciente',
            'codcidp',
            'estadio',
            'finalidade',
            'intencaoradical',
            'intencaopaliativa',
            'tipot',
            'tipon',
            'tipom',
            'naplicacoes',
            'karno',
            'codmed',
            'medico',
            'planejamento',
            'sessoes',
        ]


class ApiAplicMM_PrescQTSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiAplicMM_PrescQT
        fields = [
            'idaplic',
            'ndoc',
            'npresc',
            'codpaciente',
            'paciente',
            'hora',
            'codproduto',
            'brasindice',
            'simpro',
            'descr',
            'un',
            'quant',
            'codenf',
            'enfermeiro',
            'datahora',
            'aplicado',
            'grupop',
            'diaquimioterapia'
        ]


class ApiAplicMM_PrescEletivaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiAplicMM_PrescEletiva
        fields = [
            'idaplic',
            'ndoc',
            'grupop',
            'npresc',
            'codpaciente',
            'paciente',
            'hora',
            'codproduto',
            'brasindice',
            'simpro',
            'descr',
            'un',
            'quant',
            'codenf',
            'enfermeiro',
            'datahora',
            'aplicado'
        ]



class ApiPrescreveqtSerializer(serializers.ModelSerializer):
    gasto = ApiAplicMM_PrescQTSerializer(source='npresc_set', many=True, read_only=True)

    class Meta:
        model = ApiPrescreveqt
        fields = [
            'numero',
            'data',
            'codpaciente',
            'codpacref',
            'paciente',
            'codmedico',
            'medico',
            'texto',
            'obs',
            'texto',
            'peso',
            'supcorp',
            'protocolo',
            'nciclo',
            'aplicado',
            'gasto',
        ]        


class ApiEntradaSerializer(serializers.ModelSerializer):
    consultorio = ApiConsultaSerializer(source='apiconsulta_set', many=True, read_only=True)
    evolucoes = ApiEnfEvoluCSerializer(source='apienfevoluc_set', many=True, read_only=True)
    prescqt = ApiPrescreveqtSerializer(source='prescqt_set', many=True, read_only=True)

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
            'total',
            'consultorio',
            'prescqt',
            'evolucoes',
        ]