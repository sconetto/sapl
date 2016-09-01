from datetime import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.views.generic import FormView, ListView
from django.utils.translation import ugettext_lazy as _

from django_filters.views import FilterView

from sapl.compilacao.views import IntegracaoTaView
from sapl.crud.base import (Crud, CrudBaseMixin, CrudCreateView,
                            CrudDeleteView, CrudUpdateView, make_pagination)
from sapl.utils import permissoes_norma

from .forms import NormaJuridicaForm, NormaJuridicaFilterSet
from .models import (AssuntoNorma, LegislacaoCitada, NormaJuridica,
                     TipoNormaJuridica)

LegislacaoCitadaCrud = Crud.build(LegislacaoCitada, '')


class AssuntoNormaCrud(Crud):
    model = AssuntoNorma
    help_path = 'assunto_norma_juridica'

    class BaseMixin(PermissionRequiredMixin, CrudBaseMixin):
        permission_required = permissoes_norma()
        list_field_names = ['assunto', 'descricao']


class TipoNormaCrud(Crud):
    model = TipoNormaJuridica
    help_path = 'tipo_norma_juridica'

    class BaseMixin(PermissionRequiredMixin, CrudBaseMixin):
        permission_required = permissoes_norma()
        list_field_names = ['equivalente_lexml', 'sigla', 'descricao']


class NormaCrud(Crud):
    model = NormaJuridica
    help_path = 'norma_juridica'

    class UpdateView(PermissionRequiredMixin, CrudUpdateView):
        form_class = NormaJuridicaForm
        permission_required = permissoes_norma()

        @property
        def layout_key(self):
            return 'NormaJuridicaCreate'

        def get_initial(self):
            norma = NormaJuridica.objects.get(id=self.kwargs['pk'])
            if norma.materia:
                self.initial['tipo_materia'] = norma.materia.tipo
                self.initial['ano_materia'] = norma.materia.ano
                self.initial['numero_materia'] = norma.materia.numero
            return self.initial.copy()

    class CreateView(PermissionRequiredMixin, CrudCreateView):
        form_class = NormaJuridicaForm
        permission_required = permissoes_norma()

        @property
        def layout_key(self):
            return 'NormaJuridicaCreate'

    class DeleteView(PermissionRequiredMixin, CrudDeleteView):
        permission_required = permissoes_norma()

    class BaseMixin(CrudBaseMixin):
        list_field_names = ['tipo', 'numero', 'ano', 'ementa']


class PesquisaNormaJuridicaView(FilterView):
    model = NormaJuridica
    filterset_class = NormaJuridicaFilterSet
    paginate_by = 10

    def get_filterset_kwargs(self, filterset_class):
        super(PesquisaNormaJuridicaView,
              self).get_filterset_kwargs(filterset_class)

        kwargs = {'data': self.request.GET or None}

        qs = self.get_queryset()

        # if vigencia
        # TODO

        kwargs.update({
            'queryset': qs,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(PesquisaNormaJuridicaView,
                        self).get_context_data(**kwargs)

        context['title'] = _('Pesquisar Norma Jurídica')

        paginator = context['paginator']
        page_obj = context['page_obj']
        context['page_range'] = make_pagination(
            page_obj.number, paginator.num_pages)

        self.filterset.form.fields['o'].label = _('Ordenação')

        qr = self.request.GET.copy()
        if 'page' in qr:
            del qr['page']
        context['filter_url'] = ('&' + qr.urlencode()) if len(qr) > 0 else ''

        return context


class NormaTaView(IntegracaoTaView):
    model = NormaJuridica
    model_type_foreignkey = TipoNormaJuridica
