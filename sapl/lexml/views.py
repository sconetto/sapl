from sapl.crud.base import Crud

from .models import LexmlProvedor, LexmlPublicador

# LexmlProvedorCrud = Crud.build(LexmlProvedor, 'lexml_provedor')
# LexmlPublicadorCrud = Crud.build(LexmlPublicador, 'lexml_publicador')

from django.shortcuts import render


def add_oai_server(request):
    template = 'lexml/add_SAPLOAIServer.html'
    return render(request, template, {})

def edit_oai_server(request):
    template = 'lexml/edit_SAPLOAIServer.html'
    return render(request, template, {})
