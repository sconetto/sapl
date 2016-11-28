from django.conf.urls import include, url

from sapl.sessao.views import (AdicionarVariasMateriasExpediente,
                               AdicionarVariasMateriasOrdemDia, BancadaCrud,
                               BlocoCrud, CargoBancadaCrud,
                               ExpedienteMateriaCrud, ExpedienteView,
                               MateriaOrdemDiaCrud, MesaView, OradorCrud,
                               OradorExpedienteCrud, PainelView,
                               PautaExpedienteDetail, PautaOrdemDetail,
                               PautaSessaoDetailView, PautaSessaoListView,
                               PesquisarPautaSessaoView,
                               PesquisarSessaoPlenariaView,
                               PresencaOrdemDiaView, PresencaView, ResumoView,
                               SessaoCrud, TipoExpedienteCrud,
                               TipoResultadoVotacaoCrud, TipoSessaoCrud,
                               VotacaoEditView, VotacaoExpedienteEditView,
                               VotacaoExpedienteView, VotacaoNominalEditView,
                               VotacaoNominalExpedienteEditView,
                               VotacaoNominalExpedienteView,
                               VotacaoNominalView, VotacaoView,
                               abrir_votacao_expediente_view,
                               abrir_votacao_ordem_view, recuperar_materia,
                               recuperar_numero_sessao,
                               reordernar_materias_expediente,
                               reordernar_materias_ordem,
                               sessao_legislativa_legislatura_ajax)

from .apps import AppConfig

app_name = AppConfig.name


