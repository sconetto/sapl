from django.views.generic import FormView

from sapl.crud.base import Crud

from .forms import PesquisaLexmlForm
from .models import LexmlProvedor, LexmlPublicador

LexmlProvedorCrud = Crud.build(LexmlProvedor, 'lexml_provedor')
LexmlPublicadorCrud = Crud.build(LexmlPublicador, 'lexml_publicador')


class LexmlPesquisarView(FormView):
    template_name = 'lexml/resultado_pesquisa.html'
    form_class = PesquisaLexmlForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = self.form_class
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = PesquisaLexmlForm(request.POST)

        url = 'http://www.lexml.gov.br/busca/search?keyword='
        url += form.data['conteudo']

        context['url'] = url
        return self.render_to_response(context)
