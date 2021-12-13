from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render

from .models import (
    ApiAplicMM_PrescEletiva,
    ApiAplicMM_PrescQT,
    ApiConsulta,
    ApiEnfevoluc,
    ApiPrescreveqt,
    ApiRadioterapia,
    Cadpaciente,
    ApiEntrada,
    ApiEntradaradio,
    ApiPlanejfisicoc,
    ApiPrescreve,
)
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from .serializers import (
    ApiAplicMM_PrescEletivaSerializer,
    ApiAplicMM_PrescQTSerializer,
    ApiEnfEvoluCSerializer,
    ApiPrescreveqtSerializer,
    ApiRadioterapiaSerializer,
    CadpacienteSerializer,
    ApiEntradaSerializer,
    ApiConsultaSerializer,
    ApiEntradaradioSerializer,
    ApiPlanejfisicocSerializer,
    ApiPrescreveSerializer,
)
from drf_yasg import openapi


class CadPacienteSerializerViewSet(viewsets.ModelViewSet):
    """
    Endpoint Cadastro de Pacientes

    Retorna lista com cadastro de todos os pacientes.
    """
    queryset = Cadpaciente.objects.all().order_by('codpaciente')
    serializer_class = CadpacienteSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']


class ApiEntradaSerializerViewSet(viewsets.ModelViewSet):
    """
    Endpoint Entrada

    Retorna lista com todos as entradas realizadas. Cada entrada é representada por um código de movimento.
    Por exemplo: 000007.10
    Onde '000007' é o número do prontuário do paciente, e '.10' indica que esta entrada é o atendimento nº 10 realizado.

    Os 3 últimos campos deste endpoint estão aninhados, respectivamente desta forma:
    * Consultorio: -> Relaciona-se com o Endpoint Consulta
    * Prescqt: -> Relaciona-se com o Endpoint Prescreveqt
    * Evolucoes: -> Relaciona-se com o Endpoint EnfEvoluC

    Filtros de datas estão disponíveis, usando como chave o atributo "datahoraent".
    Os operadores do filtro são:
    * __gte: Greater Than/Equal - Maior Que ou Igual A;
    * __lte: Less Than/Equal - Menor Que ou Igual A;
    * __gt: Greater Than - Maior Que;
    * __lt: Less Than - Menor Que.

    O formato de data aceito é: AAAA-MM-DD HH:mm 

    O exemplo abaixo retornará todas entradas realizadas no período de 20/09/2021 00:00 a 20/09/2021 23:59
    * datahoraent__gte: 2021-09-20 00:00
    * datahoraent__lte: 2021-09-20 23:59
    """
    serializer_class = ApiEntradaSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']
    filterset_fields = {'datahoraent': ['gte', 'lte', 'exact', 'gt', 'lt']}

    def get_queryset(self):
        queryset = ApiEntrada.objects.all().order_by('datahoraent')
        codmovimento = self.request.query_params.get('codmovimento')
        if codmovimento is not None:
            queryset = queryset.filter(codmovimento__exact=codmovimento)

        return queryset


class ApiConsultaSerializerViewSet(viewsets.ModelViewSet):
    """
    Endpoint Consulta

    Retorna lista com todos os dados clínicos gerados pelo médico dentro do consultório.
    Cada registro está amarrado a um código de movimento.
    O atributo "Histórico" é uma string no formato RTF.
    Para exibir, o sistema que irá consumir esta API deverá receber o conteúdo do atributo e salvar em um arquivo .RTF

    Filtros de datas estão disponíveis, usando como chave o atributo "data".
    Os operadores do filtro são:
    * __gte: Greater Than/Equal - Maior Que ou Igual A;
    * __lte: Less Than/Equal - Menor Que ou Igual A;
    * __gt: Greater Than - Maior Que;
    * __lt: Less Than - Menor Que.

    O formato de data aceito é: AAAA-MM-DD HH:mm

    O exemplo abaixo retornará todas as consultas realizadas no período de 20/09/2021 00:00 a 20/09/2021 23:59
    * data__gte: 2021-09-20 00:00
    * data__lte: 2021-09-20 23:59
    """
    serializer_class = ApiConsultaSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']
    filterset_fields = {'data': ['gte', 'lte', 'exact', 'gt', 'lt']}

    def get_queryset(self):
        queryset = ApiConsulta.objects.all().order_by('data')
        query = self.request.query_params.get('codmovimento')
        if query is not None:
            queryset = queryset.filter(codmovimento__exact=query)
        return queryset


