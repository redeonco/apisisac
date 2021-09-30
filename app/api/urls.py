from app.core.views import CadPacienteSerializerViewSet2
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from rest_framework import routers
from core.views import (
    CadPacienteSerializerViewSet, 
    ApiEntradaSerializerViewSet,
    ApiConsultaSerializerViewSet,
    ApiEnfEvoluCSerializerViewSet,
    ApiEntradaRadioSerializerViewSet,
    ApiPlanejfisicocSerializerViewSet,
    ApiPrescreveSerializerViewSet,
    ApiPrescreveqtSerializerViewSet,
    ApiRadioterapiaSerializerViewSet,
    ApiAplicMM_PrescQTSerializerViewSet,
    ApiAplicMM_PrescEletivaSerializerViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'api/pacientes', CadPacienteSerializerViewSet)
router.register(r'api/pacientes2', CadPacienteSerializerViewSet2)
router.register(r'api/entrada', ApiEntradaSerializerViewSet, basename='ApiEntrada')
router.register(r'api/consulta', ApiConsultaSerializerViewSet, basename='ApiConsulta')
router.register(r'api/enfevoluc', ApiEnfEvoluCSerializerViewSet, basename='ApiEnfevoluc')
router.register(r'api/entradaradio', ApiEntradaRadioSerializerViewSet, basename='ApiEntradaradio')
router.register(r'api/planejfisicoc', ApiPlanejfisicocSerializerViewSet, basename='ApiPlanejfisicoc')
router.register(r'api/prescreve', ApiPrescreveSerializerViewSet, basename='ApiPrescreve')
router.register(r'api/prescreveqt', ApiPrescreveqtSerializerViewSet, basename='ApiPrescreveqt')
router.register(r'api/radioterapia', ApiRadioterapiaSerializerViewSet, basename='ApiRadioterapia')
router.register(r'api/aplicmmprescqt', ApiAplicMM_PrescQTSerializerViewSet, basename='ApiAplicMM_PrescQT')
router.register(r'api/aplicmmpresceletiva', ApiAplicMM_PrescEletivaSerializerViewSet, basename='ApiAplicMM_PrescEletiva')

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
