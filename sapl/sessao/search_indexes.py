import datetime
from haystack import indexes
from sapl.sessao.models import SessaoPlenaria


class PautaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    upload_pauta_auto = indexes.EdgeNgramField(model_attr='upload_pauta_auto')

    def get_model(self):
        return SessaoPlenaria

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
