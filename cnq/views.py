 # -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from templates import *
from .models import *
from weasyprint import HTML
import tempfile
from django.template.loader import render_to_string
from itertools import groupby


# Create your views here.

def PDFGeneral(request):

        #Modelos
        escuelas = RawSchool.objects.all()
        concurso = Contest.objects.all()
        cantidad_grupos = Group.objects.count()
        proyecto = RawProject.objects.all()
        
        
        datos = {
            'tipo_escuela': escuelas,
            'datos_concurso': concurso,
            'cantidad_grupos': cantidad_grupos,
            'nombre_proyecto': proyecto,
            'difusion': proyecto,
            'diffusion_count': {}
        }
        print(RawProject.DIFFUSION)
                
        tipo = []
        for proyectos in proyecto:
            tipo.append(proyectos.get_diffusion_display())
            
        for k in RawProject.DIFFUSION:
            datos['diffusion_count'][k[1]] = 0

        for i in tipo:
            datos['diffusion_count'][i] = tipo.count(i)        
        print(datos)

        #Response
        rendered_html = render_to_string('caracteristicas_generales.html', datos)
        response = HttpResponse(content_type='application/pdf')
        pdf = HTML(string=rendered_html).write_pdf(response, presentational_hints=True)
        return response
    
def PDFEspecifico(request, id):

        #Modelos
        contact = RawContact.objects.get(group=id)
        escuelas = RawSchool.objects.get(group=id)
        proyecto = RawProject.objects.get(group=id)
        participant = RawParticipant.objects.filter(group=id)

        print(participant)
        datos = {
            'contact': contact,
            'school': escuelas,
            'project': proyecto,
            'participant': participant,
            'category': proyecto.category.all()
            
        }

        #Response
        rendered_html = render_to_string('caracteristicas_especificas.html', datos)
        response = HttpResponse(content_type='application/pdf')
        pdf = HTML(string=rendered_html).write_pdf(response, presentational_hints=True)
        return response