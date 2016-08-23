from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth import views
from django.contrib.auth.views import (password_reset,
                                       password_reset_done,
                                       password_reset_confirm,
                                       password_reset_complete)
from django.views.generic.base import TemplateView


from .apps import AppConfig
from .forms import LoginForm, RecuperarSenhaEmailForm, RedefineSenhaForm
from .views import CasaLegislativaCrud, HelpView, SistemaView

app_name = AppConfig.name

recuperar_senha = [
    url(r'^recuperar-senha/$',
        password_reset,
        {'template_name': 'base/recuperar_senha.html',
         'password_reset_form': RecuperarSenhaEmailForm,
         'post_reset_redirect': 'sapl.base:recuperar_senha_finalizado',
         'email_template_name': 'base/recuperar_senha_email.html',
         'from_email': settings.EMAIL_SEND_USER,
         'html_email_template_name': 'base/recuperar_senha_email.html'},
        name='recuperar_senha'),

    url(r'^recuperar-senha/finalizado/$',
        password_reset_done,
        {'template_name': 'base/recuperar_senha_enviado.html'},
        name='recuperar_senha_finalizado'),

    url(r'^recuperar-senha/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        password_reset_confirm,
        {'post_reset_redirect': 'sapl.base:recuperar_senha_completo',
         'template_name': 'base/recuperacao_senha_form.html',
         'set_password_form': RedefineSenhaForm},
        name='recuperar_senha_confirma'),

    url(r'^recuperar-senha/completo/$',
        password_reset_complete,
        {'template_name': 'base/recuperacao_senha_completo.html'},
        name='recuperar_senha_completo'),
]

urlpatterns = [
    url(r'^sistema/', TemplateView.as_view(template_name='sistema.html')),
    url(r'^ajuda/', TemplateView.as_view(template_name='ajuda.html')),
    url(r'^ajuda/(?P<topic>\w+)$', HelpView.as_view(), name='help_topic'),
    url(r'^ajuda/', TemplateView.as_view(template_name='ajuda/index.html'),
        name='help_base'),

    url(r'^casa_legislativa/', include(CasaLegislativaCrud.get_urls())),

    url(r'^login/$', views.login, {
        'template_name': 'base/login.html', 'authentication_form': LoginForm},
        name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/login'}, name='logout')
] + recuperar_senha