class ApiEnfEvoluCSerializerViewSet(viewsets.ModelViewSet):
    """
    Endpoint Evolução de Enfermagem

    Retorna lista com todas as evoluções de enfermagem realizadas no prontuário eletrônico.
    Cada registro está amarrado a um código de movimento.
    O atributo "Texto3" é uma string no formato RTF.
    Para exibir, o sistema que irá consumir esta API deverá receber o conteúdo do atributo e salvar em um arquivo .RTF

    Filtros de datas estão disponíveis, usando como chave o atributo "datahoraf".
    Os operadores do filtro são:
    * __gte: Greater Than/Equal - Maior Que ou Igual A;
    * __lte: Less Than/Equal - Menor Que ou Igual A;
    * __gt: Greater Than - Maior Que;
    * __lt: Less Than - Menor Que.

    O formato de data aceito é: AAAA-MM-DD HH:mm

    O exemplo abaixo retornará todas as evoluções de enfermagem realizadas no período de 20/09/2021 00:00 a 20/09/2021 23:59
    * datahoraf__gte: 2021-09-20 00:00
    * datahoraf__lte: 2021-09-20 23:59
    """
    serializer_class = ApiEnfEvoluCSerializer
    #authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']
    filterset_fields = {'datahoraf': ['gte', 'lte', 'exact', 'gt', 'lt']}

    def get_queryset(self):
        queryset = ApiEnfevoluc.objects.all().order_by('datahoraf')
        codmovimento = self.request.query_params.get('codmovimento')
        if codmovimento is not None:
            queryset = queryset.filter(codpaciente__exact=codmovimento)
        return queryset


class ApiEntradaRadioSerializerViewSet(viewsets.ModelViewSet):
    """
    Endpoint Entrada Radioterapia

    Retorna lista com todas as sessões de radioterapia realizadas.
    Cada sessão está amarrada a um código de movimento do endpoint Entrada.
    O atributo "numpresc" faz referência à prescrição de radioterapia do paciente.
    Assim como "idplanejfisico" faz referência ao planejamento físico.

    Filtros de datas estão disponíveis, usando como chave o atributo "datahora".
    Os operadores do filtro são:
    * __gte: Greater Than/Equal - Maior Que ou Igual A;
    * __lte: Less Than/Equal - Menor Que ou Igual A;
    * __gt: Greater Than - Maior Que;
    * __lt: Less Than - Menor Que.

    O formato de data aceito é: AAAA-MM-DD HH:mm

    O exemplo abaixo retornará todas as sessões de radioterapia realizadas no período de 20/09/2021 00:00 a 20/09/2021 23:59
    * datahora__gte: 2021-09-20 00:00
    * datahora__lte: 2021-09-20 23:59
    """
    serializer_class = ApiEntradaradioSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']
    filterset_fields = {'datahora': ['gte', 'lte', 'exact', 'gt', 'lt']}

    def get_queryset(self):
        queryset = ApiEntradaradio.objects.all().order_by('datahora')
        codmovimento = self.request.query_params.get('codpaciente')
        if codmovimento is not None:
            queryset = queryset.filter(codmovimento__exact=codmovimento)
        return queryset


