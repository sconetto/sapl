import datetime

import pytest
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from model_mommy import mommy

from sapl.materia.models import UnidadeTramitacao
from sapl.protocoloadm.forms import AnularProcoloAdmForm
from sapl.protocoloadm.models import (DocumentoAdministrativo, Protocolo,
                                      StatusTramitacaoAdministrativo,
                                      TipoDocumentoAdministrativo,
                                      TramitacaoAdministrativo)


@pytest.mark.django_db(transaction=False)
def test_create_tramitacao(admin_client):
    tipo_doc = mommy.make(
        TipoDocumentoAdministrativo,
        descricao='Teste Tipo_DocAdm')

    documento_adm = mommy.make(
        DocumentoAdministrativo,
        tipo=tipo_doc)

    unidade_tramitacao_local_1 = mommy.make(
        UnidadeTramitacao, pk=1)

    unidade_tramitacao_destino_1 = mommy.make(
        UnidadeTramitacao, pk=2)

    unidade_tramitacao_destino_2 = mommy.make(
        UnidadeTramitacao, pk=3)

    status = mommy.make(
        StatusTramitacaoAdministrativo)

    tramitacao = mommy.make(
        TramitacaoAdministrativo,
        unidade_tramitacao_local=unidade_tramitacao_local_1,
        unidade_tramitacao_destino=unidade_tramitacao_destino_1,
        status=status,
        documento=documento_adm,
        data_tramitacao=datetime.date(2016, 8, 21))

    response = admin_client.post(
        reverse(
            'sapl.protocoloadm:tramitacaoadministrativo_create',
            kwargs={'pk': documento_adm.pk}),
        {'unidade_tramitacao_local': unidade_tramitacao_destino_2.pk,
         'unidade_tramitacao_destino': unidade_tramitacao_local_1.pk,
         'documento': documento_adm.pk,
         'status': status.pk,
         'data_tramitacao': datetime.date(2016, 8, 21)},
        follow=True)

    msg = force_text(_('A origem da nova tramitação deve ser igual ao '
                       'destino  da última adicionada!'))

    # Verifica se a origem da nova tramitacao é igual ao destino da última
    assert msg in response.context_data[
        'form'].errors['__all__']

    response = admin_client.post(
        reverse(
            'sapl.protocoloadm:tramitacaoadministrativo_create',
            kwargs={'pk': documento_adm.pk}),
        {'unidade_tramitacao_local': unidade_tramitacao_destino_1.pk,
         'unidade_tramitacao_destino': unidade_tramitacao_destino_2.pk,
         'documento': documento_adm.pk,
         'status': status.pk,
         'data_tramitacao': datetime.date(2016, 8, 20)},
        follow=True)

    msg = _('A data da nova tramitação deve ser ' +
            'maior que a data da última tramitação!')

    # Verifica se a data da nova tramitação é maior do que a última
    assert msg in response.context_data[
        'form'].errors['__all__']

    response = admin_client.post(
        reverse(
            'sapl.protocoloadm:tramitacaoadministrativo_create',
            kwargs={'pk': documento_adm.pk}),
        {'unidade_tramitacao_local': unidade_tramitacao_destino_1.pk,
         'unidade_tramitacao_destino': unidade_tramitacao_destino_2.pk,
         'documento': documento_adm.pk,
         'status': status.pk,
         'data_tramitacao': datetime.date.today() + datetime.timedelta(
             days=1)},
        follow=True)

    msg = force_text(_('A data de tramitação deve ser ' +
                       'menor ou igual a data de hoje!'))

    # Verifica se a data da tramitação é menor do que a data de hoje
    assert msg in response.context_data[
        'form'].errors['__all__']

    response = admin_client.post(
        reverse(
            'sapl.protocoloadm:tramitacaoadministrativo_create',
            kwargs={'pk': documento_adm.pk}),
        {'unidade_tramitacao_local': unidade_tramitacao_destino_1.pk,
         'unidade_tramitacao_destino': unidade_tramitacao_destino_2.pk,
         'documento': documento_adm.pk,
         'status': status.pk,
         'data_tramitacao': datetime.date(2016, 8, 21),
         'data_encaminhamento': datetime.date(2016, 8, 20)},
        follow=True)

    msg = force_text(_('A data de encaminhamento deve ser ' +
                       'maior que a data de tramitação!'))

    # Verifica se a data da encaminhamento é menor do que a data de tramitacao
    assert msg in response.context_data[
        'form'].errors['__all__']

    response = admin_client.post(
        reverse(
            'sapl.protocoloadm:tramitacaoadministrativo_create',
            kwargs={'pk': documento_adm.pk}),
        {'unidade_tramitacao_local': unidade_tramitacao_destino_1.pk,
         'unidade_tramitacao_destino': unidade_tramitacao_destino_2.pk,
         'documento': documento_adm.pk,
         'status': status.pk,
         'data_tramitacao': datetime.date(2016, 8, 21),
         'data_fim_prazo': datetime.date(2016, 8, 20)},
        follow=True)

    msg = _('A data fim de prazo deve ser ' +
            'maior que a data de tramitação!')

    # Verifica se a data da do fim do prazo é menor do que a data de tramitacao
    assert msg in response.context_data[
        'form'].errors['__all__']

    response = admin_client.post(
        reverse(
            'sapl.protocoloadm:tramitacaoadministrativo_create',
            kwargs={'pk': documento_adm.pk}),
        {'unidade_tramitacao_local': unidade_tramitacao_destino_1.pk,
         'unidade_tramitacao_destino': unidade_tramitacao_destino_2.pk,
         'documento': documento_adm.pk,
         'status': status.pk,
         'data_tramitacao': datetime.date(2016, 8, 21)},
        follow=True)

    tramitacao = TramitacaoAdministrativo.objects.last()
    # Verifica se a tramitacao que obedece as regras de negócios é criada
    assert tramitacao.data_tramitacao == datetime.date(2016, 8, 21)

