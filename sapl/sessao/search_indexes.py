import datetime
from haystack import indexes
from sapl.sessao.models import SessaoPlenaria


class PautaIndex(indexes.SearchIndex, index.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # pub_date = indexes.DateTimeField(model_attr='pub_date')

    upload_pauta_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return SessaoPlenaria

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
