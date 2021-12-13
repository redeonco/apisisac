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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

api_info = openapi.Info(
    title="Rede Onco - API",
    default_version='v1',
    description="Documentação da API de integração para o SISAC Oncoradium",
    terms_of_service="",
    contact=openapi.Contact(email="ti@oncoradium.com.br"),
    license=openapi.License(name="BSD License")
)

schema_view = get_schema_view(
    openapi.Info(
        title="Rede Onco - API",
        default_version='v1',
        description="Documentação da API de integração para o SISAC Oncoradium",
        terms_of_service="",
        contact=openapi.Contact(email="ti@oncoradium.com.br"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'api/pacientes', CadPacienteSerializerViewSet)
router.register(r'api/entrada', ApiEntradaSerializerViewSet,
                basename='ApiEntrada')
router.register(r'api/consulta', ApiConsultaSerializerViewSet,
                basename='ApiConsulta')
router.register(r'api/enfevoluc', ApiEnfEvoluCSerializerViewSet,
                basename='ApiEnfevoluc')
router.register(r'api/entradaradio',
                ApiEntradaRadioSerializerViewSet, basename='ApiEntradaradio')
router.register(r'api/planejfisicoc',
                ApiPlanejfisicocSerializerViewSet, basename='ApiPlanejfisicoc')
router.register(r'api/prescreve', ApiPrescreveSerializerViewSet,
                basename='ApiPrescreve')
router.register(r'api/prescreveqt',
                ApiPrescreveqtSerializerViewSet, basename='ApiPrescreveqt')
router.register(r'api/radioterapia',
                ApiRadioterapiaSerializerViewSet, basename='ApiRadioterapia')
router.register(r'api/aplicmmprescqt',
                ApiAplicMM_PrescQTSerializerViewSet, basename='ApiAplicMM_PrescQT')
router.register(r'api/aplicmmpresceletiva',
                ApiAplicMM_PrescEletivaSerializerViewSet, basename='ApiAplicMM_PrescEletiva')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^api/docs/$', schema_view.with_ui('swagger',
        cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc',
        cache_timeout=0), name='schema-redoc'),
]
