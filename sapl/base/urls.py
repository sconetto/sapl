from authtools.views import (PasswordResetView, PasswordResetConfirmView,
                             PasswordResetDoneView, PasswordResetCompleteView)

from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth import views
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView


from .apps import AppConfig
from .forms import LoginForm, RecuperarSenhaEmailForm, RedefineSenhaForm
from .views import (AppConfigCrud, CasaLegislativaCrud, HelpView,
                    RelatorioAtasView, RelatorioHistoricoTramitacaoView,
                    RelatorioMateriasPorAnoAutorTipoView,
                    RelatorioMateriasPorAutorView,
                    RelatorioMateriasTramitacaoView,
                    RelatorioPresencaSessaoView)

app_name = AppConfig.name

recuperar_senha = [
    url(r'^recuperar-senha/$',
        PasswordResetView.as_view(
            template_name='base/recuperar_senha.html',
            form_class=RecuperarSenhaEmailForm,
            success_url=reverse_lazy('sapl.base:recuperar_senha_finalizado'),
            email_template_name='base/recuperar_senha_email.html',
            from_email=settings.EMAIL_SEND_USER,
            html_email_template_name='base/recuperar_senha_email.html'),
        name='recuperar_senha'),

    url(r'^recuperar-senha/finalizado/$',
        PasswordResetDoneView.as_view(
            template_name='base/recuperar_senha_enviado.html'),
        name='recuperar_senha_finalizado'),

    url(r'^recuperar-senha/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        PasswordResetConfirmView.as_view(
            template_name='base/recuperacao_senha_form.html',
            success_url=reverse_lazy('sapl.base:recuperar_senha_completo'),
            form_class=RedefineSenhaForm),
        name='recuperar_senha_confirma'),

    url(r'^recuperar-senha/completo/$',
        PasswordResetCompleteView.as_view(
            template_name='base/recuperacao_senha_completo.html'),
        name='recuperar_senha_completo'),
]

urlpatterns = [
    url(r'^sistema/', TemplateView.as_view(template_name='sistema.html')),
    url(r'^ajuda/', TemplateView.as_view(template_name='ajuda.html')),
    url(r'^relatorios/', TemplateView.as_view(
        template_name='base/relatorios_list.html')),
    url(r'^ajuda/(?P<topic>\w+)$', HelpView.as_view(), name='help_topic'),
    url(r'^ajuda/', TemplateView.as_view(template_name='ajuda/index.html'),
        name='help_base'),
    url(r'^casa-legislativa/', include(CasaLegislativaCrud.get_urls()),
        name="casa_legislativa"),
    url(r'^app-config/', include(AppConfigCrud.get_urls())),

    url(r'^login/$', views.login, {
        'template_name': 'base/login.html', 'authentication_form': LoginForm},
        name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/login'}, name='logout'),

    url(r'^relatorio/materia-por-autor$',
        RelatorioMateriasPorAutorView.as_view(), name='materia_por_autor'),
    url(r'^relatorio/materia-por-ano-autor-tipo$',
        RelatorioMateriasPorAnoAutorTipoView.as_view(),
        name='materia_por_ano_autor_tipo'),
    url(r'^relatorio/materia-por-tramitacao$',
        RelatorioMateriasTramitacaoView.as_view(),
        name='materia_por_tramitacao'),
    url(r'^relatorio/historico-tramitacoes$',
        RelatorioHistoricoTramitacaoView.as_view(),
        name='historico_tramitacoes'),
    url(r'^relatorio/presenca$',
        RelatorioPresencaSessaoView.as_view(),
        name='presenca_sessao'),
    url(r'^relatorio/atas$',
        RelatorioAtasView.as_view(),
        name='atas'),

] + recuperar_senha
