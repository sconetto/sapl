from haystack import indexes

from sapl.protocoloadm.models import DocumentoAcessorioAdministrativo


class DocumentoAcessorioIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    path = indexes.CharField(model_attr='arquivo')
    nome = indexes.CharField(model_attr='nome')
    primary_key = indexes.CharField(model_attr='id')

    def get_model(self):
        return DocumentoAcessorioAdministrativo

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