class ApiPlanejfisicocSerializerViewSet(viewsets.ModelViewSet):
    """
    Endpoint Planejamento Físico

    Retorna lista com todos os planejamentos de radioterapia realizados.
    Cada planejamento está amarrado a uma prescrição de radioterapia.

    Filtros de datas estão disponíveis, usando como chave o atributo "datasist".
    Os operadores do filtro são:
    * __gte: Greater Than/Equal - Maior Que ou Igual A;
    * __lte: Less Than/Equal - Menor Que ou Igual A;
    * __gt: Greater Than - Maior Que;
    * __lt: Less Than - Menor Que.

    O formato de data aceito é: AAAA-MM-DD HH:mm

    O exemplo abaixo retornará todos os planejamentos de radioterapia realizados no período de 20/09/2021 00:00 a 20/09/2021 23:59
    * datasist__gte: 2021-09-20 00:00
    * datasist__lte: 2021-09-20 23:59
    """
    serializer_class = ApiPlanejfisicocSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']
    filterset_fields = {'datasist': ['gte', 'lte', 'exact', 'gt', 'lt']}

    def get_queryset(self):
        queryset = ApiPlanejfisicoc.objects.all().order_by('numpresc')
        codmovimento = self.request.query_params.get('codpaciente')
        if codmovimento is not None:
            queryset = queryset.filter(codmovimento__exact=codmovimento)
        return queryset


class ApiPrescreveSerializerViewSet(viewsets.ModelViewSet):
    """
    Endpoint Prescrições Eletivas

    Retorna lista com todas as prescrições eletivas realizadas, tanto pelo médico, quanto pelo enfermeiro.
    Cada prescrição está amarrada a um código de movimento do endpoint Entrada.
    O atributo "Texto" é uma string no formato RTF.
    Para exibir, o sistema que irá consumir esta API deverá receber o conteúdo do atributo e salvar em um arquivo .RTF

    Filtros de datas estão disponíveis, usando como chave o atributo "data".
    Os operadores do filtro são:
    * __gte: Greater Than/Equal - Maior Que ou Igual A;
    * __lte: Less Than/Equal - Menor Que ou Igual A;
    * __gt: Greater Than - Maior Que;
    * __lt: Less Than - Menor Que.

    O formato de data aceito é: AAAA-MM-DD HH:mm

    O exemplo abaixo retornará todas as prescrições eletivas realizadas no período de 20/09/2021 00:00 a 20/09/2021 23:59
    * data__gte: 2021-09-20 00:00
    * data__lte: 2021-09-20 23:59
    """
    serializer_class = ApiPrescreveSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']
    filterset_fields = {'data': ['gte', 'lte', 'exact', 'gt', 'lt']}

    def get_queryset(self):
        queryset = ApiPrescreve.objects.all().order_by('data')
        codmovimento = self.request.query_params.get('codpaciente')
        if codmovimento is not None:
            queryset = queryset.filter(codmovimento__exact=codmovimento)
        return queryset


class ApiPrescreveqtSerializerViewSet(viewsets.ModelViewSet):
    """
    Endpoint PrescreveQT

    Retorna lista com todas as prescrições de quimioterapia realizadas.
    A prescrição pode, ou não, estar amarrada a um código de movimento, mas sempre estará amarrada ao prontuário de um paciente.

    Filtros de datas estão disponíveis, usando como chave o atributo "data".
    Os operadores do filtro são:
    * __gte: Greater Than/Equal - Maior Que ou Igual A;
    * __lte: Less Than/Equal - Menor Que ou Igual A;
    * __gt: Greater Than - Maior Que;
    * __lt: Less Than - Menor Que.

    O formato de data aceito é: AAAA-MM-DD HH:mm

    O exemplo abaixo retornará todas as prescrições de quimioterapia realizadas no período de 20/09/2021 00:00 a 20/09/2021 23:59
    * data__gte: 2021-09-20 00:00
    * data__lte: 2021-09-20 23:59
    """
    serializer_class = ApiPrescreveqtSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']
    filterset_fields = {'data': ['gte', 'lte', 'exact', 'gt', 'lt']}

    def get_queryset(self):
        queryset = ApiPrescreveqt.objects.all().order_by('data')
        numpresc = self.request.query_params.get('numpresc')
        if numpresc is not None:
            queryset = queryset.filter(numero__exact=numpresc)
        return queryset