urlpatterns = [
    url(r'^search/', include('haystack.urls'), name='haystack_search'),

    url(r'^sessao/', include(SessaoCrud.get_urls() + OradorCrud.get_urls() +
                             OradorExpedienteCrud.get_urls() +
                             ExpedienteMateriaCrud.get_urls() +
                             MateriaOrdemDiaCrud.get_urls())),

    url(r'^sessao/(?P<pk>\d+)/mesa$', MesaView.as_view(), name='mesa'),

    url(r'^sessao/recuperar-materia/', recuperar_materia),
    url(r'^sessao/recuperar-numero-sessao/', recuperar_numero_sessao),
    url(r'^sessao/sessao-legislativa-legislatura-ajax/',
        sessao_legislativa_legislatura_ajax),

    url(r'^sessao/(?P<pk>\d+)/(?P<spk>\d+)/abrir-votacao-expediente$',
        abrir_votacao_expediente_view,
        name="abrir_votacao_exp"),
    url(r'^sessao/(?P<pk>\d+)/(?P<spk>\d+)/abrir-votacao-ordem$',
        abrir_votacao_ordem_view,
        name="abrir_votacao"),
    url(r'^sessao/(?P<pk>\d+)/reordenar-expediente$',
        reordernar_materias_expediente,
        name="reordenar_expediente"),
    url(r'^sessao/(?P<pk>\d+)/reordenar-ordem$', reordernar_materias_ordem,
        name="reordenar_ordem"),
    url(r'^sistema/sessao-plenaria/tipo/',
        include(TipoSessaoCrud.get_urls())),
    url(r'^sistema/sessao-plenaria/tipo-resultado-votacao/',
        include(TipoResultadoVotacaoCrud.get_urls())),
    url(r'^sistema/sessao-plenaria/tipo-expediente/',
        include(TipoExpedienteCrud.get_urls())),
    url(r'^sistema/bancada/',
        include(BancadaCrud.get_urls())),
    url(r'^sistema/bloco/',
        include(BlocoCrud.get_urls())),
    url(r'^sistema/cargo-bancada/',
        include(CargoBancadaCrud.get_urls())),
    url(r'^sessao/(?P<pk>\d+)/adicionar-varias-materias-expediente/',
        AdicionarVariasMateriasExpediente.as_view(),
        name='adicionar_varias_materias_expediente'),
    url(r'^sessao/(?P<pk>\d+)/adicionar-varias-materias-ordem-dia/',
        AdicionarVariasMateriasOrdemDia.as_view(),
        name='adicionar_varias_materias_ordem_dia'),

    # PAUTA SESSÃO
    url(r'^sessao/pauta-sessao$',
        PautaSessaoListView.as_view(), name='list_pauta_sessao'),
    url(r'^sessao/pauta-sessao/pesquisar-pauta$',
        PesquisarPautaSessaoView.as_view(), name='pesquisar_pauta'),
    url(r'^sessao/pauta-sessao/(?P<pk>\d+)$',
        PautaSessaoDetailView.as_view(), name='pauta_sessao_detail'),
    url(r'^sessao/pauta-sessao/(?P<pk>\d+)/expediente/$',
        PautaExpedienteDetail.as_view(), name='pauta_expediente_detail'),
    url(r'^sessao/pauta-sessao/(?P<pk>\d+)/ordem/$',
        PautaOrdemDetail.as_view(), name='pauta_ordem_detail'),

    # Subnav sessão
    url(r'^sessao/(?P<pk>\d+)/expediente$',
        ExpedienteView.as_view(), name='expediente'),
    url(r'^sessao/(?P<pk>\d+)/presenca$',
        PresencaView.as_view(), name='presenca'),
    url(r'^sessao/(?P<pk>\d+)/painel$',
        PainelView.as_view(), name='painel'),
    url(r'^sessao/(?P<pk>\d+)/presencaordemdia$',
        PresencaOrdemDiaView.as_view(),
        name='presencaordemdia'),
    url(r'^sessao/(?P<pk>\d+)/resumo$',
        ResumoView.as_view(), name='resumo'),
    url(r'^sessao/pesquisar-sessao$',
        PesquisarSessaoPlenariaView.as_view(), name='pesquisar_sessao'),
    url(r'^sessao/(?P<pk>\d+)/matordemdia/votnom/(?P<oid>\d+)/(?P<mid>\d+)$',
        VotacaoNominalView.as_view(), name='votacaonominal'),
    url(r'^sessao/(?P<pk>\d+)/matordemdia/votnom'
        '/edit/(?P<oid>\d+)/(?P<mid>\d+)$',
        VotacaoNominalEditView.as_view(), name='votacaonominaledit'),
    url(r'^sessao/(?P<pk>\d+)/matordemdia/votsec/(?P<oid>\d+)/(?P<mid>\d+)$',
        VotacaoView.as_view(), name='votacaosecreta'),
    url(r'^sessao/(?P<pk>\d+)/matordemdia/votsec'
        '/view/(?P<oid>\d+)/(?P<mid>\d+)$',
        VotacaoEditView.as_view(), name='votacaosecretaedit'),
    url(r'^sessao/(?P<pk>\d+)/matordemdia/votsimb/(?P<oid>\d+)/(?P<mid>\d+)$',
        VotacaoView.as_view(), name='votacaosimbolica'),
    url(r'^sessao/(?P<pk>\d+)/matordemdia/votsimb'
        '/view/(?P<oid>\d+)/(?P<mid>\d+)$',
        VotacaoEditView.as_view(), name='votacaosimbolicaedit'),
    url(r'^sessao/(?P<pk>\d+)/matexp/votnom/(?P<oid>\d+)/(?P<mid>\d+)$',
        VotacaoNominalExpedienteView.as_view(), name='votacaonominalexp'),
    url(r'^sessao/(?P<pk>\d+)/matexp/votnom/edit/(?P<oid>\d+)/(?P<mid>\d+)$',
        VotacaoNominalExpedienteEditView.as_view(),
        name='votacaonominalexpedit'),
    url(r'^sessao/(?P<pk>\d+)/matexp/votsimb/(?P<oid>\d+)/(?P<mid>\d+)$',
        VotacaoExpedienteView.as_view(), name='votacaosimbolicaexp'),
    url(r'^sessao/(?P<pk>\d+)/matexp/votsec/view/(?P<oid>\d+)/(?P<mid>\d+)$',
        VotacaoExpedienteEditView.as_view(), name='votacaosimbolicaexpedit'),
    url(r'^sessao/(?P<pk>\d+)/matexp/votsec/(?P<oid>\d+)/(?P<mid>\d+)$',
        VotacaoExpedienteView.as_view(), name='votacaosecretaexp'),
    url(r'^sessao/(?P<pk>\d+)/matexp/votsec/view/(?P<oid>\d+)/(?P<mid>\d+)$',
        VotacaoExpedienteEditView.as_view(), name='votacaosecretaexpedit'),

]
