from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from rest_framework import routers
from core.views import (
    EntradaSerializerViewSet, 
    CadPacienteSerializerViewSet, 
    ApiEntradaSerializerViewSet,
    ApiConsultaSerializerViewSet,
    ApiEnfEvoluCSerializerViewSet,
    ApiEntradaRadioSerializerViewSet,
    ApiPlanejfisicocSerializerViewSet,
    ApiPrescreveSerializerViewSet,
    ApiPrescreveqtSerializerViewSet,
    ApiRadioterapiaSerializerViewSet,
)

router = routers.DefaultRouter()
router.register(r'pacientes', CadPacienteSerializerViewSet)
router.register(r'entradas', EntradaSerializerViewSet, basename='Entrada')
router.register(r'api/entrada', ApiEntradaSerializerViewSet, basename='ApiEntrada')
router.register(r'api/consuta', ApiConsultaSerializerViewSet, basename='ApiConsulta')
router.register(r'api/enfevoluc', ApiEnfEvoluCSerializerViewSet, basename='ApiEnfevoluc')
router.register(r'api/entradaradio', ApiEntradaRadioSerializerViewSet, basename='ApiEntradaradio')
router.register(r'api/planejfisicoc', ApiPlanejfisicocSerializerViewSet, basename='ApiPlanejfisicoc')
router.register(r'api/prescreve', ApiPrescreveSerializerViewSet, basename='ApiPrescreve')
router.register(r'api/prescreveqt', ApiPrescreveqtSerializerViewSet, basename='ApiPrescreveqt')
router.register(r'api/radioterapia', ApiRadioterapiaSerializerViewSet, basename='ApiRadioterapia')

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