class ApiRadioterapiaSerializerViewSet(viewsets.ModelViewSet):
    """
    Endpoint Radioterapia

    Retorna lista de todas as prescrições de radioterapia realizadas.
    Cada prescrição está amarrada a um prontuário de paciente.    

    Os 2 últimos campos deste endpoint estão aninhados, respectivamente desta forma:
    * Planejamento: -> Relaciona-se com o Endpoint PlanejFisicoC
    * Sessoes: -> Relaciona-se com o Endpoint EntradaRadio

    Filtros de datas estão disponíveis, usando como chave o atributo "datasist".
    Os operadores do filtro são:
    * __gte: Greater Than/Equal - Maior Que ou Igual A;
    * __lte: Less Than/Equal - Menor Que ou Igual A;
    * __gt: Greater Than - Maior Que;
    * __lt: Less Than - Menor Que.

    O formato de data aceito é: AAAA-MM-DD HH:mm

    O exemplo abaixo retornará todas as prescrições de radioterapia realizadas no período de 20/09/2021 00:00 a 20/09/2021 23:59
    * datasist__gte: 2021-09-20 00:00
    * datasist__lte: 2021-09-20 23:59
    """
    serializer_class = ApiRadioterapiaSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']
    filterset_fields = {'datasist': ['gte', 'lte', 'exact', 'gt', 'lt']}

    def get_queryset(self):
        queryset = ApiRadioterapia.objects.all().order_by('numpresc')
        numpresc = self.request.query_params.get('numpresc')
        if numpresc is not None:
            queryset = queryset.filter(numpresc__exact=numpresc)
        return queryset


class ApiAplicMM_PrescQTSerializerViewSet(viewsets.ModelViewSet):
    """
    Endpoint Aplicação Medicamentosa - Prescrição QT

    Retorna lista de todas as aplicações medicamentosas para prescrições de quimioterapia.
    Cada aplicação está amarrada a uma prescrição de quimioterapia.

    Filtros de datas estão disponíveis, usando como chave o atributo "datahora".
    Os operadores do filtro são:
    * __gte: Greater Than/Equal - Maior Que ou Igual A;
    * __lte: Less Than/Equal - Menor Que ou Igual A;
    * __gt: Greater Than - Maior Que;
    * __lt: Less Than - Menor Que.

    O formato de data aceito é: AAAA-MM-DD HH:mm

    O exemplo abaixo retornará todas as aplicações medicamentosas de prescrição de quimioterapia realizadas no período de 20/09/2021 00:00 a 20/09/2021 23:59
    * datahora__gte: 2021-09-20 00:00
    * datahora__lte: 2021-09-20 23:59
    """
    serializer_class = ApiAplicMM_PrescQTSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']
    filterset_fields = {'datahora': ['gte', 'lte', 'exact', 'gt', 'lt']}

    def get_queryset(self):
        queryset = ApiAplicMM_PrescQT.objects.all().order_by('npresc')
        codmovimento = self.request.query_params.get('codpaciente')
        if codmovimento is not None:
            queryset = queryset.filter(codpaciente__exact=codmovimento)
        return queryset


class ApiAplicMM_PrescEletivaSerializerViewSet(viewsets.ModelViewSet):
    """
    Endpoint Aplicação Medicamentosa - Prescrições Eletivas

    Retorna lista de todas as aplicações medicamentosas para prescrições eletivas.
    Cada aplicação está amarrada a uma prescrição eletiva.

    Filtros de datas estão disponíveis, usando como chave o atributo "datahora".
    Os operadores do filtro são:
    * __gte: Greater Than/Equal - Maior Que ou Igual A;
    * __lte: Less Than/Equal - Menor Que ou Igual A;
    * __gt: Greater Than - Maior Que;
    * __lt: Less Than - Menor Que.

    O formato de data aceito é: AAAA-MM-DD HH:mm

    O exemplo abaixo retornará todas as aplicações medicamentosas de prescrição eletiva realizadas no período de 20/09/2021 00:00 a 20/09/2021 23:59
    * datahora__gte: 2021-09-20 00:00
    * datahora__lte: 2021-09-20 23:59
    """
    serializer_class = ApiAplicMM_PrescEletivaSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']
    filterset_fields = {'datahora': ['gte', 'lte', 'exact', 'gt', 'lt']}

    def get_queryset(self):
        queryset = ApiAplicMM_PrescEletiva.objects.all().order_by('npresc')
        codmovimento = self.request.query_params.get('codpaciente')
        if codmovimento is not None:
            queryset = queryset.filter(codpaciente__exact=codmovimento)
        return queryset
