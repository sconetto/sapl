from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout

from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from sapl.crispy_layout_mixin import form_actions, to_row
from sapl.settings import MAX_IMAGE_UPLOAD_SIZE
from sapl.utils import ImageThumbnailFileInput

from .models import CasaLegislativa


class CasaLegislativaForm(ModelForm):

    class Meta:

        model = CasaLegislativa
        fields = ['codigo',
                  'nome',
                  'sigla',
                  'endereco',
                  'cep',
                  'municipio',
                  'uf',
                  'telefone',
                  'fax',
                  'logotipo',
                  'endereco_web',
                  'email',
                  'informacao_geral']

        widgets = {
            'uf': forms.Select(attrs={'class': 'selector'}),
            'cep': forms.TextInput(attrs={'class': 'cep'}),
            'telefone': forms.TextInput(attrs={'class': 'telefone'}),
            'fax': forms.TextInput(attrs={'class': 'telefone'}),
            'logotipo': ImageThumbnailFileInput,
            'informacao_geral': forms.Textarea(
                attrs={'id': 'texto-rico'})
        }

    def clean_logotipo(self):
        logotipo = self.cleaned_data.get('logotipo', False)
        if logotipo:
            if logotipo.size > MAX_IMAGE_UPLOAD_SIZE:
                raise ValidationError("Imagem muito grande. ( > 2mb )")
        return logotipo


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username", max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(
        label="Password", max_length=30,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 'name': 'password'}))


class RecuperarSenhaEmailForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super(RecuperarSenhaEmailForm, self).__init__(*args, **kwargs)

        row1 = to_row(
            [('email', 12)])

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(_('Insira seu e-mail cadastrado'),
                     row1,
                     form_actions(save_label='Enviar'))
        )

    def clean(self):
        email_existente_usuario = User.objects.filter(
            email=self.data['email'])
        email_existente_user = User.objects.filter(
            email=self.data['email'])

        if not email_existente_usuario and not email_existente_user:
            msg = _('Não existe nenhum usuário cadastrado com este e-mail.')
            raise ValidationError(msg)

        return self.cleaned_data


class RedefineSenhaForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(RedefineSenhaForm, self).__init__(*args, **kwargs)

        row1 = to_row(
            [('new_password1', 6),
             ('new_password2', 6)])

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(_('Insira sua nova senha'),
                     row1,
                     form_actions(save_label='Enviar'))
        )