@pytest.mark.django_db(transaction=False)
def test_protocoloadm_protocolo_sem_parametros(admin_client):
    response = admin_client.get(reverse('sapl.protocoloadm:protocolo'))
    assert response.status_code == 200

@pytest.mark.django_db(transaction=False)
def test_protocoloadm_protocolo(admin_client):
    url = reverse('sapl.protocoloadm:protocolo') + "?numero=&ano=&data_0=01/02/2013&data_1=01/02/2017&salvar=Pesquisar"
    response = admin_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db(transaction=False)
def test_protocoloadm_protocolo_criar_documento_autenticado(admin_client):
    # Autentica operador_geral
    # To-Do
    # Criar função de setup para criar os usuários padrão do sistema
    # response = client.post('/login/', {'username': 'operador_geral', 'password': 'interlegis'}, follow=True)
    # assert response.status_code == 200
    # assert  not(response.context_data.get('view') == None)

    sigla = 'd_adm'
    descricao = 'documento administrativo'
    mommy.make(TipoDocumentoAdministrativo, sigla=sigla, descricao=descricao)

    pk = '999'
    numero_protocolo = '1'
    ano_protocolo = '2017'

    tipo_documento = TipoDocumentoAdministrativo.objects.first()
    mommy.make(Protocolo, pk = pk, tipo_documento=tipo_documento, numero=numero_protocolo, ano=ano_protocolo, anulado=False)

    url = reverse('sapl.protocoloadm:criar_documento', kwargs={'pk':pk})

    numero_documento = '56'
    assunto = 'assunto9876453 21'
    ano = '2017'
    data = '07/06/2017'

    response = admin_client.post(url,
                            {'tipo': tipo_documento.pk,
                            'numero_protocolo':numero_protocolo,
                            'ano_protocolo': ano_protocolo,
                            'numero': numero_documento,
                            'assunto': assunto,
                            'ano': ano,
                            'data': data}, follow=True)


    assert response.status_code == 200

    documento = DocumentoAdministrativo.objects.get(numero=numero_documento, ano=ano)

    assert documento
    assert documento.numero == int(numero_documento)
    assert documento.ano == int(ano)
    assert documento.numero_protocolo == int(numero_protocolo)
    assert documento.assunto == assunto
    assert documento.protocolo.ano == int(ano_protocolo)
    assert documento.tipo == tipo_documento
    assert documento.data.strftime("%d/%m/%Y") == data
