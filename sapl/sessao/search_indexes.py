import datetime
from haystack import indexes
from sapl.sessao.models import SessaoPlenaria


class PautaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    upload_pauta = indexes.CharField(model_attr='numero')

    # def prepare(self, obj):
    #     data = super(PautaIndex, self).prepare(obj)
    #
    #     file_data = self._get_backend(None).extract_file_contents(
    #         obj.upload_pauta)
    #
    #     # template = loader.select_template(
    #     #     ("search/indexes/sessaoplenaria/sessaoplenaria_text.txt", ),)
    #
    #     data["text"] = template.render(Context({
    #         "object": obj,
    #         "file_data": file_data}))
    #     import ipdb; ipdb.set_trace()
    #
    #     return data

    # def prepare(self, obj):
    #     data = super(PautaIndex, self).prepare(obj)
    #
    #     if obj.upload_pauta:
    #         extracted_data = self._get_backend(None).extract_file_contents(
    #             open(obj.upload_pauta.path, "rb"))
    #
    #         if extracted_data is not None:
    #             for k, v in extracted_data['metadata'].items():
    #                 data["attr_%s" % k] = k
    #         else:
    #             self.log.warning("Metadata extraction failed for %s", obj)
    #
    #         for k, v in obj.attributes.items():
    #             data["attr_%s" % k] = v
    #
    #         t = loader.select_template(
    #             ('search/indexes/sessao/sessaoplenaria_text.txt',))
    #         data['text'] = t.render(Context({'object': obj,
    #                                          'extracted': extracted_data}))
    #     return data

    # def prepare(self, obj):
    #     data = super(PautaIndex, self).prepare(obj)
    #     if data['id'] == 'sessao.sessaoplenaria.328':
    #         with open(ob.upload_pauta.path) as f:
    #             doc = PDF(f)
    #         import ipdb; ipdb.set_trace()
    #     return data

    def get_model(self):
        return SessaoPlenaria

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
