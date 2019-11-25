from django.urls import path

from .views import *


urlpatterns = [
    path('rest/caracteristicas_generales/', PDFGeneral, name='PDF'),
    path('rest/caracteristicas_especificas/<int:id>', PDFEspecifico, name='PDF'),
]